#!/usr/bin/python3
'''
Fabric tasks to deploy web_static on our servers
'''
from fabric.api import local, run, put, env
from datetime import datetime
import os

env.hosts = ['52.91.178.165', '18.206.198.119']


def do_pack():
    '''Generates a .tgz archive from the contents of web_static folder'''
    time_now = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_name = 'web_static_' + time_now + '.tgz'

    try:
        local('mkdir -p versions')
        path = f'versions/{archive_name}'
        local(f'tar -cvzf {path} web_static')
        return path
    except Exception:
        return None


def do_deploy(archive_path):
    '''Distribute an archive to our web servers'''

    try:
        if not os.path.isfile(archive_path):
            return False
        file_path = archive_path.split('/')[-1]  # web_static_xxxxxx.tgz
        name = file_path.split('.')[0]  # web_static_xxxxxx
        r_path = '/data/web_static/releases'

        put(archive_path, f'/tmp/{file_path}')
        run(f'mkdir -p {r_path}/{name}/')
        run(f'tar -xzf /tmp/{file_path} -C {r_path}/{name}/')
        run(f'rm /tmp/{file_path}')
        run(f'mv {r_path}/{name}/web_static/* {r_path}/{name}/')
        run(f'rm -rf {r_path}/{name}/web_static')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {r_path}/{name}/ /data/web_static/current')
        print('New version deployed!')
        return True
    except Exception as e:
        return False
