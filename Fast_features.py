import cv2
import numpy as np
import argparse as ap
import time

if __name__ == "__main__":
    ap = ap.ArgumentParser()
    ap.add_argument('-i', '--image', help = 'path to image', required = True)
    args = vars(ap.parse_args())
    start = time.time()

    thresh_percentage = 20
    n = 12
    img = cv2.imread(args['image'])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    test = 0
    kps = []

    for i in range(0, gray.shape[1]) :

        if i > 3 and i < gray.shape[1] - 4 :

            for j in range(0, gray.shape[0]) :

                if j > 3 and j < gray.shape[0] - 4 :
                    test = test + 1
                    test_pix = []

                    test_pix.append(gray[j-3][i]) #1
                    test_pix.append(gray[j][i+3]) #5
                    test_pix.append(gray[j+3][i]) #9
                    test_pix.append(gray[j][i-3]) #13

                    nums_matched_brighter = 0
                    nums_matched_darker = 0

                    for pix in test_pix:
                        print (gray[j][i],((gray[j][i])*thresh_percentage)/100,pix)

                        if gray[j][i] + ((gray[j][i])*thresh_percentage)/100 > pix :
                            nums_matched_darker = nums_matched_darker + 1

                        elif gray[j][i] - ((gray[j][i])*thresh_percentage)/100 < pix :
                            nums_matched_brighter = nums_matched_brighter + 1

                        else :
                            pass

                        print ("*************")

                    if nums_matched_darker == 3 or nums_matched_brighter == 3 :
                        test_pix.insert(1,gray[j-3][i+1]) #2
                        test_pix.insert(2,gray[j-2][i+2]) #3
                        test_pix.insert(3,gray[j-1][i+3]) #4

                        test_pix.insert(5,gray[j+1][i+3]) #6
                        test_pix.insert(6,gray[j+2][i+2]) #7
                        test_pix.insert(7,gray[j+3][i+1]) #8

                        test_pix.insert(9,gray[j+3][i-3]) #10
                        test_pix.insert(10,gray[j+2][i+2]) #11
                        test_pix.insert(11,gray[j+1][i-3]) #12

                        test_pix.insert(13,gray[j-1][i-3]) #14
                        test_pix.insert(14,gray[j-2][i-2]) #15
                        test_pix.insert(15,gray[j-3][i-1]) #16

                        pixel_intensities = []

                        for pix in test_pix:
                            if gray[j][i] + ((gray[j][i])*thresh_percentage)/100 > pix :
                                pixel_intensities.append(0)

                            elif gray[j][i] - ((gray[j][i])*thresh_percentage)/100 < pix :
                                pixel_intensities.append(1)

                            else:
                                pixel_intensities.append(-1)

                        print (pixel_intensities)

                        if pixel_intensities.count(1) == 12 or pixel_intensities.count(0) == 12:
                            kps.append((i,j))
                        else:
                            pass

                    print("++++++++++++++++++++++++")
                else:
                    pass
            else:
                pass

    for kp in kps:
        cv2.circle(gray, kp, 1, 0, -1)

    stop = time.time()
    print ("time taken to find {} features = ".format(len(kps)), stop - start, "secs")
    cv2.imshow('image', gray)
    cv2.waitKey(0)
