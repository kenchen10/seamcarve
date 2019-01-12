import numpy as np
import cv2
from get_image import get_energy, get_matrix

class SeamRemover:

    def __init__(self, img):
        self.img = get_matrix(img)
        self.w = self.img.shape[1]
        self.h = self.img.shape[0]
        self.energy = get_energy(self.img)

    def findVerticalSeam(self):
        m = self.energy.copy()
        seam = np.array([])
        for r in np.arange(1, self.h):
            for c in np.arange(0, self.w):
                if c == 0:
                    m[r][c] = self.energy[r][c] + min(m[r-1][c], m[r-1][c+1])
                elif c == self.w - 1:
                    m[r][c] = self.energy[r][c] + min(m[r-1][c-1], m[r-1][c])
                else:
                    m[r][c] = self.energy[r][c] + min(m[r-1][c-1], m[r-1][c], m[r-1][c+1])
        min_idx = np.nonzero(m[len(m) - 1] == min(m[len(m) - 1]))[0][0]
        seam = np.append(seam, min_idx)
        n = len(m)
        l = min_idx if min_idx == 0 else min_idx - 1
        r = min_idx if min_idx == len(m[0]) else min_idx + 1
        m = min_idx
        for row in np.arange(n - 2, 0, -1):
            min_val = min([m[row][l], m[row][m], m[row][r]])
            if min_val == m[row][l]:
                seam = np.append(seam, l)
                l = l if l == 0 else l - 1
                r = l if l == len(m[0]) else l + 1
                m = l
            elif min_val == m[row][r]:
                seam = np.append(seam, r)
                l = r if r == 0 else r - 1
                r = r if r == len(m[0]) else r + 1
                m = r
            else:
                seam = np.append(seam, m)
                l = m if m == 0 else m - 1
                r = m if m == len(m[0]) else m + 1
                m = m
        print(seam)
        return seam

    #def findHorizontalSeam():

    #def removeHorizontalSeam(seam):

    #def removeVerticalSeam(seam):

def main():
    remover = SeamRemover("images/me.jpg")
    remover.findVerticalSeam()

if __name__ == '__main__':
    main()
