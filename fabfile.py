"""
This fabfile automates the creation Django Project. 

1. Create virtual environment with the project name 
2. Activate the virtual environment 
3. Download list of packages and install them 
4. Make `src` directory where the project source will reside 
5. Create new Django project in source directory 
6. Update the settings
"""

try:
    from fabric.api import env, run, local
    from fabric.context_managers import lcd, prefix
except ImportError, e:
    print 'Python Fabric should be installed to use this script'
 
import re, sys, os
 
 
DIRECTORY_NAME_REGEXP = r'^[a-zA-Z_].[\w_-]+$'
SOURCE_DIRECTORY_NAME = 'src'
DJANGO_VERSION = '1.6.2'
PROJECT_NAME = 'sample_django_project'
 
PACKAGES_LIST = [
    'Django=={}'.format(DJANGO_VERSION)
]
 
def create_project_directory():
    if not re.match(DIRECTORY_NAME_REGEXP, PROJECT_NAME):
        print 'Incorrect name. Project names can contain only numbers, letters, dashes ' \
            'and underscores. It should start with letter or underscore.'
        sys.exit()
    else:
        try:
            os.makedirs(PROJECT_NAME)
        except OSError, e:
            print '\n--------------------------------'
            print 'Project Directory already exists'
            print '--------------------------------'
            pass

def create_virtual_env():
    venv_path = os.path.join(PROJECT_NAME, 'bin')
    if not os.path.exists(venv_path):
        local('virtualenv --no-site-packages .')
    else:
        print '\n------------------------'
        print 'virtualenv already setup'
        print '------------------------'

 
def install_packages():
    for package in PACKAGES_LIST:
        local('pip install {}'.format(package))
 
 
def create_django_project():
    django_path = os.path.join(PROJECT_NAME, 'src')
    try:
        os.makedirs(django_path)
        local('python ./bin/django-admin.py startproject {} {}'.format(PROJECT_NAME, SOURCE_DIRECTORY_NAME))
    except OSError, e:
        print '\n---------------------------------------'
        print 'Django Project Directory already exists'
        print '---------------------------------------'
        pass
 
def new_project():
    create_project_directory()
    with lcd(PROJECT_NAME):
        create_virtual_env()
        virtualenv_activate_prefix = os.path.join(os.getcwd(), PROJECT_NAME, 'bin', 'activate')
        with prefix('. {}'.format(virtualenv_activate_prefix)):
            install_packages()
            create_django_project()
            manage_py_path = os.path.join(SOURCE_DIRECTORY_NAME, 'manage.py')
