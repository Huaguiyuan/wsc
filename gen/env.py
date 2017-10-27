import numpy as np


class Environment(object):

    def __init__(self, runVal):

        self.runVal = runVal

    @property
    def thermDG(self):

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
    def thermD(self):

        V = self.runVal
        return np.tanh(V.ener / (2 * V.temp))

    @property
    def deltaR(self):

        V = self.runVal
        L = self.runVal.lim

        rv = 1.764 / (2 * np.pi)
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
        rv[1, 0] = np.conj(self.deltaR)

        return rv

    @property
    def hamA(self):

        rv = np.zeros(shape=(2, 2), dtype=np.complex128)
        rv[0, 0] = self.sigmaA
        rv[1, 1] = -self.sigmaA
        rv[0, 1] = -self.deltaA
        rv[1, 0] = np.conj(self.deltaA)

        return rv

    @property
    def hamK(self):

        return (self.hamR - self.hamA) * self.thermD

    @property
    def hamKG(self):

        return (self.hamR - self.hamA) * self.thermDG

    @property
    def dzhamKG(self):
        V = self.runVal
        L = self.runVal.lim
        hZero = self.hamKG
        V.alpha += L.dAlpha
        V.compSpace()
        rv = np.cos(V.Xi) * (self.hamKG - hZero) / L.dAlpha
        V.alpha -= L.dAlpha
        V.compSpace()
        V.Xi += L.dKPolar
        V.compSpace()
        rv -= np.sin(V.Xi) * (self.hamKG - hZero) / (L.dKPolar * L.v)
        return rv
