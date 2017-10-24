import numpy as np
import gen.parser as ps
from gen.lim import Limits
import kel.kelparam as kPar
import uni.uniparamkel as uPar
import gen.forms as fm


class HCOND:

    def __init__(self, path, spin):

        self.path = path
        self.spin = spin
        self.lim = Limits()
        self.lim.readData(self.path)
        self.P = {}
        self.P['1'] = uPar.ParamSpace(self.lim, '1', 'gK')
        self.P['3'] = kPar.ParamSpace(self.lim, '3', 'gK')

    def compute(self):

        rv = 0.0
        for iE, E in enumerate(self.P['1'].ener):
            hE = 0.0
            for order in self.P:
                f = ps.getFile(self.path, order, self.spin, iE)
                self.P[order].readData(f[iE])
            for iXi, Xi in enumerate(self.P['1'].kPol):
                hXi = 0.0
                for iTheta, Theta in enumerate(self.P['1'].kAzi):
                    hTheta = 0.0
                    g = self.P['1'].data['gK'][iXi, iTheta] \
                        + self.P['3'].data['gK'][iXi, iTheta]
                    hTheta += np.trace(np.dot(fm.p3(), g))
                    hTheta /= 8 * np.pi * np.pi
                    hTheta *= self.lim.dTheta
                    if iTheta in [0, self.lim.nKAzimu - 1]:
                        pass
                    elif iTheta % 2 == 0:
                        hTheta *= 4.0
                    else:
                        hTheta *= 2.0
                    hXi += hTheta
                hXi *= np.sin(Xi) * np.cos(Xi) * self.lim.dKPolar * 3.0 / 8.0
                if iXi in [0, self.lim.nKPolar - 1]:
                    pass
                elif iXi % 2 == 0:
                    hXi *= 4.0
                else:
                    hXi *= 2.0
                hE += hXi
            hE *= E * self.lim.dEnergy * 3.0 / 8.0
            if iE in [0, self.lim.nEnergy - 1]:
                pass
            elif iE % 2 == 0:
                hE *= 4.0
            else:
                hE *= 2.0
            rv += hE
