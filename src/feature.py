import numpy as np
import skimage as sk
import matplotlib.pyplot as plt

from scipy.interpolate import make_interp_spline, BSpline

def cornerCount(img: np.ndarray, labels: np.ndarray, display: bool = False):
    labelValue = np.unique(labels)

    distanceArray = []

    for i in range(len(labelValue)):

        if i == 0:
            continue
        
        #get subset image with only one label
        subSetImage = np.int_(labels == labelValue[i])


        
        #information about the labeled region and the contours of the region
        region = sk.measure.regionprops(subSetImage,img)[0]
        contours = sk.measure.find_contours(subSetImage)

        center = region.centroid

        #if there is uncontinious border, stack them
        contoursArr = contours[0]
        for i in range(1,len(contours)):
            contoursArr = np.vstack((contoursArr, contours[1]))
        
        fig, ax = (None, None)
        if display:
            fig, ax = plt.subplots(1,2,figsize=(15, 5))
            
            # Display the image and plot all contours found
            ax[0].imshow(img, cmap=plt.cm.gray)
            for contour in contours: ax[0].plot(contour[:, 1], contour[:, 0], linewidth=2)
            ax[0].plot(center[0], center[1], 'b', label='center')
            ax[0].set_title(f"Label {i} contour")
            ax[0].set_axis_off()

        #compute the distance
        distance = np.zeros((contoursArr.shape[0]))
        for i in range(distance.shape[0]): distance[i] = np.linalg.norm(center-contoursArr[i])

        distanceArray.append(distance)

        if display:

            ax[1].plot(distance)
            ax[1].set_title('Distances')

            plt.show()

    return distanceArray
