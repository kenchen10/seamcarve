import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_matrix(img):
    ret = cv2.imread(img)
    ret = cv2.cvtColor(ret, cv2.COLOR_BGR2RGB)
    return ret

def get_energy(img):
    del_x = np.square(np.roll(img, -1, axis = 0) - np.roll(img, 1, axis = 0))
    del_y = np.square(np.roll(img, -1, axis = 1) - np.roll(img, 1, axis = 1))
    energy = np.sum(del_x, axis = 2) + np.sum(del_y, axis = 2)
    return energy

def main():
    plt.imshow(get_matrix("images/me.jpg"))
    # plt.gray()
    plt.show()

if __name__ == '__main__':
    main()
