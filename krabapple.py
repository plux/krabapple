import os
import sys
import ConfigParser
import time
import mimetypes

from bottle import run, get, view, route, static_file, HTTPError, response

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

ROOT_PATH    = os.path.expanduser(config.get('general', 'root_path'))
HOST         = config.get('general', 'host')
PORT         = config.get('general', 'port')
MAX_VISIBLE  = config.getint('view', 'max_visible')
CALLBACKS = {}

#-----------------------------------------------------------------------------
# GET request handlers

@get('/')
def index():
    return html_list()

@get('/config.js')
@view('config.js')
def configjs():
    response.content_type = 'text/js'
    return {'max_visible': MAX_VISIBLE}

@get('/dynamic_style.css')
@view('dynamic_style.css.tpl')
def dynamic_style():
    response.content_type = 'text/css'
    return {'width': (100/MAX_VISIBLE)-1}


@get('/list/:path#.*#')
@view('index')
def html_list(path=''):
    return {"path" : path}

@get('/json/list/:path#.*#')
def json_list(path=''):
    path    = os.path.join(ROOT_PATH, path)
    if not os.path.exists(path):
        raise HTTPError(404, "Path doesn't exist") # Not found
    if not os.path.isdir(path):
        raise HTTPError(403, "Path is not a directory") # Forbidden
    time.sleep(0.3)
    files   = os.listdir(path)
    content = [file_info(path, f) for f in files if is_visible(f)]
    content.sort(key=file_cmp_key)
    return {"content": content}

@get('/file/:path#.+#')
def get_file(path):
    real_path = os.path.join(ROOT_PATH, path)
    print real_path
    if not os.path.exists(real_path):
        raise HTTPError(404, "File doesn't exist") # Not found
    if not os.path.isfile(real_path):
        raise HTTPError(403, "Not a file") # Forbidden
    filename = os.path.basename(path)
    return static_file(path, root=ROOT_PATH, download=filename)


@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='static')

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
    data = callbacks('file_info', data)
    del data['path']
    return data

def get_type(path):
    if os.path.isfile(path):
        return "file"
    elif os.path.isdir(path):
        return "directory"
    else:
        return "unknown"

def file_cmp_key(f):
    return (f['type'], f['name'])

def register_mimetypes():
    # TODO: Read mimetypes from config
    custom_types = [('txt/x-nfo', '.nfo')]
    for (mimetype, ext) in custom_types:
        mimetypes.add_type(mimetype, ext)

#-----------------------------------------------------------------------------
# Main

def main():
    register_callbacks()
    register_mimetypes()
    mimetypes.add_type("text/x-nfo", ".nfo")
    run(reloader=True, host=HOST, port=PORT)

main()
