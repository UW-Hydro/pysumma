from __future__ import print_function
import time
from threading import Thread

from . import progress
from .compat import *


class threadWrapper(object):
    def __init__(self, func):
        self.func = func
        self.results = queue.Queue()

    def run(self, *args, **kwargs):

        # create a thread to run the function in
        self.thread = Thread(target=self.f, args=args, kwargs=kwargs)

        # start the thread
        self.thread.start()

    def f(self, *args, **kwargs):
        res = self.func(*args, **kwargs)
        self.results.put(res)

    def close(self):
        self.thread.join()

    def result(self):
        results = None
        if not self.results.empty():
            results = self.results.get()
        return results

    def isAlive(self):
        return self.thread.isAlive()

    def join(self):
        self.thread.join()

def runThreadedFunction(msg, success, func, *args, **kwargs):

    pbar = progress.progressBar(msg, type='dial',
                                finish_message=success)

    # create a thread for the function
    threaded_func = threadWrapper(func)
    threaded_func.run(*args, **kwargs)

    # print message while the function is running
    while(threaded_func.isAlive()):
        time.sleep(.2)
        pbar.writeprogress()

    # join the thread
    threaded_func.join()
    pbar.success()

    res = threaded_func.result()

    return res