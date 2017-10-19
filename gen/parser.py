from os import listdir
from os.path import join, isfile
from jsci.Coding import NumericDecoder
import json


def fileName(order, spinDir, iT, iE):
    return '-%s-%s-T%04dE%04d' % (order, spinDir, iT, iE)


def nameParser(filename, part):
    if part == 'run':
        return filename[-30:-16]
    elif part == 'run+order':
        return filename[-30:-13]
    elif part == 'run+order+spin':
        return filename[-30:-10]
    elif part == 'run+order+spin+temp':
        return filename[-30:-5]
    elif part == 'temp':
        return filename[-10:-5]
    elif part == 'spin+temp':
        return filename[-14:-5]


def filter(order, folder, kind):
    if kind == 'raw':
        return [join(folder, f) for f in listdir(folder)
                if isfile(join(folder, f))
                and '-%s-' % (order) in f
                and 'dos' not in f]
    if kind == 'dos':
        return [join(folder, f) for f in listdir(folder)
                if isfile(join(folder, f))
                and '-%s-' % (order) in f
                and 'dos' in f]


def getFiles(orders, folder, kind):
    return {order: sorted(filter(order, folder, kind)) for order in orders}


def getData(files):
    rv = {}
    for f in files:
        rv[f] = json.loads(f.read(), cls=NumericDecoder)['data']
    return rv
