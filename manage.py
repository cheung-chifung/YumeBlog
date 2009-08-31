#!/usr/bin/python
#-*-coding:UTF-8-*-#
import sys, os

#USE YOUR CUSTOM PATH FOR YUMEBLOG AND RELATED LIBs
pathAdd = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(pathAdd,'libs'))
sys.path.insert(0,os.path.join(pathAdd,'libs','utils'))
sys.path.insert(0,os.path.join(pathAdd,'myblog'))

os.chdir(pathAdd)

from django.core.management import execute_manager
try:
    #USE YOUR OWN INSTANCE SETTINGS
    import myblog.settings
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    #USE YOUR OWN INSTANCE SETTINGS
    execute_manager(myblog.settings)
