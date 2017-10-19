from ana.unidos import LDOS
import ana.unidostotal as LDOST
from gen.lim import Limits
import numpy as np
from jsci.Coding import NumericEncoder
import json
import sys
from os import getcwd
from os.path import join
from gen.parser import nameParser, getFiles


data_folder = join(getcwd(), "data/")


def compIndiDOS(orders, files, lims):
    print 'Computing DOS...'
    for iT in range(lims.nTemp):
        data = {order: np.zeros(lims.nEnergy) for order in orders}
        for iE in range(lims.nEnergy):
            index = iE + iT * lims.nEnergy
            perc = 100 * float(index) / (lims.nEnergy * lims.nTemp)
            sys.stdout.write('\r%.2f%%' % perc)
            sys.stdout.flush()
            L = {order: LDOS(files[order][index], order, 'gR')
                 for order in orders}
            for order in orders:
                data[order][iE] = np.abs(L[order].compute())
        path = {order: join(data_folder,
                            nameParser(files[order][index],
                                       'run+order+temp'))
                + '-dos' for order in orders}
        for order in orders:
            with open(path[order], 'w') as f:
                f.write(json.dumps({'param': lims.save(),
                                    'data': data[order]},
                                   cls=NumericEncoder,
                                   indent=4,
                                   sort_keys=True))
    sys.stdout.write('\rDone!    \n')
    sys.stdout.flush()


def compTotalDOS(files, lims):
    print 'Computing DOS...'
    for iT in range(lims.nTemp):
        data = np.zeros(lims.nEnergy)
        for iE in range(lims.nEnergy):
            index = iE + iT * lims.nEnergy
            perc = 100 * float(index) / (lims.nEnergy * lims.nTemp)
            sys.stdout.write('\r%.2f%%' % perc)
            sys.stdout.flush()
            L = LDOST.LDOS(files['0'][index], files['1'][index])
            data[iE] = np.abs(L.compute())
        path = join(data_folder,
                    nameParser(files['0'][index], 'run')
                    + '-total-'
                    + nameParser(files['0'][index], 'temp')
                    + '-dos')
        with open(path, 'w') as f:
            f.write(json.dumps({'param': lims.save(),
                                'data': data},
                               cls=NumericEncoder,
                               indent=4,
                               sort_keys=True))
    sys.stdout.write('\rDone!    \n')
    sys.stdout.flush()


def Main():
    orders = ['0', '1']
    files = getFiles(orders, data_folder, 'raw')
    lims = Limits()
    lims.loadFromFile(data_folder)
    compIndiDOS(orders, files, lims)
    compTotalDOS(files, lims)


if __name__ == '__main__':
    orders = ['0', '1']
    files = getFiles(orders, data_folder, 'raw')
    lims = Limits()
    lims.loadFromFile(data_folder)
    compIndiDOS(orders, files, lims)
    compTotalDOS(files, lims)
