#!/usr/bin/python3
'''
Fabric script that generates a .tgz archive from the contents of the
web_static folder of our AirBnB Clone repo, using the function do_pack
'''
from fabric.api import local
from datetime import datetime


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
