# computer_vision_reto
# Created by; Eva Denisse Vargas Sosa 
# For: Quantum Robotics
# Place: Mexico City
# Day: Sept 11, 2022 


Use of dictionary to store position and coords
The code works with: 
  1. Camera
  2. OpenCv, numpy
  3. Python3 

Proccess: 
 1. The image is converted from color to grayscale
 2. Applied GaussianBlur to eliminate noise 
 3. Used of moments to calculate the center of the image and the figure 
 4. Edge Detection with Canny 
 5. Find the contours in Canny 
 6. For every contour find if the figure is a Polygon 
 7. Verify if that contour is a square and it has more area than a pixel 
 8. Check if the figure/square is in left or right side 
 9. Store the information in a dictionary
 
 The functionality depends on the enviroment and light. 
 It identify objects although the surface have a lot of white. 
 
