import cv2


def RegionCheck(foo, ListPath):#foo defines x-coordinate of point

    if (foo <= 130) and (ListPath[0] is not 0):
        ListPath[0] = 0
    if (foo > 130) and (foo <= 320) and (ListPath[1] is not 0):
        ListPath[1] = 0
    if (foo > 320) and (foo <= 510) and (ListPath[2] is not 0):
        ListPath[2] = 0
    if (foo > 510) and (ListPath[3] is not 0):
        ListPath[3] = 0

    return ListPath

def imgshow(ListPath,t,imn,Winname):
	
	#insert a ListPath, t, input img to read
	
	if(ListPath[1:3]==[1, 1]):
		imn = cv2.imread(str(t)+"frwd.bmp")
		cv2.imshow('Navig',imn)
	elif(ListPath[2:4]==[1, 1]):
		imn = cv2.imread(str(t)+"right.bmp")
		cv2.imshow('Navig',imn)
	elif(ListPath[0:2]==[1, 1]):
		imn = cv2.imread(str(t)+"left.bmp")
		cv2.imshow('Navig',imn)
	else:
		imn = cv2.imread(str(t)+"back.bmp")
		cv2.imshow('Navig',imn)
	
	#pass
def DirectBot():
    pass
