import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import skimage as sk

from scipy import ndimage as ndi

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

def thresholdOtsu(img: np.ndarray, display:bool=False) -> np.ndarray:
    """Binarise an image with the Otsu method."""

    #get the threshold
    thresholds = sk.filters.threshold_otsu(img)
    
    #apply the thresold
    imBinary = img >= thresholds

    #display the threshold image
    if(display):
        plt.imshow(imBinary,cmap="gray")
        plt.title(f"{thresholds}")
        plt.axis('off')
        plt.show()
    
    return imBinary

def distanceBasedWatershed(binaryImage: np.ndarray, display:bool = False, mainImage:any = None) -> any:

    """Perform a distance base watershed, for more information :
    https://www.sciencedirect.com/science/article/abs/pii/0165168494900604"""

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

        fig, (ax1, ax2) = plt.subplots(1,2,figsize=(10, 5))

        labelsColorOverlay = sk.color.label2rgb(labels)

        ax1.imshow(-distance, cmap=plt.cm.gray)
        ax1.set_title('Distances')
        ax1.set_axis_off()

        if mainImage is None:
            ax2.imshow(labelsColorOverlay)
        else:
            ax2.imshow(mainImage, cmap="gray")
            ax2.imshow(labelsColorOverlay, alpha=0.5)
        
        ax2.set_axis_off()
        ax2.set_title('Separated objects')
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
    imTemp = sk.morphology.opening(imTemp,footprint=sk.morphology.square(structuringElementSize))

    if(display):
        ax3.imshow(imTemp, cmap="gray")
        ax3.set_axis_off()
        ax3.set_title('Gaussian + opening')
        plt.show()
    
    return imTemp