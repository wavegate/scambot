import cv2
import numpy as np
from matplotlib import pyplot as plt
import pyautogui
import time
import random

if __name__ == "__main__":
    img = cv2.imread('images/in_memory_to_disk.png',0)
    img2 = img.copy()
    template = cv2.imread('images/stash.png',0)
    w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        print(meth, top_left, bottom_right)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()

def myadd(xs,ys):
     return tuple((x + y)/2 for x, y in izip(xs, ys))

def locImage(name, threshold):
    max_val = 0
    while max_val < threshold:
        print("searching for {}".format(name))
        img = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        cv2.imwrite("images/in_memory_to_disk.png", img)
        img = cv2.imread("images/in_memory_to_disk.png",0)
        img2 = img.copy()
        template = cv2.imread('images/{}.png'.format(name),0)
        w, h = template.shape[::-1]

        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        methods2 = ['cv2.TM_CCOEFF_NORMED']
        for meth in methods2:
            img = img2.copy()
            method = eval(meth)

            # Apply template Matching
            res = cv2.matchTemplate(img,template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print(max_val)
            if max_val >= threshold:
                # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
                if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                    top_left = min_loc
                else:
                    top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                
                cv2.rectangle(img,top_left, bottom_right, 255, 2)
                center = ((top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
                return(center)
            #plt.subplot(121),plt.imshow(res,cmap = 'gray')
            #plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            #plt.subplot(122),plt.imshow(img,cmap = 'gray')
            #plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            #plt.suptitle(meth)

            #plt.show()
        time.sleep(random.uniform(0.3, 0.6))