import numpy as np
from get_image import get_energy, get_matrix
import cv2

fast = True

class SeamRemover:

    def __init__(self, img):
        self.img = get_matrix(img)
        self.w = self.img.shape[1]
        self.h = self.img.shape[0]
        self.energy = get_energy(self.img)
        if fast:
            self.m_mat = self.get_m_mat()

    def get_m_mat(self):
        """
        Single calculation of the DP matrix for the approximation algorithm.
        """
        m_mat = self.energy.copy()
        for r in np.arange(1, self.h):
            for c in np.arange(0, self.w):
                if c == 0:
                    m_mat[r][c] = self.energy[r][c] + min(m_mat[r-1][c], m_mat[r-1][c+1])
                elif c == self.w - 1:
                    m_mat[r][c] = self.energy[r][c] + min(m_mat[r-1][c-1], m_mat[r-1][c])
                else:
                    m_mat[r][c] = self.energy[r][c] + min(m_mat[r-1][c-1], m_mat[r-1][c], m_mat[r-1][c+1])
        return m_mat


    def findVerticalSeamDP(self):
        """
        O(n^2) optimal DP solution.
        """
        m_mat = self.energy.copy()
        for r in np.arange(1, self.h):
            for c in np.arange(0, self.w):
                if c == 0:
                    m_mat[r][c] = self.energy[r][c] + min(m_mat[r-1][c], m_mat[r-1][c+1])
                elif c == self.w - 1:
                    m_mat[r][c] = self.energy[r][c] + min(m_mat[r-1][c-1], m_mat[r-1][c])
                else:
                    m_mat[r][c] = self.energy[r][c] + min(m_mat[r-1][c-1], m_mat[r-1][c], m_mat[r-1][c+1])
        seam = np.array([])
        min_idx = np.nonzero(m_mat[len(m_mat) - 1] == min(m_mat[len(m_mat) - 1]))[0][0]
        seam = np.append(seam, min_idx)
        n = len(m_mat)
        l = min_idx if min_idx == 0 else min_idx - 1
        r = min_idx if min_idx == len(m_mat[0]) - 1 else min_idx + 1
        m = min_idx
        for row in np.arange(n - 2, 0, -1):
            min_val = min([m_mat[row][l], m_mat[row][m], m_mat[row][r]])
            if min_val == m_mat[row][l]:
                seam = np.append(seam, l)
                l = l if l == 0 else l - 1
                r = l if l == len(m_mat[0]) - 1 else l + 1
                m = l
            elif min_val == m_mat[row][r]:
                seam = np.append(seam, r)
                l = r if r == 0 else r - 1
                r = r if r == len(m_mat[0]) - 1 else r + 1
                m = r
            else:
                seam = np.append(seam, m)
                l = m if m == 0 else m - 1
                r = m if m == len(m_mat[0]) - 1 else m + 1
                m = m
        return seam

    def findVerticalSeamDPFaster(self):
        """
        An approximation of the Optimal seam carving solution, by not recalulating
        the DP matrix at each carve. Performs recognizably worse than the Optimal
        solution. About 3x speed up.
        """
        seam = np.array([])
        min_idx = np.nonzero(self.m_mat[len(self.m_mat) - 1] == min(self.m_mat[len(self.m_mat) - 1]))[0][0]
        seam = np.append(seam, min_idx)
        n = len(self.m_mat)
        l = min_idx if min_idx == 0 else min_idx - 1
        r = min_idx if min_idx == len(self.m_mat[0]) - 1 else min_idx + 1
        m = min_idx
        for row in np.arange(n - 2, 0, -1):
            min_val = min([self.m_mat[row][l], self.m_mat[row][m], self.m_mat[row][r]])
            if min_val == self.m_mat[row][l]:
                seam = np.append(seam, l)
                l = l if l == 0 else l - 1
                r = l if l == len(self.m_mat[0]) - 1 else l + 1
                m = l
            elif min_val == self.m_mat[row][r]:
                seam = np.append(seam, r)
                l = r if r == 0 else r - 1
                r = r if r == len(self.m_mat[0]) - 1 else r + 1
                m = r
            else:
                seam = np.append(seam, m)
                l = m if m == 0 else m - 1
                r = m if m == len(self.m_mat[0]) - 1 else m + 1
                m = m
        return seam

    #def findHorizontalSeam():

    def findVerticalSeamDPMAX(self):
        """
        Gets rid of the maximum energy seam. Good for removing people/objects.
        """
        m_mat = self.energy.copy()
        seam = np.array([])
        for r in np.arange(1, self.h):
            for c in np.arange(0, self.w):
                if c == 0:
                    m_mat[r][c] = self.energy[r][c] + max(m_mat[r-1][c], m_mat[r-1][c+1])
                elif c == self.w - 1:
                    m_mat[r][c] = self.energy[r][c] + max(m_mat[r-1][c-1], m_mat[r-1][c])
                else:
                    m_mat[r][c] = self.energy[r][c] + max(m_mat[r-1][c-1], m_mat[r-1][c], m_mat[r-1][c+1])
        min_idx = np.nonzero(m_mat[len(m_mat) - 1] == max(m_mat[len(m_mat) - 1]))[0][0]
        seam = np.append(seam, min_idx)
        n = len(m_mat)
        l = min_idx if min_idx == 0 else min_idx - 1
        r = min_idx if min_idx == len(m_mat[0]) - 1 else min_idx + 1
        m = min_idx
        for row in np.arange(n - 2, 0, -1):
            min_val = max([m_mat[row][l], m_mat[row][m], m_mat[row][r]])
            if min_val == m_mat[row][l]:
                seam = np.append(seam, l)
                l = l if l == 0 else l - 1
                r = l if l == len(m_mat[0]) - 1 else l + 1
                m = l
            elif min_val == m_mat[row][r]:
                seam = np.append(seam, r)
                l = r if r == 0 else r - 1
                r = r if r == len(m_mat[0]) - 1 else r + 1
                m = r
            else:
                seam = np.append(seam, m)
                l = m if m == 0 else m - 1
                r = m if m == len(m_mat[0]) - 1 else m + 1
                m = m
        return seam

    def removeVerticalSeam(self, seam):
        n = len(self.energy)
        new_img = np.zeros(shape=(self.h, self.w - 1, 3))
        new_energy = np.zeros(shape=(self.h, self.w - 1))
        if fast:
            new_m_mat = np.zeros(shape=(self.h, self.w - 1))
        # pool = multiprocessing.Pool()
        # pool.map(self.remove_elem, np.arange(0, n, 1))
        for row in np.arange(0, n, 1):
            col = seam[len(self.energy) - 2 - row]
            new_row = np.delete(self.img[row], col, axis = 0)
            new_img[row] = new_row
            new_row_energy = np.delete(self.energy[row], col, axis = 0)
            new_energy[row] = new_row_energy
            if fast:
                new_row_m_mat = np.delete(self.m_mat[row], col, axis = 0)
                new_m_mat[row] = new_row_m_mat


        self.w -= 1
        self.img = new_img
        self.energy = new_energy
        if fast:
            self.m_mat = new_m_mat

    # def remove_elem(self, row):
    #     col = self.seam[len(self.energy) - 2 - row]
    #     new_row = np.delete(self.img[row], col, axis = 0)
    #     self.new_img[row] = new_row
    #     new_row_energy = np.delete(self.energy[row], col, axis = 0)
    #     self.new_energy[row] = new_row_energy
    #     new_row_m_mat = np.delete(self.m_mat[row], col, axis = 0)
    #     self.m_mat[row] = new_row_m_mat


    #def removeHorizontalSeam(seam):

def main():
    remover = SeamRemover("images/153x197.jpg")

if __name__ == '__main__':
    main()
