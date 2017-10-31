from multiprocessing import Pool
import itertools
import os


def worker(runValue):

    if runValue.order == '0':
        import urt.func as func
    elif runValue.order == '1':
        import ukl.RK as func
    elif runValue.order == '2':
        import ret.func as func
    elif runValue.order == '3':
        import kel.RK as func
    elif runValue.order == '4':
        import qtm.RK as func
    elif runValue.order == '5':
        import qtb.RK as func

    F = func.Function(runValue)

    return {'index': runValue.index,
            'value': getattr(F, runValue.string)}


class Main:

    def __init__(self, limits, start_time, data_folder, order):

        self.limits = limits
        self.start_time = start_time
        self.data_folder = data_folder
        self.order = order

        if order in ['0', '1', '2', '3', '4', '5']:
            self.order = order
        else:
            raise ValueError("The given order is not valid")

        if self.order == '0':
            import urt.par as param
            self.string = 'gR'
        elif self.order == '1':
            import ukl.par as param
            self.string = 'gK'
        elif self.order == '2':
            import ret.par as param
            self.string = 'gR'
        elif self.order == '3':
            import kel.par as param
            self.string = 'gK'
        elif self.order == '4':
            import qtm.par as param
            self.string = 'gK'
        elif self.order == '5':
            import qtb.par as param
            self.string = 'gK'

        self.P = param.ParamSpace(self.limits, self.order, self.string)
        self.DOF = itertools.product(enumerate(self.P.temp),
                                     enumerate(self.P.ener))

    def run(self):

        print('Calculating order %s...' % self.order)

        for (iT, T), (iE, E) in self.DOF:
            self.P.getProgress(iT, iE)
            self.P.initData((iT, iE))
            self.P.loadData(self.data_folder,
                            self.start_time,
                            iT,
                            iE)
            self.DATA = {}

            ######################################
            if False:
                runs = self.P.getRun(iT, iE, self.string)
                for run in runs:
                    worker(run)
            ######################################

            run = self.P.getRun(iT, iE, self.string)
            p = Pool()
            self.DATA[self.string] = p.map(worker, run)
            p.close()

            self.P.updateData(self.DATA[self.string], self.string)

            del self.DATA

            self.P.writeData(os.path.join(self.data_folder, self.start_time))
