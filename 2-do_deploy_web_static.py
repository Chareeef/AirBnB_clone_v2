#!/usr/bin/python3
'''
Fabric tasks to deploy web_static on our servers
'''
from fabric.api import local, run, put, env
from datetime import datetime

env.hosts = ['52.91.178.165', 'ubuntu@18.206.198.119']


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
        put(archive_path, '/tmp/')
        file_without_tgz = archive_path.split('.')[0].split('/')[-1]
        remote_path = '/tmp/' + archive_path.split('/')[-1]
        decompressed_path = f'/data/web_static/releases/{file_without_tgz}'
        run('mkdir -p {}'.format(decompressed_path))
        run('tar -xzf {} -C {}/'.format(remote_path, decompressed_path))
        run('rm -f {}'.format(remote_path))
        run(f'ln -sf {decompressed_path} /data/web_static/current')
        return True
    except Exception as e:
        print(e)
        return False
