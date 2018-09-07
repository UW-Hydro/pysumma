from __future__ import absolute_import, print_function
import sys, urllib
is_py2 = sys.version[0] == '2'
if is_py2:
    print('Python 2!')
    import Queue as queue
    input = raw_input
    urlencode = urllib.pathname2url
else:
    import queue
    urlencode = urllib.parse.quote