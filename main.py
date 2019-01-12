import matplotlib.pyplot as plt
import cv2
from SeamRemover import SeamRemover
import timeit
from skimage import transform
from skimage import filters
import datetime
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image file")
ap.add_argument("-d", "--direction", type=str,
	default="vertical", help="seam removal direction")
ap.add_argument("-w", "--write", type=bool,
	default=False, help="write image")
# ap.add_argument("-n", "--filename", type=str,
# 	default=r"test/img_name.png", help="name your file")
args = vars(ap.parse_args())

# Usage: python main.py --image img_name.jpg --direction vertical

fast = True
remover = SeamRemover("images/"+args["image"])

def animate(iterations, f):
    """
    Animates each iteration of seam carving. 
    """
    start = timeit.default_timer()
    for i in range(iterations):
        if args["direction"] == "vertical":
            seam = f().astype(int)
            remover.removeVerticalSeam(seam)
        else:
            seam = f().astype(int)
            remover.removeHorizontalSeam(seam)
        plt.imshow(remover.img)
        plt.title("iteration: " + str(i))
        plt.pause(0.0001)
    stop = timeit.default_timer()
    # cv2.imwrite(r'images/'+'output'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.png', remover.img)
    if args["write"]:
        cv2.imwrite(r"test/test4.png", remover.img)
    print('Time: ', stop - start)


def main():
    # np.set_printoptions(threshold=np.nan)
    plt.figure(1); plt.clf()
    plt.axis('off')
    if not fast:
        f = remover.findVerticalSeamDP
    else:
        f = remover.findVerticalSeamDPFaster
    animate(10, f)

if __name__ == '__main__':
    main()
