from __future__ import absolute_import, print_function
from pysumma.specworker.worker import app
import time
import subprocess
import shlex
import os

@app.task
def task_sanity_check(string, wait=1):
    print('sleeping %d seconds' % wait)
    run_command('sleep %d' % wait)
    time.sleep(wait)
    print(string)
    image_id = os.popen('basename "$(head /proc/1/cgroup)"').read().strip().split('-')[1][:-6]
    run_command('sleep %d' % wait)
    print(image_id)
    time.sleep(wait)
    return {'success': 1,'imageid': image_id}

@app.task
def task_get_registered_images():
    res = os.popen("docker images").read()
    return res


@app.task
def task_run(image_name, invoker_id, vol_mount=None, mount_target='/tmp', env_vars={}, args=''):
    print('long time task begins')
    print("Name: %s" % image_name)
    print("Local Relative Path: %s" % vol_mount)
    print("Mount target: %s" % mount_target)
    print("Invoking Container Id: %s" % invoker_id)

    # get the invoker volume mounts
    vols = os.popen("docker inspect -f '{{ .Mounts }}' %s" % invoker_id).read()
    print(vols)
    volumes = []
    for vol in vols.strip()[2:-2].split('} {'):
        atts = vol.split(' ')
        print(atts)
        mnt_path = os.path.join(mount_target, atts[3].strip('/'))
        volumes.append('-v ' + ':'.join([atts[2], mnt_path]))
    for v in volumes:
        print(v)

    if vol_mount is not None:
        # set the path to data (inside the tmp dir)
        envars = '-e %s=%s' % ('RELPATH', os.path.join('/tmp',
                                                   vol_mount.strip('/')))
    # this assumes that env_vars are relative paths
    envars = ''
    for k, v in env_vars.items():
        envars += ' -e %s=%s' % (k, v)

    run_cmd = 'docker run --rm %s %s %s %s' % (' '.join(volumes),
                                            envars,
                                            image_name, args)
    print('RUN COMMAND: %s' % run_cmd)
    res = run_command(run_cmd)
    return res


@app.task
def task_run_container(image_name, vol_mount, mount_target, invoker_id, env_vars={}):
    print('long time task begins')
    print("Name: %s" % image_name)
    print("Local Relative Path: %s" % vol_mount)
    print("Mount target: %s" % mount_target)
    print("Invoking Container Id: %s" % invoker_id)

    # get the invoker volume mounts
    vols = os.popen("docker inspect -f '{{ .Mounts }}' %s" % invoker_id).read()
    print(vols)
    volumes = []
    for vol in vols.strip()[2:-2].split('} {'):
        atts = vol.split(' ')
        print(atts)
        mnt_path = os.path.join(mount_target, atts[3].strip('/'))
        volumes.append('-v ' + ':'.join([atts[2], mnt_path]))
    for v in volumes:
        print(v)

    # set the path to data (inside the tmp dir)
    envars = '-e %s=%s' % ('RELPATH', os.path.join('/tmp',
                                                   vol_mount.strip('/')))
    # this assumes that env_vars are relative paths
    for k, v in env_vars.items():
        envars += ' -e %s=%s' % (k, v)
    print(envars)

    run_cmd = 'docker run --rm %s %s %s' % (' '.join(volumes),
                                            envars,
                                            image_name)
    print('RUN COMMAND: %s' % run_cmd)
    res = run_command(run_cmd)
    return res


@app.task
def task_run_test(name, host_volume, param, wait=5):
    print('long time task begins')
    run_command('sleep %d' % wait)
    print("Name: %s" % name)
    print("Volume: %s" % host_volume)
    print("Param: %s" % param)
    print('long time task finished')
    return 1

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    ret_output = ''
    while True:
        output = process.stdout.readline()
        ret_output += output
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return ret_output