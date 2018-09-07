from pysumma.specworker.tasks import *
import time
import os


if __name__ == '__main__':

    volume = os.path.abspath('/share')
    print(volume)

    # get the id of the current container
    image_id = os.popen('basename "$(head /proc/1/cgroup)"').read().strip()

    # all paths should be relative to the mounted volume
    vars = {'LOCALBASEDIR': 'share/summa_tests',
            'OUTDIR': 'output/syntheticTestCases/celia1990/',
            'MASTERPATH': 'settings/syntheticTestCases/celia1990/summa_fileManager_celia1990.txt'
            }

    res = run_container.delay('summa',
                              volume,
                              '/tmp/summa',
                              image_id,
                              vars)
    while not res.ready():
        time.sleep(1)
        print('...working')
    print(res.result)
#    print(os.listdir(volume))
    print('finished')



#if __name__ == '__main__':
#    for _ in xrange(10):
#        result = longtime_add.delay(1,2)
#        print 'Task finished?',result.ready()
#        print 'Task result:',result.result
#        time.sleep(1)
#        print 'Task finished"',result.ready()
#        print 'Task result:',result.result