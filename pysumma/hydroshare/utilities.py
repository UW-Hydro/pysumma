from __future__ import print_function
import os, sys
from IPython.core.display import display, HTML
import glob

from .compat import *


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def get_hs_content(resid):

    resdir = find_resource_directory(resid)

    content = {}
    for f in glob.glob('%s/*/data/contents/*' % resdir):
        fname = os.path.basename(f)
        content[fname] = f

    return content

def find_resource_directory(resid):
   
    basedir = os.environ['NOTEBOOK_HOME']
   
    # loop over all the files in userspace
    for dirpath, dirnames, filenames in os.walk(basedir):
        for dirname in [d for d in dirnames]:
            if dirname == resid:
                return os.path.join(dirpath, dirname)
    return None

def check_for_ipynb(content_files):

    links = {}
    for f, p in content_files.items():
        if f[-5:] == 'ipynb':
            fname = os.path.basename(p)
            url = urlencode(p)
            links[fname] = url
    return links

def display_tree(resid):

    # todo: display a tree view of the resource bagit, based on id
    pass

def display_resource_content_files(content_file_dictionary,
                                   text='Found the following content when parsing the HydroShare resource:'):
    
    # get ipynb files
    nbs = check_for_ipynb(content_file_dictionary)
    if len(nbs.keys()) > 0:
        display(HTML('<b>Found the following notebook(s) associated with this HydroShare resource.</b><br>Click the link(s) below to launch the notebook.'))
        
        for name, url in nbs.items():
            display(HTML('<a href=%s target="_blank">%s<a>' % (url, name)))

    # print the remaining files    
    if len(content_file_dictionary.keys()) > 0:
        display(HTML('<b>Found the following file(s) associated with this HydroShare resource.</b>'))
        
        text = '<br>'.join(content_file_dictionary.keys())
        display(HTML(text))
    
    if (len(content_file_dictionary.keys()) + len(nbs.keys())) > 0:
        display(HTML('These files are stored in a dictionary called <b>hs.content</b> for your convenience.  To access a file, simply issue the following command where MY_FILE is one of the files listed above: <pre>hs.content["MY_FILE"] </pre> '))


def load_environment(env_path=None):

    # load the environment path (if it exists)
    if env_path is None:
        if 'NOTEBOOK_HOME' in os.environ.keys():
            env_path = os.path.join(os.environ['NOTEBOOK_HOME'], '.env')

    if not os.path.exists(env_path):
        print('\nEnvironment file could not be found.  Make sure that the JUPYTER_ENV variable is set properly')
        return

    with open(env_path, 'r') as f:
        lines = f.readlines()
        print('Adding the following system variables:')
        for line in lines:
            k, v = line.strip().split('=')
            os.environ[k] = v
            print('   %s = %s' % (k, v))
        print('\nThese can be accessed using the following command: ')
        print('   os.environ[key]')
        print('\n   (e.g.)\n   os.environ["HS_USR_NAME"]  => %s' % os.environ['HS_USR_NAME'])

def get_env_var(varname):
    if varname in os.environ.keys():
        return os.environ[varname]
    else:
        return input('Could not find %s, please specify a value: ' % varname).strip()

def get_server_url_for_path(p):
    """
    gets the url corresponding to a given file or directory path
    p : path to convert into a url

    returns the url path for the filepath p
    """

    load_environment()
    fname = os.path.basename(p)
    rel_path = os.path.relpath(p, os.environ['NOTEBOOK_HOME'])
    url = urlencode(rel_path)
    return url

def get_relative_path(p):
    """
    gets the path relative to the jupyter home directory
    p: path to convert into relative path

    returns the path relative to the default jupyter home directory
    """

    return os.path.relpath(p, os.environ['NOTEBOOK_HOME'])
