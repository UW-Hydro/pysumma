from __future__ import print_function
import sys
import urllib

is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
    input = raw_input
    urlencode = urllib.pathname2url
else:
    import queue as queue
    urlencode = urllib.parse.quote