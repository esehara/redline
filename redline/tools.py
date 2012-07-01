# -*- coding: utf-8 -*-

def put(url,xml):
    request(url,'PUT',xml)

def post(url,xml):
    request(url,'POST',xml)

def request(url,method='GET',data=''):
    import urllib2
    request = urllib2.Request(url,data=data)
    request.add_header('Content-Type','text/xml')
    request.get_method = lambda: method
    try:
        response = urllib2.urlopen(request)
        body = response.read()
    except urllib2.HTTPError,e:
        if not (200 <= e.code < 300): raise
    return body

def load_configure(filepath=None):
    """
    Read Configure File.If filepath is exist,this function use this,but None Type, it reads home directory.
    """
    import yaml
    if filepath is None:
        import os
        if not os.path.isfile(os.environ.get("HOME") + "/.redline"):
            print("oh,redline configure is not find.I guess, you use -I Option and Initialize ;) ")
            exit()
        filepath = os.environ.get("HOME") + "/.redline"
    configure_file = open(filepath)
    return yaml.load(configure_file.read())

def initialize(cmd,opt):
    """
    Make Configure File (YAML type) in Home Directory.
    """
    import os
    if os.environ.get("HOME") == None:
        print("Oh... Environment Valiable 'HOME' isn't found :( You set Home directory :D !")
        exit()
    home_dir = os.environ.get("HOME")
    if (os.path.isfile(os.environ.get("HOME") + "/.redline")
        and cmd.filepath is None):
        print("""Oops!! Configure is already exist :(
If you make new configure file,use option "-f" or "file" """)
        exit()
    print("OK,I make configure file :D !!")
    
    if cmd.filepath is not None:
        init_file = open(cmd.filepath,"w")
    else:
        init_file = open(home_dir + "/.redline","w")
    init_file.write("""
URL: http://hogehoge.com/
API_KEY: Write your redmine API_KEY :) If not use, delete it.
TEMPLATE: Write your template file path :) If not use, delete it.
    """)
    init_file.close()
    print("Happy !! your configure file is -> " + home_dir + "/.redline")

if __name__ == "__main__":
    initialize()
    print(load_configure())
