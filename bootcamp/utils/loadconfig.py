import os
import ConfigParser

def readconf():
    config = ConfigParser.ConfigParser()
    config.read('/etc/netaut.conf')
    return config


def project_path(type):
    config = readconf()
    if type == 'project':
        path = config.get('paths', 'project_path')
    elif type == 'play':
        path = config.get('paths', 'project_path')
    elif type == 'resultout':
        path = config.get('paths', 'result_path')
    return os.listdir(path)

def get_path(type):
    config = readconf()
    if type == 'project':
        path = config.get('paths', 'project_path')
    elif type == 'play':
        path = config.get('paths', 'project_path')
    elif type == 'resultout':
        path = config.get('paths', 'result_path')
    elif type == 'baseurl':
        path = config.get('paths', 'baseurl')
    return path