import sys
import itertools

class progressBar(object):

    def __init__(self, progress_message, type='pulse', refresh_delay=0.25,
                 finish_message='Finished', error_message='An error has occurred'):

        # create a simple progress bar
        self.barArray = itertools.cycle(self._pulseArrays(type))
        self.refreshDelay = float(refresh_delay)

        self.messagelen = 0

        self.msg = '\r' + progress_message
        self.fin = '\r' + finish_message 
        self.err = '\r' + error_message 
        
        self.overwrite_progress_length = len(self.msg) + 21

    def _pulseArrays(self, ptype='pulse'):

        types = ['pulse', 'dial', 'dots']

        # set default bar type to 'pulse' if unknown type is provided
        if ptype not in types:
            ptype = 'pulse'

        if ptype == 'pulse':
            parray = ['___________________'] * 20
            parray = [parray[i][:i] + '/\\' + parray[i][i:] for i in range(len(parray))]
            parray = parray + parray[-2:0:-1]

        elif ptype == 'dial':
            parray = ['-', '\\', '|', '/', '-', '\\', '|', '/']

        elif ptype == 'dots':
            parray = [' ']*19
            parray = ['.'*i + ''.join(parray[i:]) for i in range(len(parray))]
#            parray = ['.'*i for i in range(20)]

        return parray

    def _clearLine(self):
        chars = len(self.msg) + 27

        sys.stdout.write('\r%s' % (chars * ' '))
        sys.stdout.flush()

    def updateProgressMessage(self, msg):
        self.msg = '\r' + msg

    def writeprogress(self):
        # self._clearLine()
        msg = '\r' + ' '.join([self.msg, next(self.barArray)])
        #msg += 'x'*(len(self.msg) - len(msg))
        sys.stdout.write(msg)

        sys.stdout.flush()
    
    def success(self):
        self._clearLine()
        sys.stdout.write(self.fin + '\n')
        sys.stdout.flush()
    
    def error(self):
        self._clearLine()
        sys.stdout.write(self.err + '\n')
        sys.stdout.flush()

    def update(self, *args):
        self._clearLine()
        msg = self.msg + ' %s  '
        args += tuple([next(self.barArray)])
        sys.stdout.write(msg % args)
        sys.stdout.flush()
