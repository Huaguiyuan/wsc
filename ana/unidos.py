import numpy as np
from uni.uniparam import ParamSpace
from gen.lim import Limits


class LDOS:

    def __init__(self, path, order, func):

        self.path = path
        self.order = order
        self.func = func
        self.lim = Limits()
        self.lim.readData(self.path)
        self.P = ParamSpace(self.lim, order, [func])
        self.P.readData(self.path)

    def compute(self):

        tau3 = np.array([[1, 0], [0, -1]])
        rv = 0.0
        for iXi, Xi in enumerate(self.P.kPol):
            dosXi = 0.0
            for iTheta, Theta in enumerate(self.P.kAzi):
                dosTheta = 0.0
                if self.order == '0':
                    indexIn = (iXi, iTheta, 0)
                elif self.order == '1':
                    indexIn = (iXi, iTheta)
                g = self.P.data[self.P.strings[0]][indexIn]
                dosTheta += 1.0 * 1j / (4.0 * np.pi)
                dosTheta *= np.trace(tau3 * g)
                dosTheta *= self.P.lim.dKAzimu / 3.0

                if iTheta == 0 or iTheta == self.P.lim.nKAzimu:
                    pass
                elif iTheta % 2 == 0:
                    dosTheta *= 4.0
                else:
                    dosTheta *= 2.0
                dosXi += np.imag(dosTheta)

            dosXi *= np.sin(Xi) * self.P.lim.dKPolar / 3.0
            if iXi == 0 or iXi == self.P.lim.nKPolar:
                pass
            elif iXi % 2 == 0:
                dosXi *= 4.0
            else:
                dosXi *= 2.0
            rv += dosXi
            print rv
        return rv
