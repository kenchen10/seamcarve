import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import cv2
from SeamRemover import SeamRemover


style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def main():
    # np.set_printoptions(threshold=np.nan)
    remover = SeamRemover("images/spongebob.jpg")
    fig,ax = plt.subplots(1,1)
    image = remover.img
    img = ax.imshow(image)
    #remover2 = SeamRemover("images/me.jpg")
    #seam = remover.findVerticalSeam().astype(int)
    for i in range(200):
        seam = remover.findVerticalSeam().astype(int)
        remover.removeVerticalSeam(seam)
        img.set_data(remover.img)
        fig.canvas.draw_idle()
        # plt.imshow(remover.img)
        # plt.show()
    # n = len(remover.energy)
    # for row in np.arange(n - 1, 0, -1):
    #     remover.img[row][seam[n - 1 - row]] = [255,0,0]

    # plt.imshow(remover.img)
    # plt.show()

if __name__ == '__main__':
    main()
