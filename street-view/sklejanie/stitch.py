from pyimagesearch.panorama import Stitcher
import numpy
import cv2


def stich_photos(imageA, imageB, folder, filename):
    stitcher = Stitcher()
    (result, vis, ptA, ptB) = stitcher.stitch([imageA, imageB], showMatches=True)
    if result is None:
        print("no keypoints")
    else:
        imageA = imageA[:, 0:ptB[0] - imageA.shape[1], :]
        imageB = imageB[:, ptA[0]:, :]
        imageC = numpy.concatenate((imageA, imageB), 1)
        cv2.imwrite("images/" + folder + '/' + filename, imageC)
        cv2.waitKey(0)


for index in range(2, 17, 2):
    imageA = cv2.imread("images/photos/img" + str(index) + ".jpg")
    imageB = cv2.imread("images/photos/img" + str(index + 1) + ".jpg")

    filename = str(int(index/2)) + ".jpg"
    stich_photos(imageA, imageB, '1', filename)

# imageA = cv2.imread("images/photos/img17.jpg")
# imageB = cv2.imread("images/photos/img2.jpg")
# filename = "koniec.jpg"
# stich_photos(imageA, imageB, '1', filename)
#
# imageA = cv2.imread("images/1/koniec.jpg")
# imageB = cv2.imread("images/1/1.jpg")
# filename = "1.jpg"
# stich_photos(imageA, imageB, '1', filename)

for index in range(1, 9, 2):
    imageA = cv2.imread("images/1/" + str(index) + ".jpg")
    imageB = cv2.imread("images/1/" + str(index + 1) + ".jpg")

    filename = str(int((index+1)/2)) + ".jpg"
    stich_photos(imageA, imageB, '2', filename)

for index in range(1, 5, 2):
    imageA = cv2.imread("images/2/" + str(index) + ".jpg")
    imageB = cv2.imread("images/2/" + str(index + 1) + ".jpg")

    filename = str(int((index+1)/2)) + ".jpg"
    stich_photos(imageA, imageB, '3', filename)


imageA = cv2.imread("images/3/1.jpg")
imageB = cv2.imread("images/3/2.jpg")

filename = "1.jpg"
stich_photos(imageA, imageB, '4', filename)


panorama = cv2.imread("images/4/1.jpg")
print(panorama.shape[0], panorama.shape[1])  # Wysokosc, szerokosc

lenght = panorama.shape[1]
number_of_photos = 18
px_per_photo = int(lenght / number_of_photos)
print(px_per_photo)

start = 0
stop = px_per_photo
i = 1
while stop <= panorama.shape[1]:
    result = panorama[0:480, start:stop]
    start += px_per_photo
    stop += px_per_photo
    cv2.imwrite("images/stiched/" + str(i) + ".jpg", result)
    i += 1

cv2.imshow("Result", result)
cv2.waitKey(0)
