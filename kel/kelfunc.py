import gen.env as envi
import numpy as np
import gen.forms as fm


class Keldysh:

    def __init__(self, runVal, funcVal):

        self.runVal = runVal
        self.runVal.compSpace()
        self.funcVal = funcVal
        self.envi = envi.Environment(runVal)

    @property
    def fK1(self):

        V = self.runVal
        E = self.envi

        epsil = np.zeros(shape=(2, 2), dtype=np.complex128)
        epsil[0, 0] = V.ener
        epsil[1, 1] = -V.ener
        gA = np.dot(np.dot(fm.p3(), np.conj(V.gR).T), fm.p3())

        rv = (epsil - E.hamR) * self.funcVal \
            - self.funcVal * (epsil - E.hamA) \
            + V.gR * E.hamK \
            - E.hamK * gA \
            + 1j * V.lim.B_z * V.dgK0

        return -rv / V.lim.v
