import gen.env as envi
import numpy as np
from math import ceil


class Keldysh:

    def __init__(self, runVal, funcVal):

        self.runVal = runVal
        self.funcVal
        self.envi = envi.Environment(runVal)

    @property
    def fK1(self):

        V = self.runVal
        E = self.envi

        tau3 = np.array([[1, 0], [0, -1]])
        epsil = np.zeros(shape=(2, 2), dtype=np.complex128)
        epsil[0, 0] = 1j * V.ener
        epsil[1, 1] = -1j * V.ener
        gA = tau3 * np.conj(V.gR).T * tau3
        if type(self.iAlpha) == int:
            dgK0 = V.dgK0[self.iAlpha]
        else:
            dgK0 = (V.dgK0[int(self.iAlpha)]
                    + V.dgK0[int(ceil(self.iAlpha))]) / 2

        rv = (epsil - E.hamR) * self.funcVal \
            - self.funcVal * (epsil - E.hamA) \
            + V.gR * E.hamK \
            - E.hamK * gA \
            + 1j * dgK0

        return rv
