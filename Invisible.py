#Import Libraries
import cv2
import numpy as np
import time

print("!! Invisibility is no more a Dream !!")

# Used to capture from the webcam
cap = cv2.VideoCapture(0)

# Time to adjust camera according to the background
time.sleep(3)
count = 0
# The background image to be displayed when cloak is on
background = 0

# Capture the background in range of 60
for i in range(60):
    ret, background = cap.read()
background = np.flip(background, axis=1)

# Read every frame from the webcam, until the camera is open
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count += 1
    img = np.flip(img, axis=1)

    # Convert the color space from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Generate masks to detect red color
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # If there is any shade of red, it will be saved to mask 1
    mask1 = mask1 + mask2 # + works as OR here

    # Open and Improve the mask image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2) # Noise Removal
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1) # Increase smoothness of image

    # Create an inverted mask to segment out the red color from the frame
    mask2 = cv2.bitwise_not(mask1) # Everything except the cloak

    # Create image showing static background frame pixels only for the masked region
    res1 = cv2.bitwise_and(background, background, mask=mask1)

    # Segment the red color part out of the frame using bitwise AND with the inverted mask
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    # Generating the final output
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0) # Linearly adding 2 images
    cv2.imshow("Eureka", finalOutput)
    k = cv2.waitKey(10)
    if k == 27:         # To end the execution,press esc
        break

cap.release()
cv2.destroyAllWindows()


