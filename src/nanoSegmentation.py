import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import skimage as sk

from scipy import ndimage as ndi


def thresholdOtsu(img: np.ndarray) -> any:
    """Binarise an image with the Otsu method."""

    #get the threshold
    thresholds = sk.filters.threshold_otsu(img)
    
    #apply the thresold
    imBinary = img >= thresholds

    return imBinary,thresholds

def distanceBasedWatershed(img: np.ndarray, display:bool = False) -> any:

    """Perform a distance base watershed, for more information :
    https://www.sciencedirect.com/science/article/abs/pii/0165168494900604"""
    binaryImage,thresholds = thresholdOtsu(img)

    # Calculate the Euclidean distance transform of the binary image
    distance = ndi.distance_transform_edt(binaryImage)

    # Identify local maxima in the distance transform image
    coords = sk.feature.peak_local_max(distance, footprint=np.ones((5, 5)), labels=binaryImage)

    # Create a mask image from the identified local maxima
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)

    # Perform watershed segmentation on the distance transform image
    labels = sk.segmentation.watershed(-distance, markers, mask=binaryImage,  compactness=0.001)

    fig, ax = (None, None)
    if display:

        fig, (ax1, ax2,ax3) = plt.subplots(1,3,figsize=(15, 5))

        labelsColorOverlay = sk.color.label2rgb(labels)

        ax1.imshow(binaryImage, cmap=plt.cm.gray)
        ax1.set_title(f"thresholds: {thresholds:.2f}")
        ax1.set_axis_off()

        ax2.imshow(-distance, cmap=plt.cm.gray)
        ax2.set_title('Distances')
        ax2.set_axis_off()

        ax3.imshow(labelsColorOverlay)
        ax3.set_axis_off()
        ax3.set_title('Separated objects')

        plt.show()

    return labels, markers

def preProcessing(img: np.ndarray, structuringElementSize:int = 7, sigma:float = 2.5, display: bool = False) -> np.ndarray:

    """Process an image to faciliate the upcoming algorithm"""

    #Perform histogram equalisation
    imTemp = sk.exposure.equalize_adapthist(img)

    fig, ax = (None, None)

    if(display):

        fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=(15, 5))


        ax1.hist(imTemp.flatten(),bins=16)
        ax1.set_title('Histogram')

        ax2.imshow(imTemp, cmap="gray")
        ax2.set_axis_off()
        ax2.set_title('equalised exposure')

    #Perform a opening on the image
    imTemp = sk.filters.gaussian(imTemp, sigma=sigma)

    imTemp = sk.morphology.opening(imTemp,footprint=sk.morphology.disk(structuringElementSize))

    if(display):
        ax3.imshow(imTemp, cmap="gray")
        ax3.set_axis_off()
        ax3.set_title('Gaussian + opening')
        plt.show()
    
    return imTemp

def mergeLabel(img: np.ndarray,labels: np.ndarray, display:bool = False)-> np.ndarray: 
    """constructs a Region Adjacency Graph (RAG) and progressively merges regions that are similar in color.\n
    Merging two adjacent regions produces a new region with all the pixels from the merged regions.\n
    Regions are merged until no highly similar region pairs remain.\n
    more info : https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_rag_merge.html#sphx-glr-auto-examples-segmentation-plot-rag-merge-py"""

    def _weight_mean_color(graph, src, dst, n):
        
        diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
        diff = np.linalg.norm(diff)
        return {'weight': diff}


    def merge_mean_color(graph, src, dst):
        
        graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
        graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
        graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                        graph.nodes[dst]['pixel count'])


    g = sk.future.graph.rag_mean_color(img, labels)
    newLabels = sk.future.graph.merge_hierarchical(labels, g, thresh=100, rag_copy=False, in_place_merge=True, merge_func=merge_mean_color, weight_func=_weight_mean_color)

    fig, ax = (None, None)
    if display:

        fig, (ax1, ax2) = plt.subplots(1,2,figsize=(10, 5))

        labelsColorOverlay = sk.color.label2rgb(labels)
        newLabelsColorOverlay = sk.color.label2rgb(newLabels)

        ax1.imshow(labelsColorOverlay)
        ax1.set_axis_off()
        ax1.set_title("Old label")

        ax2.imshow(newLabelsColorOverlay)
        ax2.set_axis_off()
        ax2.set_title("Merged label")

        plt.show()


    return newLabels