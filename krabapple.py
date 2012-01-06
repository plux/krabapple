from bottle import get, route, run, request
import sys
import os

ROOT_PATH = "/Users/hakan.nilsson/Music/Library/"
CALLBACKS = {}

###---------------------------------------------------------------------------
### GET request handlers

@get('/hello/:name')
def index(name='W'):
    return '<b>Hello %s!</b>' % name

@get('/list/:path#.+#')
def list(path=''):
    path    = os.path.join(ROOT_PATH, path)
    content = [file_info(path, f) for f in os.listdir(path) if is_visible(f)]
    return {"path"   : path,
            "content": content}

###---------------------------------------------------------------------------
### Callbacks
def register_callbacks():
    global CALLBACKS
    CALLBACKS = {"file_info": [cb_file_info]}

def cb_file_info(data):
    if os.path.isfile(data['path']):
        data['ext'] = os.path.splitext(data['path'])[1]
    return data

###---------------------------------------------------------------------------
### Helpers
def is_visible(f):
    return not f.startswith(".")
        
def file_info(dir_path, f):
    path = os.path.join(dir_path, f)
    relative_path = os.path.relpath(path, ROOT_PATH)
    file_info = {
                   "path"     : path,
                   "name"     : os.path.basename(path),
            #           "ext"      : os.path.splitext(path)[1],
            #           "type"     : get_type(path),
            #           "rel_path" : relative_path
        }
    return callbacks('file_info', file_info)

def callbacks(call, data):
    for callback in CALLBACKS[call]:
        data = callback(data)
    return data

def get_type(path):
    if os.path.isfile(path):
        return "file"
    elif os.path.isdir(path):
        return "directory"
    else:
        return "unknown"

register_callbacks()
run(reloader=True, host='localhost', port=8080)
