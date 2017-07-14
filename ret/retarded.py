import retspace
import retfunc 
import retmc
from multiprocessing import Pool, Manager
import time
import itertools

def worker( run_in ):

    F = retfunc.Retarded( run_in.getSet(), run_in[ 'data' ] )
    M = retmc.MonteCarlo( F )
    out = M.do()
    
    return { 'index' : run_in[ 'index' ], 'value' : out }

class RetardedMain:

    def __init__( self, limits, run_time, data_folder ):

        self.run_time = run_time
        self.data_folder = data_folder
        self.limits = limits
        self.P = retspace.ParamSpace( self.limits, self.data_folder, self.run_time )

    def run( self ):
        

        for ( iT, T ), ( iE, E ) in itertools.product( enumerate( self.P.temp ), enumerate( self.P.energy ) ):

            self.P.initialiseData( ( iT, iE ) )
            DATA = dict()
            run = self.P.getRun()
            
            #######################################
            for r in run:
                a = worker( r ) 
            ######################################

            p = Pool()
            DATA[ string ] = p.map( worker, run ) 
            p.close()

            self.P.updateData( DATA[ string ], string )

            del DATA

            P.writeData( '%s%s' % ( self.data_folder, self.start_time ) )
            print '#######--%d-%d--#######' % ( iT, iE )

