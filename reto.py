##
# Created by: Eva Denisse Vargas Sosa 
# Date: Sept 11, 2022 
##
import cv2 as c 
import numpy as np

capture = c.VideoCapture(0)
# Dictionary where the information will store the position and coordinates
informacion = {}
codigos = 1
# While the buffer is open
while (True):
    # kernel used to iterate over the image
    kernel = np.ones((5,5), np.uint8) 
    ret, frame = capture.read()
    v = np.median(frame)
    #The image is converted from color to grayscale
    gray_img = c.cvtColor(frame, c.COLOR_BGR2GRAY)
    gray_img = c.equalizeHist(gray_img) # Equalize is used to sharp the image
    # Applied GaussianBlur to eliminate noise 
    gray_img = c.GaussianBlur(gray_img, (1,1),0)

    # Moments only works with one channel color, in this case the image have to be in gray
    # Moments help to get the center of a shape, and I'm using it for calculate the center of the image 
    m = c.moments(gray_img)
    # This coords are needed to compare the position of the ArUco code
    cx_imagen = m['m10']/m['m00']
    cy_imagen = m['m01']/m['m00']
    # Otsu method is use for two reason: 
    #   The first is to minimize the within-class variance
    #   the second is to maximize the between-class variance 
    optimal_threshold, otsu = c.threshold(gray_img,127,200,c.THRESH_TOZERO)
    # automatic Canny edge detection 
    sigma = 0.33
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    canny = c.Canny(otsu, lower, upper) 
    # Contours are searched according to edge detection
    cnts,_ = c.findContours(canny, c.RETR_EXTERNAL, c.CHAIN_APPROX_SIMPLE)
    c.drawContours(frame, cnts, -1, (0,0,255), 2)
    # For each of the contours: 
    for i in cnts:
        # It is the parameter that specifies the approximation precision
        epsilon = 0.01*c.arcLength(i,True) #  Es true cuando la curva aproximada es cerrada,
        #                                      es decir que tanto el primer como el último vértice están conectado
        # This allows to find figures
        approx = c.approxPolyDP(i,epsilon,True)
        #print(len(approx))
        x,y,w,h = c.boundingRect(approx)
        #This is a sencond parameter to find a especific figure 
        area = c.contourArea(i)
        # If the figure that detects have 4 sides 
        if len(approx)==4:
            # It calculate the ratio 
            aspect_ratio = float(w)/h
            #If required you can change the size of the square
            # It is recommended that it adapts to the square
            if aspect_ratio == 1 and area > 50: #If the ratio is = 1 and the area > 50
                # Write in the picture where is the figure or in this case, where the square is. 
                c.drawContours(frame, [approx], 0, (255, 255, 0), 5) 
                # Calculate the center of the square
                M = c.moments(i)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # Then draw it 
                c.circle(frame, (cx, cy), 5, (255, 0, 255), -1) 
                # Little disclamer: I use the main frame to visualize what is happening 
                # If the coord x of the square is less than the center of the main frame, that means that 
                #           the figure are in the left side of the frame 
                if cx < cx_imagen:
                    direccion = "Izquierda"
                    c.putText(frame,'Izquierda', (x,y-5),1,1.5,(255, 0, 255),2)
                # If the coord x of the square is more than the center of the main frame, that means that 
                #           the figure are in the right side of the frame
                elif cx > cx_imagen:
                    direccion = "Derecha"
                    c.putText(frame,'Derecha', (x,y-5),1,1.5,(255, 0, 255),2)
                # If the coord x of the square is equal than the center of the main frame, that means that 
                #           the figure are in the middle of the frame
                elif cx == cx_imagen:
                    direccion = "Centro"
                    c.putText(frame,'Centro', (x,y-5),1,1.5,(255, 0, 255),2)
                # this store the info of the square
                informacion[codigos] = [direccion, cx, cy] 
                codigos += 1
                print(informacion) 
                # If the square is more than 11, it reset the dictionary 
                if codigos == 11:
                    codigos = 1
                    informacion = {}

    
    c.imshow("Video frame", frame)
   
    if (c.waitKey(1) == ord('s')):
        break
capture.release()
c.destroyAllWindows()
    
