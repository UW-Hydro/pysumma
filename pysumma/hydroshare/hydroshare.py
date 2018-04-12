from __future__ import print_function
import os
import getpass
import glob
from IPython.core.display import display, HTML
from hs_restclient import HydroShare, HydroShareAuthBasic
from hs_restclient import HydroShareHTTPException
from datetime import datetime as dt
import pickle
import shutil

from . import threads
from . import resource
from . import utilities
from .compat import *


class hydroshare():
    def __init__(self, username=None, password=None, cache=True):
        self.hs = None
        self.content = {}

        # load the HS environment variables
        # todo: this should be set as a path variable somehow.
        #       possibly add JPY_TMP to Dockerfile
        self.cache = cache
        if cache:
            utilities.load_environment(os.path.join(
                                        os.environ['NOTEBOOK_HOME'], '.env'))
        self.auth_path = '/home/jeff/.auth'

        # todo: either use JPY_USR or ask them to
        #       enter their hydroshare username
        uname = username
        if uname is None:
            if 'HS_USR_NAME' in os.environ.keys():
                uname = os.environ['HS_USR_NAME']

        if password is None:
            # get a secure connection to hydroshare
            auth = self.getSecureConnection(uname)
        else:
            print('WARNING: THIS IS NOT A SECURE METHOD OF CONNECTING TO '
                  'HYDROSHARE...AVOID TYPING CREDENTIALS AS PLAIN TEXT')
            auth = HydroShareAuthBasic(username=uname, password=password)

        try:
            self.hs = HydroShare(auth=auth)
            self.hs.getUserInfo()
            print('Successfully established a connection with HydroShare')

        except HydroShareHTTPException as e:
            print('Failed to establish a connection with HydroShare.\n  '
                  'Please check that you provided the correct credentials.\n'
                  '%s' % e)

            # remove the cached authentication
            if os.path.exists(self.auth_path):
                os.remove(self.auth_path)

            return None

    def _addContentToExistingResource(self, resid, content_files):

        for f in content_files:
            self.hs.addResourceFile(resid, f)

    def getSecureConnection(self, username=None):
        """Establishes a secure connection with hydroshare.

        args:
        -- email: email address associated with hydroshare

        returns:
        -- hydroshare api connection
        """

        if not os.path.exists(self.auth_path):
            print('\nThe hs_utils library requires a secure connection to '
                  'your HydroShare account.')
            if username is None:
                username = input('Please enter your HydroShare username: ') \
                        .strip()
            p = getpass.getpass('Enter the HydroShare password for user '
                                '\'%s\': ' % username)
            auth = HydroShareAuthBasic(username=username, password=p)

            if self.cache:
                with open(self.auth_path, 'wb') as f:
                    pickle.dump(auth, f, protocol=2)

        else:

            with open(self.auth_path, 'rb') as f:
                auth = pickle.load(f)

        return auth

    def getResourceMetadata(self, resid):
        """Gets metadata for a specified resource.

        args:
        -- resid: hydroshare resource id

        returns:
        -- resource metadata object
        """

        science_meta = self.hs.getScienceMetadata(resid)
        system_meta = self.hs.getSystemMetadata(resid)
        return resource.ResourceMetadata(system_meta, science_meta)

    def createHydroShareResource(self, abstract, title, derivedFromId=None,
                                 keywords=[], resource_type='genericResource',
                                 content_files=[], public=False):
        """Creates a hydroshare resource.

        args:
        -- abstract: abstract for resource (str, required)
        -- title: title of resource (str, required)
        -- derivedFromId: id of parent hydroshare resource (str, default=>None)
        -- keywords: list of subject keywords (list, default=>[])
        -- resource_type: type of resource to create (str, default=>
                                                     'GenericResource')
        -- content_files: data to save as resource content (list, default=>[])
        -- public: resource sharing status (bool, default=>False)

        returns:
        -- None
        """

        # query the hydroshare resource types and make sure that
        # resource_type is valid
        restypes = {r.lower(): r for r in self.hs.getResourceTypes()}
        try:
            res_type = restypes[resource_type]
        except KeyError:
            display(HTML('<b style="color:red;">[%s] is not a valid '
                         'HydroShare resource type.</p>' % resource_type))
            return None

        # get the 'derived resource' metadata
        if derivedFromId is not None:
            try:
                # update the abstract and keyword metadata
                meta = self.getResourceMetadata(derivedFromId)

                abstract = meta.abstract \
                    + '\n\n[Modified in JupyterHub on %s]\n%s' \
                    % (dt.now(), abstract)

                keywords = set(keywords + meta.keywords)
            except:
                display(HTML('<b style="color:red;">Encountered an error '
                             ' while setting the derivedFrom relationship '
                             ' using id=%s. Make sure this resource is '
                             ' is accessible to your account. '
                             % derivedFromId))
                display(HTML('<a href=%s target="_blank">%s<a>' %
                             ('https://www.hydroshare.org/resource/%s'
                              % derivedFromId, 'View the "DerivedFrom" '
                              'Resource')))
                return None

        f = None if len(content_files) == 0 else content_files[0]

        # create the hs resource (1 content file allowed)
        resid = threads.runThreadedFunction('Creating HydroShare Resource',
                                            'Resource Created Successfully',
                                            self.hs.createResource,
                                            resource_type=res_type,
                                            title=title,
                                            abstract=abstract,
                                            resource_file=f,
                                            keywords=keywords)

        # add the remaining content files to the hs resource
        try:
            if len(content_files) > 1:
                self.addContentToExistingResource(resid, content_files[1:])
        except Exception as e:
            print(e)

        display(HTML('Resource id: %s' % resid))
        display(HTML('<a href=%s target="_blank">%s<a>' %
                     ('https://www.hydroshare.org/resource/%s'
                      % resid, 'Open Resource in HydroShare')))
        return resid

    def getResourceFromHydroShare(self, resourceid, destination='.'):
        """Downloads content of a hydroshare resource.

        args:
        -- resourceid: id of the hydroshare resource (str)
        -- destination: path to save resource, default
                        /user/[username]/notebooks/data (str)

        returns:
        -- None
        """

        # default_dl_path = utilities.get_env_var('NOTEBOOK_HOME')
        dst = os.path.abspath(destination)
        print (dst)
        download = True

        # check if the data should be overwritten
        # dst_res_folder = os.path.join(dst, resourceid)
        # if os.path.exists(dst_res_folder):
            # res = input('This resource already exists in your userspace.'
                        # '\nWould you like to overwrite this data [Y/n]? ')
            # if res != 'n':
                # shutil.rmtree(dst_res_folder)
            # else:
                # download = False

        # re-download the content if desired
        if download:
            try:

                # download the resource (threaded)
                threads.runThreadedFunction('Downloading Resource',
                                            'Download Finished',
                                            self.hs.getResource,
                                            resourceid,
                                            destination=dst,
                                            unzip=True)

                print('Successfully downloaded resource %s' % resourceid)

            except Exception as e:
                display(HTML('<b style="color:red">Failed to retrieve '
                             'resource content from HydroShare: %s</b>' % e))
                return None

        # load the resource content
        # outdir = os.path.join(dst, '%s/%s' % (resourceid, resourceid))
        # content_files = glob.glob(os.path.join(outdir, 'data/contents/*'))

        # content = {}
        # for f in content_files:
            # fname = os.path.basename(f)

            # trim the base name relative to the data directory
            # dest_folder_name = os.path.dirname(destination).split('/')[-1]
            # f = os.path.join(dest_folder_name,
                             # os.path.relpath(f, dest_folder_name))

            # content[fname] = f

        # show the resource content files
        # utilities.display_resource_content_files(content)

        # update the content dictionary
        # self.content.update(content)

    def addContentToExistingResource(self, resid, content):
        """Adds content files to an existing hydroshare resource.

        args:
        -- resid: id of an existing hydroshare resource (str)
        -- content: files paths to be added to resource (list)

        returns:
        -- None
        """

        threads.runThreadedFunction('Adding Content to Resource',
                                    'Successfully Added Content Files',
                                    self._addContentToExistingResource,
                                    resid, content)

    def loadResource(self, resourceid):
        """Loads the contents of a previously downloaded resource.

         args:
         -- resourceid: the id of the resource that has been downloaded (str)

         returns:
         -- {content file name: path}
        """

        resdir = utilities.find_resource_directory(resourceid)
        if resdir is None:
            display(HTML('<b style="color:red">Could not find any resource '
                         'matching the id [%s].</b> <br> It is likely that '
                         'this resource has not yet been downloaded from '
                         'HydroShare.org, or it was removed from the '
                         'JupyterHub server. Please use the following '
                         'command to aquire the resource content: '
                         '<br><br><code>hs.getResourceFromHydroShare(%s)'
                         '</code>.' % (resourceid, resourceid)))
            return
        
        # create search paths.  Need to check 2 paths due to hs_restclient bug #63.
        search_paths = [os.path.join(resdir, '%s/data/contents/*' % resourceid), 
                        os.path.join(resdir, 'data/contents/*')]
                        
        content = {}
        found_content = False
        for p in search_paths:
            content_files = glob.glob(p)
            if len(content_files) > 0:
                found_content = True
                display(HTML('<p>Downloaded content is located at: %s</p>' % resdir))
                display(HTML('<p>Found %d content file(s). \n</p>'
                             % len(content_files)))
            for f in content_files:
                fname = os.path.basename(f)
                content[fname] = f
        if len(content.keys()) == 0:
            display(HTML('<p>Did not find any content files for resource id: %s</p>' % resourceid))

        utilities.display_resource_content_files(content)
        self.content = content

    def getContentFiles(self, resourceid):
        """Gets the content files for a resource that exists on the
           Jupyter Server

        args:
        -- resourceid: the id of the hydroshare resource

        returns:
        -- {content file name: path}
        """

        content = utilities.get_hs_content(resourceid)
        return content

    def getContentPath(self, resourceid):
        """Gets the server path of a resources content files.

        args:
        -- resourceid: the id of the hydroshare resource

        returns:
        -- server path the the resource content files
        """

        path = utilities.find_resource_directory(resourceid)
        if path is not None:
            return os.path.join(path, resourceid, 'data/contents')
