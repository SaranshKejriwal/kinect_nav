import freenect
import cv2
import numpy as np
from functions import *

def nothing(x):
    pass

#cv2.namedWindow('edge')
cv2.namedWindow('Video')
cv2.moveWindow('Video',5,5)
cv2.namedWindow('Navig',cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow('Navig',400,100)
cv2.moveWindow('Navig',700,5)
#cv2.namedWindow('Fin')
#cv2.namedWindow('Win')
kernel = np.ones((5, 5), np.uint8)


print('Press ESC in window to stop')
cv2.createTrackbar('val1', 'Video', 37, 1000, nothing)
cv2.createTrackbar('val2', 'Video', 43, 1000, nothing)
cv2.createTrackbar('bin', 'Video',20,50,nothing)
cv2.createTrackbar('erode', 'Video',4,10,nothing)#after plenty of testing
imn=cv2.imread('blank.bmp')
im0=cv2.imread("Collision Alert.bmp")
im1=cv2.imread("VCP Reverse.bmp")
#cv2.createTrackbar('dilate', 'edge',0,10,nothing)
def pretty_depth(depth):
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

while 1:
	cv2.imshow('Navig',imn)
	flag120=[1, 1, 1, 1]
	f12=0
	f8=0
#get kinect input__________________________________________________________________________
	dst = pretty_depth(freenect.sync_get_depth()[0])#input from kinect
    	#orig = freenect.sync_get_video()[0]
    	#orig = cv2.cvtColor(orig,cv2.COLOR_BGR2RGB) #to get RGB image, which we don't want
	#cv2.flip(orig, 0, orig)#since we keep kinect upside-down
    	#cv2.flip(orig, 1,orig)# thus correcting upside-down mirror effect
    	cv2.flip(dst, 0, dst)#since we keep kinect upside-down
	cv2.flip(dst, 1,dst)# thus correcting upside-down mirror effect
    
#rectangular border (improved edge detection + closed contours)___________________________ 
	cv2.rectangle(dst,(0,0),(640,480),(40,100,0),2)
	   
#image binning (for distinct edges)________________________________________________________
    	binn=cv2.getTrackbarPos('bin', 'Video') 
    	e=cv2.getTrackbarPos('erode', 'Video') 
    	#d=cv2.getTrackbarPos('dilate', 'edge') 
    	dst = (dst/binn)*binn
    	#dst = (dst/20)*20 #after plenty of testing 
    	dst=cv2.erode(dst, kernel, iterations=e)
    	#dst=cv2.dilate(dst, kernel, iterations=d)#dilations don't help
    
 	  
#Video detection___________________________________________________________________________
    	v1 = 37
    	v2 = 43
    	v1 = cv2.getTrackbarPos('val1', 'Video')
    	v2 = cv2.getTrackbarPos('val2', 'Video')
    	edges = cv2.Canny(dst, v1, v2)
    	#cv2.imshow('edge', edges)

#finding contours__________________________________________________________________________
    	contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    	cv2.drawContours(dst, contours, -1, (0, 0, 255), -1)
    #cv2.drawContours(orig, contours, -1, (0, 0, 255), -1)
#finding contour center of mass (moments)___________________________________________________
    	cx=0
    	cy=0
    	try:
        	for i in range(len(contours)):
            		M = cv2.moments(contours[i])
	    
            		cx = int(M['m10']/M['m00'])
            		cy = int(M['m01']/M['m00'])
            		#cv2.circle(dst, (cx, cy), 6, (0, 255, 0), 3)
           # cx = int(cx/len(contours))
           # cy = int(cy/len(contours))
    	except:
      		pass

#boundingRect approach_______________________________________________________________________
    	cv2.createTrackbar('epsilon', 'Video', 1, 100, nothing)#for approxPolyDP
    	ep=cv2.getTrackbarPos('epsilon', 'Video') 
    	#for i in range(len(contours)):
		#if (cv2.contourArea(contours[i])>1):
    			#x,y,w,h = cv2.boundingRect(contours[i])#upright rectangle
			#cv2.rectangle(dst,(x,y),(x+w,y+h),(150,100,0),2)
			#cv2.circle(dst, (x+w/2,y+h/2), 1, (0, 255, 0), 3)
			
			#rect=cv2.minAreaRect(contours[i])#rotated rect
			#box = cv2.cv.BoxPoints(rect)                     Rotated Rect approach failed
			#box = np.int0(box)
			#cv2.drawContours(dst,[box],0,(50,0,255),2)
#approxPolyDP approach________________________________________________________________________
		#approx = cv2.approxPolyDP(contours[i],(ep/100)*cv2.arcLength(contours[i],True),True)
		#cv2.drawContours(dst, approx, -1, (0, 0, 2), 1)

#defined points approach (to check: runtime)________________________________________________
	cv2.createTrackbar('spacing', 'Video', 30, 100, nothing)#for approxPolyDP
    	spac=cv2.getTrackbarPos('spacing', 'Video') 
    	(rows,cols)=dst.shape # 480 rows and 640 cols
    	#print cols
	

    	for i in range(rows/spac): #note the presence of colon
		for j in range(cols/spac):
			cv2.circle(dst, (spac*j,spac*i), 1, (0, 255, 0), 1)
			if (dst[spac*i,spac*j]==80):
				f8=1
				cv2.putText(dst,"0",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),2)
				cv2.putText(dst,"Collision Alert!",(30,30),cv2.FONT_HERSHEY_TRIPLEX,1,(2),1)
				cv2.imshow('Navig',im0)
			if (dst[spac*i,spac*j]==100):
				cv2.putText(dst,"1",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),2)
				cv2.putText(dst,"Very Close proximity. Reverse",(30,60),cv2.FONT_HERSHEY_TRIPLEX,1,(2),1)
				if(f8==0):
					cv2.imshow('Navig',im1)
			if (dst[spac*i,spac*j]==120):
				f12=1
				cv2.putText(dst,"2",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0),1)
				cv2.putText(dst,"Close proximity.Go      immediately",(30,90),cv2.FONT_HERSHEY_DUPLEX,1,(2),1)
				
				#print spac*j
				if(spac*j<=130):
					flag120[0]=0					
				if(spac*j>130 and spac*j<=320):
					flag120[1]=0
				if(spac*j>320 and spac*j<=510):
					flag120[2]=0
				if(spac*j>510):
					flag120[3]=0
				#print flag0, flag1, flag2, flag3
				

				
			if (dst[spac*i,spac*j]==140):
				cv2.putText(dst,"3",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
			if (dst[spac*i,spac*j]==160):
				cv2.putText(dst,"4",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
			if (dst[spac*i,spac*j]==180):
				cv2.putText(dst,"5",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
			if (dst[spac*i,spac*j]==200):
				cv2.putText(dst,"6",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
			if (dst[spac*i,spac*j]==220):
				cv2.putText(dst,"7",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)


				
#imshow outputs______________________________________________________________________   
    #cv2.imshow('Input',orig)
	#print flag
	#cv2.destroyWindow('Navig')
	if(flag120[1:3]==[1, 1] and f12==1):
		#print flag, "FWD"
		cv2.putText(dst," frwd",(325,90),cv2.FONT_HERSHEY_DUPLEX,1,(2),1)
	elif(flag120[2:4]==[1, 1] and f12==1):
		#print flag, "RIGHT"
		cv2.putText(dst," right",(325,90),cv2.FONT_HERSHEY_DUPLEX,1,(2),1)
	elif(flag120[0:2]==[1, 1] and f12==1):
		#print flag, "LEFT"
		cv2.putText(dst," left",(325,90),cv2.FONT_HERSHEY_DUPLEX,1,(2),1)
	elif(f12==1):
		#print flag, "BACK"
		cv2.putText(dst," back",(325,90),cv2.FONT_HERSHEY_DUPLEX,1,(2),1)
	cv2.line(dst,(130,0),(130,480),(0),1)
	cv2.line(dst,(320,0),(320,480),(0),1)
	cv2.line(dst,(510,0),(510,480),(0),1)
    	cv2.imshow('Video', dst)
    	
       	if(cv2.waitKey(1) & 0xFF == ord('b')):
        	break
