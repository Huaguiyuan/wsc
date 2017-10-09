import numpy as np


class Environment(object):

    def __init__(self, runVal):

        self.runVal = runVal

    @property
    def thermD(self):

        V = self.runVal
        L = self.runVal.lim

        rv = -V.ener * V.Z * L.tempInc
        rv /= (2
               * V.temp
               * V.temp
               * np.cosh(V.ener / (2 * V.temp))
               * np.cosh(V.ener / (2 * V.temp)))

        return rv

    @property
    def deltaR(self):

        V = self.runVal
        L = self.runVal.lim

        rv = 1.0
        rv *= 1.764 / (2 * np.pi)
        rv *= np.tanh(np.sqrt(L.T_c / V.temp - 1.0))
        rv *= np.sin(V.Xi)
        rv *= (L.gamma1 * np.cos(V.Theta) + 1j * L.gamma2 * np.sin(V.Theta))

        return rv

    @property
    def deltaA(self):

        return self.deltaR

    @property
    def sigmaR(self):

        return -1j * self.runVal.lim.tau

    @property
    def sigmaA(self):

        return 1j * self.runVal.lim.tau

    @property
    def sigmaK(self):

        return 1j * self.runVal.lim.tau

    @property
    def hamR(self):

        rv = np.zeros(shape=(2, 2), dtype=np.complex128)
        rv[0, 0] = self.sigmaR
        rv[1, 1] = -self.sigmaR
        rv[0, 1] = -self.deltaR
        rv[1, 0] = -np.conj(self.deltaR)

        return rv

    @property
    def hamK(self):

        rv = (self.hamR - self.hamA) * self.thermD

        return rv
