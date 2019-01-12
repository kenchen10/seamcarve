import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import cv2
from SeamRemover import SeamRemover

def main():
    # np.set_printoptions(threshold=np.nan)
    plt.ion()
    remover = SeamRemover("images/spongebob.jpg")
    for i in range(2):
        seam = remover.findVerticalSeam().astype(int)
        remover.removeVerticalSeam(seam)
        plt.figure(1); plt.clf()
        plt.imshow(remover.img)
        plt.pause(3)

if __name__ == '__main__':
    main()
