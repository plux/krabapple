import os
import sys
import ConfigParser

from bottle import run, get, view, route, static_file

#-----------------------------------------------------------------------------
# Config

# Make proper config handling here instead..
if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    # This will crash if default.conf doesn't exist
    config_file = 'default.conf'
config = ConfigParser.ConfigParser()
config.read(config_file)

ROOT_PATH = os.path.expanduser(config.get('general', 'root_path'))
HOST      = config.get('general', 'host')
PORT      = config.get('general', 'port')
CALLBACKS = {}

#-----------------------------------------------------------------------------
# GET request handlers


@get('/hello/:name')
def index(name='W'):
    return '<b>Hello %s!</b>' % name

@get('/list/:path#.+#')
def list(path=''):
    path    = os.path.join(ROOT_PATH, path)
    content = [file_info(path, f) for f in os.listdir(path) if is_visible(f)]
    return { "path"   : path
           , "content": content
           }
#-----------------------------------------------------------------------------
# Callbacks

def register_callbacks():
    global CALLBACKS
    CALLBACKS = {"file_info": [cb_file_info]}

def cb_file_info(data):
    if os.path.isfile(data['path']):
        data['ext'] = os.path.splitext(data['path'])[1]
    return data

def callbacks(call, data):
    for callback in CALLBACKS[call]:
        data = callback(data)
    return data

#-----------------------------------------------------------------------------
# Helpers

def is_visible(f):
    return not f.startswith(".")

def file_info(dir_path, f):
    path = os.path.join(dir_path, f)
    relative_path = os.path.relpath(path, ROOT_PATH)
    data = { "name"     : os.path.basename(path)
           , "path"     : path
           , "type"     : get_type(path)
           , "rel_path" : relative_path
           }
    return callbacks('file_info', data)

def get_type(path):
    if os.path.isfile(path):
        return "file"
    elif os.path.isdir(path):
        return "directory"
    else:
        return "unknown"

#-----------------------------------------------------------------------------
# Main

def main():
    register_callbacks()
    run(reloader=True, host=HOST, port=PORT)

main()
