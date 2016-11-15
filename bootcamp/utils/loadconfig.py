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

def get_vars(type):
    config = readconf()
    if type == 'project':
        vars = config.get('prod', 'project_path')
    elif type == 'play':
        vars = config.get('prod', 'project_path')
    elif type == 'resultout':
        vars = config.get('prod', 'result_path')
    elif type == 'baseurl':
        vars = config.get('prod', 'baseurl')
    elif type == 'ansibengineemc':
        vars = config.get('prod', 'ansibengineemc')
    elif type == 'ansibenginemtn':
        vars = config.get('prod', 'ansibenginemtn')
####stage env
    if type == 'project':
        vars = config.get('stage', 'project_path')
    elif type == 'play':
        vars = config.get('stage', 'project_path')
    elif type == 'resultout':
        vars = config.get('stage', 'result_path')
    elif type == 'baseurl':
        vars = config.get('stage', 'baseurl')
    elif type == 'ansibengineemc':
        vars = config.get('stage', 'ansibengineemc')
    elif type == 'ansibenginemtn':
        vars = config.get('stage', 'ansibenginemtn')
    return vars