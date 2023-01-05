import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import skimage as sk

from scipy import ndimage as ndi

import os


def openFile(path: str, scale: int=1,invert:bool = True, display: bool=False) -> np.ndarray:
    """Open a file with skimage and change is representation to gray scale in the range 0 to 255.
    Please note that the inversion of the image is done by default.
    """
    #open the image and rescale it
    im = plt.imread(path)
    im = sk.transform.resize(im, (im.shape[0]/scale,im.shape[1]/scale))

    #perform RGBA to RGB to Gray
    #or if image is RGB, change it to gray directly
    if(im.shape[2] > 3):
        im = 255*sk.color.rgb2gray(sk.color.rgba2rgb(im))
    else:
         im = 255*sk.color.rgb2gray(im)

    #invert the image if important element are dark in the image
    #since nanoparticles are often dark this is true by default
    if invert:
        im = 255 - im

    #cast as int
    im = im.astype(np.int16)

    if(display):
        plt.imshow(im,cmap="gray")
        plt.axis('off')
        plt.show

    return im


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