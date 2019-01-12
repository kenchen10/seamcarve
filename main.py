import matplotlib.pyplot as plt
import cv2
from SeamRemover import SeamRemover
import timeit

def animate(iterations):
    start = timeit.default_timer()
    remover = SeamRemover("images/spongebob.jpg")
    for i in range(iterations):
        seam = remover.findVerticalSeamDP().astype(int)
        remover.removeVerticalSeam(seam)
        plt.imshow(remover.img)
        plt.title("iteration: " + str(i))
        plt.pause(0.0001)
    stop = timeit.default_timer()
    print('Time: ', stop - start)

def main():
    # np.set_printoptions(threshold=np.nan)
    plt.figure(1); plt.clf()
    plt.axis('off')
    animate(20)

if __name__ == '__main__':
    main()
