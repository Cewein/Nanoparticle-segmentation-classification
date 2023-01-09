import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import skimage as sk

from scipy import ndimage as ndi

import os


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
    
    if display:
        labelsColorOverlay = sk.color.label2rgb(labels)

        plt.imshow(-distance, cmap=plt.cm.gray)
        plt.title('Distances')
        plt.axis('off')
        plt.show()

        if mainImage is None:
            plt.imshow(labelsColorOverlay)
        else:
            plt.imshow(mainImage, cmap="gray")
            plt.imshow(labelsColorOverlay, alpha=0.5)
        
        plt.axis('off')
        plt.title('Separated objects')
        plt.show()

    return labels, markers

def PreProcessing(img: np.ndarray, structuringElementSize:int = 7, sigma:float = 2.5, display: bool = False) -> np.ndarray:

    """Process an image to faciliate the upcoming algorithm"""

    #Perform histogram equalisation
    imTemp = sk.exposure.equalize_adapthist(img)

    if(display):
        _ = plt.hist(imTemp.flatten(),bins=16)
        plt.show()

        plt.figure()
        plt.imshow(imTemp, cmap="gray")
        plt.show()

    #Perform a opening on the image to 
    imTemp = sk.morphology.opening(imTemp,footprint=sk.morphology.square(structuringElementSize))
    imTemp = sk.filters.gaussian(imTemp, sigma=sigma)

    if(display):
        plt.imshow(imTemp, cmap="gray")
        plt.show()
    
    return imTemp