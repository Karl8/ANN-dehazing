from functions import *
import argparse
from skimage import transform
import os
parser = argparse.ArgumentParser(description='Remove image haze using dark channel prior method')
parser.add_argument('-s','--scale', action="store", dest="scale", default=1, type=float, help="Scaling factor for images")
parser.add_argument('-f','--folder', action="store", dest="folder", default='beijing1', help="folder name")
parser.add_argument('-n','--file', action="store", dest="file", default='IMG_8763', help="file name")

args = parser.parse_args()

scalingFactor = args.scale
folder = args.folder
fileName = args.file

def deHaze(imageRGB, fileName):
    # imageRGB = imageRGB / 255.0
    cv2.imwrite('output/' + fileName + '_imageRGB.jpg', imageRGB)

    

    print('Getting Dark Channel Prior')
    darkChannel = getDarkChannel(imageRGB);
    # cv2.imwrite('output/' + fileName + '_dark.jpg', darkChannel * 255.0)

    print('Getting Atmospheric Light')
    atmLight = getAtmLight(imageRGB, darkChannel);

    print('Getting Transmission')
    transmission = getTransmission(imageRGB, atmLight);
    # cv2.imwrite('output/' + fileName + '_transmission.jpg', transmission * 255.0)

    print('Getting Scene Radiance', transmission.shape)
    radiance = getRadiance(atmLight, imageRGB, transmission);
    # cv2.imwrite('output/' + fileName + '_radiance.jpg', radiance * 255.0)

    print('Apply Soft Matting')
    mattedTransmission = performSoftMatting(imageRGB, transmission);
    # cv2.imwrite('output/' + fileName + '_refinedTransmission.jpg', mattedTransmission * 255.0)

    print('Getting Scene Radiance')
    betterRadiance = getRadiance(atmLight, imageRGB, mattedTransmission);
    # cv2.imwrite('output/' + fileName + '_refinedRadiance.jpg', betterRadiance * 255.0)

    return radiance, betterRadiance

nms = ["./result/result/43_1_input.jpg","./result/result/816_2_input.jpg"]

for nm in nms:
    hazed_img =  cv2.imread(nm)
    rad, refined = deHaze(hazed_img, nm.replace("/result/result",""))
    cv2.imwrite(nm.replace(".jpg", "_baseline.jpg"), refined)


