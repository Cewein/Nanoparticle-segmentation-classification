import os

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import skimage as sk

def getBoundingBox(img: np.ndarray, label: np.ndarray, sizeThreshold:int = 500, display:bool = False) -> list:
    "from a label list, getthe bouding box with regionprops from skimage measure. the size threshold is dependant on the image size."

    fig, ax = (None, None)
    if(display):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(img, cmap="gray")

    bondingBoxArray = []

    for region in sk.measure.regionprops(label):
        # take regions with large enough areas
        if region.area >= sizeThreshold:
            # draw rectangle around segmented coins
            bondingBoxArray.append(region.bbox)

            if(display):
                minr, minc, maxr, maxc = region.bbox
                rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                        fill=False, edgecolor='red', linewidth=2)
                ax.add_patch(rect)

    if(display):
        ax.set_axis_off()
        plt.tight_layout()
        plt.show()

    return bondingBoxArray

def exctractParticle(img: np.ndarray, bondingBoxArray: list, pictureName: str, save:bool = False, display: bool = False):
    "save a sub image into a folder, can be displayed"

    if(save and not os.path.isdir(f'out/{pictureName}/')):
        os.makedirs(f'out/{pictureName}/')


    for i in range(len(bondingBoxArray)):
        minr, minc, maxr, maxc = bondingBoxArray[i]

        extendr = int((maxr - minr) * 0.5)
        extendc = int((maxc - minc) * 0.5)

        extminr = np.max([(minr-extendr),0])
        extmaxr = np.min([(maxr+extendr),img.shape[0]])
        extminc = np.max([(minc-extendc),0])
        extmaxc = np.min([(maxc+extendc),img.shape[1]])

        subimg = img[extminr:extmaxr,extminc:extmaxc]

        if(display):
            plt.figure()
            plt.imshow(subimg, cmap="gray")
            plt.show()

        if(save):
            plt.imsave(f"out/{pictureName}/output-{i}.png",subimg, cmap="gray")