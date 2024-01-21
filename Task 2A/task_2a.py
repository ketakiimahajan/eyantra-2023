'''
*****************************************************************************************
*
*        		===============================================
*           		Geo Guide (GG) Theme (eYRC 2023-24)
*        		===============================================
*
*  This script is to implement Task 2A of Geo Guide (GG) Theme (eYRC 2023-24).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 1880 ]
# Author List:		[ Rena Shoby, Pratik Panchal, Sammod Date, Ketaki Mahajan ]
# Filename:			task_2a.py
# Functions:	    [ detect_ArUco_details, mark_ArUco_image ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import numpy as np
import cv2
from cv2 import aruco
import math
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def detect_ArUco_details(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns two dictionaries where one
    contains details regarding the center coordinates and orientation of the marker
    and the second dictionary contains values of the 4 corner coordinates of the marker. 
    
    First output: The dictionary `ArUco_details_dict` should should have the id of the marker 
    as the key and the value corresponding to that id should be a list containing the following details
    in this order: [[center_x, center_y], angle from the vertical]     
    This order should be strictly maintained in the output
    Datatypes:
    1. id - int
    2. center coordinates - int
    3. angle - int, x and y coordinates should be combined as a list for each corner

    Second output: The dictionary `ArUco_corners` should contain the id of the marker as key and the
    corresponding value should be an array of the coordinates of 4 corner points of the markers
    Datatypes:
    1. id - int
    2. corner coordinates - each coordinate value should be float, x and y coordinates should 
    be combined as a list for each corner

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `ArUco_details_dict` : { dictionary }
            dictionary containing the details regarding the ArUco marker

    `ArUco_corners` : { dictionary }
            dictionary containing the details regarding the corner coordinates of the ArUco marker
    
    Example call:
    ---
    ArUco_details_dict, ArUco_corners = detect_ArUco_details(image)

    Example output for 2 markers in an image:
    ---
    * ArUco_details_dict = {9: [[311, 490], 0], 3: [[158, 175], -22]}
    * ArUco_corners = 
       {9: array([[211., 389.],
       [412., 389.],
       [412., 592.],
       [211., 592.]], dtype=float32), 
       3: array([[109.,  46.],
       [284., 118.],
       [207., 304.],
       [ 33., 232.]], dtype=float32)}
    """    
    ##############	ADD YOUR CODE HERE	##############
    
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250) # predefined dictionary of markers with size specified
    parameters = cv2.aruco.DetectorParameters() # initializing parameters
    detector = cv2.aruco.ArucoDetector(dictionary, parameters) # instance of detector with dictionary & parameters

    markerCorners, markerIds, rejected_candidates = detector.detectMarkers(image) # detecting markers in img using created detector
    
    ArUco_details_dict = {} # initializing dictionaries
    ArUco_corners = {}
    
    if markerIds is not None: # checking if markers detected
        for i in range(len(markerIds)): # if detected interating through unique marker ids
            marker_id = int(markerIds[i][0]) # extracting id 
            ArUco_corners[marker_id] = markerCorners[i][0] # appending corners of markers
            center = np.mean(markerCorners[i][0], axis=0).astype(int) # finding center

            colors = [(0, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)] # colors to draw dots at coners detected
            for col_index, corner in enumerate(markerCorners[i][0]): # drawing dots at corner 
                cv2.circle(image, tuple(corner.astype(int)), 5, colors[col_index], -1)

            # cv2.putText(image, str(marker_id), tuple(markerCorners[i][0][0].astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            cv2.circle(image, tuple(center), 5, (0, 0, 255), -1) # drawing dots at center

            # finding the orientation
            top_left_x, top_left_y = markerCorners[i][0][0] # getting top left and top right coordinates
            top_right_x, top_right_y = markerCorners[i][0][1]

            slope = (top_right_y - top_left_y) / (top_right_x - top_left_x) # finding slope

            angle = math.degrees(math.atan(slope)) # slope = tan(angle with x-axis)

            # comparison used find orientation
            # if center of marker is right of midpoint of line = marker is tilted towards the left = -180
            if center[0] > (top_left_x + top_right_x) / 2:
                angle = -angle

            angle = int(round(angle))
            ArUco_details_dict[marker_id] = [center.tolist(), angle] # storing center and angle of marker 
            
    # # print("ArUco_corners:")
    # print(ArUco_corners)

    # # print("\nArUco_details_dict:")
    # print(ArUco_details_dict)

    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    ##################################################
    
    return ArUco_details_dict, ArUco_corners 

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE CODE BELOW #########	

def mark_ArUco_image(image,ArUco_details_dict, ArUco_corners):

    for ids, details in ArUco_details_dict.items():
        center = details[0]
        cv2.circle(image, center, 5, (0,0,255), -1)

        corner = ArUco_corners[int(ids)]
        cv2.circle(image, (int(corner[0][0]), int(corner[0][1])), 5, (50, 50, 50), -1)
        cv2.circle(image, (int(corner[1][0]), int(corner[1][1])), 5, (0, 255, 0), -1)
        cv2.circle(image, (int(corner[2][0]), int(corner[2][1])), 5, (128, 0, 255), -1)
        cv2.circle(image, (int(corner[3][0]), int(corner[3][1])), 5, (25, 255, 255), -1)

        tl_tr_center_x = int((corner[0][0] + corner[1][0]) / 2)
        tl_tr_center_y = int((corner[0][1] + corner[1][1]) / 2) 

        cv2.line(image,center,(tl_tr_center_x, tl_tr_center_y),(255,0,0),5)
        display_offset = int(math.sqrt((tl_tr_center_x - center[0])**2+(tl_tr_center_y - center[1])**2))
        cv2.putText(image,str(ids),(center[0]+int(display_offset/2),center[1]),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        angle = details[1]
        cv2.putText(image,str(angle),(center[0]-display_offset,center[1]),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    
    return image

if __name__ == "__main__":

    # path directory of images in test_images folder
    img_dir_path = "C:\\Users\\Ketaki Mahajan\\OneDrive\\Desktop\\eyantra\\Task_2A_files\\public_test_cases\\"

    marker = 'aruco'

    for file_num in range(0,2):
        img_file_path = img_dir_path +  marker + '_' + str(file_num) + '.png'

        # read image using opencv
        img = cv2.imread(img_file_path)

        print('\n============================================')
        print('\nFor ' + marker  +  str(file_num) + '.png')
   
        ArUco_details_dict, ArUco_corners = detect_ArUco_details(img)
        print("Detected details of ArUco: " , ArUco_details_dict)

        # displaying the marked image
        img = mark_ArUco_image(img, ArUco_details_dict, ArUco_corners) 
        cv2.imshow("Marked Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
