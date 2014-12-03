"""Fab file for the blog project (install on Vex.net)"""
from fabric.api import *
from fabric.contrib import project
from fabric.contrib.files import exists
import os, glob, datetime, subprocess
env.user = 'mcfletch'
env.product = 'webtoys'
env.product_dir = os.path.join('/opt',env.product,'current' )
env.virtual_env = os.path.join(env.product_dir,'env' )
env.django_admin = 'DJANGO_SETTINGS_MODULE=webtoys.settings '+ os.path.join( env.virtual_env,'bin','django-admin.py' )
ssh_key = os.path.expanduser( os.path.join( '~', '.copytohosts', '.ssh','authorized_keys' ))

HERE = os.path.dirname( __file__ )
REQUIREMENTS_FILE = os.path.join( HERE, 'requirements.txt' )
ETC_SOURCE = os.path.join( HERE, 'etc' )
VAR_SOURCE = os.path.join( HERE, 'var' )
OPT_SOURCE = os.path.join( HERE, 'opt' )
HOME_SOURCE = os.path.join( HERE, 'home', env.user )

DEPENDENCIES = [
    'supervisor',
    'nginx',
    'libpq-dev', 
    'python-dev', 
    'python-psycopg2', 
    'python-virtualenv',
    'python-psycopg2',
    'python-imaging',
    'python-tz',
    'openjdk-7-jre-headless', # webassets requirement...
    'libav-tools', 
    'espeak', 
    'git',
]
def find_dist( name ):
    """Find the full path of the latest sdist of name"""
    package_dir = os.path.dirname( __import__( name ).__file__ )
    return find_setup( package_dir )

def find_setup( package_dir ):
    """Find setup.py file in the parents of package_dir"""
    while package_dir:
        packer = os.path.join( package_dir, 'setup.py' )
        if os.path.exists( packer ):
            return package_dir
        new_package_dir = os.path.dirname( package_dir )
        if new_package_dir == package_dir:
            break
        package_dir = new_package_dir
    raise RuntimeError( "Unable to find package for %s"%( package_dir, ))

def forceinstall( source ):
    """Force install given project source into environment"""
    virtual_env = env.virtual_env
    filename = upload_project( find_dist(source) )
    sudo( '%(virtual_env)s/bin/pip install --force -I --no-deps %(filename)s'%locals() )

WEBTOYS = find_dist( 'webtoys' )
TOYS = find_dist('toys')

PROJECT_SOURCES = [
    WEBTOYS,
    TOYS,
]

def empty_virtualenv( 
    environment, 
    need_system_flag=True, pip_params=''
):
    with cd( '~%s'%(env.user,) ):
        with settings( warn_only = True ):
            if not exists( environment ):
                sudo( 'mkdir -p %s'%(os.path.dirname(environment)))
                if need_system_flag:
                    need_system_flag = '--system-site-packages'
                else:
                    need_system_flag = ''
                sudo( 'virtualenv %s %s'%( need_system_flag, environment,) )

def virtualenv(
    environment, project_sources, pips, 
    need_system_flag=True, pip_params='',
):
    """Create a virtual environment at environment with pips and project_sources installed"""
    empty_virtualenv( environment=environment, need_system_flag=need_system_flag, pip_params=pip_params )
    packages = 'file:///home/%s/packages'%( env.user, )
    sudo( '%(environment)s/bin/pip install --no-index --find-links=%(packages)s %(pip_params)s "setuptools==2.1"'%locals() )
    sudo( '%(environment)s/bin/pip install --no-index --find-links=%(packages)s %(pip_params)s "pip==1.3"'%locals() )
    if pips:
        if not isinstance( pips, (list,tuple)):
            raise RuntimeError( "Please use list form" )
        source_pips = [x for x in pips if x.startswith( 'git+' )]
        package_pips = [x for x in pips if not x.startswith( 'git+' )]
        for set,extra_params in [
            (source_pips,''),
            (package_pips,'--no-index --find-links=%(packages)s'%locals())
        ]:
            set = ' '.join( [repr(x) for x in set] )
            sudo( 'PIP_DOWNLOAD_CACHE=~/.pip-cache %(environment)s/bin/pip install %(extra_params)s %(pip_params)s %(set)s'%locals() )
    for project_source in project_sources:
        filename = upload_project( project_source )
        sudo( '%(environment)s/bin/pip install --no-deps %(filename)s'%locals() )

def upload_project( project_source ):
    """Find the setup.py, build the package, copy and install"""
    subprocess.check_call( 
        'cd %(project_source)s && python setup.py sdist develop'%locals(), 
        shell=True, 
    )
    files = glob.glob( os.path.join( project_source, 'dist', '*.tar.gz' ))
    files.sort( key = lambda f: os.stat( f ).st_ctime )
    current = files[-1]
    base = os.path.basename( current )
    run( 'mkdir -p ~/tmp' )
    file = os.path.join( '~/tmp', base )
    put( current, file )
    return file

def django_command( command, *args ):
    environment = env.virtual_env
    admin = env.django_admin
    command = '%(admin)s %(command)s '%locals()
    command+= " ".join( [str(x) for x in args])
    return command
def django_admin( command, *args ):
    run( django_command( command, *args ) )
def django_sudo( command, *args ):
    sudo( django_command( command, *args ) )

def apt_update():
    """Update apt repositories"""
    sudo( 'apt-get update' )
    sudo( 'apt-get dist-upgrade --yes' )
    sudo( 'apt-get autoremove --yes' )
def dependencies( dependencies ):
    """Install OS-level dependencies"""
    if isinstance( dependencies, (list,tuple)):
        dependencies = ' '.join( dependencies )
    sudo( 'apt-get install --yes %s'%( dependencies ) )
    sudo( 'apt-get autoremove --yes' )
def ensure_dependencies( update=False ):
    """Ensure our configure .deb dependencies are all installed"""
    if update:
        apt_update()
    dependencies( DEPENDENCIES )

def django_collectstatic( ):
    product = env.product
    with settings( warn_only=True ):
        sudo( 'mkdir -p /opt/%(product)s/current/www/static'%locals())
    django_sudo( 'collectstatic', '--clear', '--noinput' )
    django_sudo( 'assets', 'build', '--parse-templates' )
    sudo('chmod -R go+r /opt/%(product)s/current/www/static'%locals())

def backup_current():
    product = env.product_dir
    user = env.user
    date = datetime.datetime.now().strftime( '%Y-%m-%d-%H-%M' )
    if exists( product ):
        sudo( 'mv %(product)s %(product)s-%(date)s'%locals())
    return backup_db(date)
def backup_db(date=None):
    user = env.user
    if date is None:
        date = datetime.datetime.now().strftime( '%Y-%m-%d-%H-%M' )
    filename = 'backup-%(date)s.sql'%locals()
    sudo( 'pg_dump blog > /tmp/%(filename)s'%locals(), user='postgres' )
    sudo( 'mv /tmp/%(filename)s /home/%(user)s/'%locals() )
    return filename

def initial_install():
    install_ssh_keys()
    ensure_dependencies(update=True)
    with settings( warn_only=True ):
        sudo( 'aptitude remove apache2 apache2-mpm-worker apache2-utils apache2.2-bin apache2.2-common' )
        sudo( '/etc/init.d/rng-tools restart' )
    initial_db()
    upgrade_pips()
    install()
def initial_db():
    sudo( 'createdb -O mcfletch --locale=en_CA.utf8 -E utf8 -T template0 webtoys', user='postgres' )

def update():
    install()

def install():
    with settings( warn_only=True):
        sudo('rm -rf %s'%(env.virtual_env,))
#    with settings( warn_only=True ):
#        sudo( '/etc/init.d/supervisor stop' )
#        sudo( '/etc/init.d/nginx stop' )
    venv = env.virtual_env
    
    virtualenv( 
        venv,
        PROJECT_SOURCES,
        pips = env.pips,
    )
    
    install_templates()
    
    django_admin( 'syncdb' )
    django_admin( 'migrate' )
    django_collectstatic()
#    restart_servers()
    
def install_templates( ):
#    install_su( ETC_SOURCE, '/etc/' )
#    install_su( VAR_SOURCE, '/var/', owner=env.user )
#    install_su( OPT_SOURCE, '/opt/', owner=env.user )
#    install_su( HOME_SOURCE, '/home/%s'%(env.user), owner=env.user )
    pass
def restart_servers():
    with settings( warn_only=True ):
        sudo( '/etc/init.d/supervisor stop' )
        sudo( '/etc/init.d/nginx stop' )
    sudo( '/etc/init.d/nginx start' )
    sudo( '/etc/init.d/supervisor start' )
    
def install_su(source_dir,target_dir, delete=False, owner='root'):
    """Install source directory into target directory on server"""
    temp = '~%s/tmp/'%( env.user,)
    run( 'mkdir -p %(temp)s'%locals())
    with cd( temp ):
        if delete:
            project.rsync_project( '%(temp)s'%locals(), source_dir, extra_opts='-l --delete-after' )
        else:
            project.rsync_project( '%(temp)s'%locals(), source_dir, extra_opts='-l' )
        base = os.path.basename( source_dir )
        sudo( 'chown -R %(owner)s:%(owner)s %(temp)s%(base)s'%locals() )
        sudo( 'rsync -alv %(temp)s%(base)s/* %(target_dir)s'%locals() )
        # now switch the template back for next time...
        user = env.user
        sudo( 'chown -R %(user)s %(temp)s%(base)s'%locals() )

def upgrade_pips( pips=None ):
    """Pull source code for packages into our package cache"""
    if pips is None:
        pips = env.pips
    environment = env.virtual_env
    if not exists( environment ):
        empty_virtualenv( environment )
    pip_params=''# -M --mirrors=http://b.pypi.python.org' 
    sudo( 'rm -rf ~/packages' )
    sudo( 'mkdir -p ~/packages' )
    if pips:
        pips = [repr(x) for x in pips if not x.startswith( 'git+' )]
        if isinstance( pips, (list,tuple)):
            pips = ' '.join( pips )
        sudo( 'PIP_DOWNLOAD_CACHE=~/.pip-cache %(environment)s/bin/pip install --download=~/packages %(pip_params)s "setuptools==2.1"'%locals() )
        sudo( 'PIP_DOWNLOAD_CACHE=~/.pip-cache %(environment)s/bin/pip install --download=~/packages %(pip_params)s "pip==1.3"'%locals() )
        sudo( 'PIP_DOWNLOAD_CACHE=~/.pip-cache %(environment)s/bin/pip install --download=~/packages %(pip_params)s %(pips)s'%locals() )

def load_requirements( *reqfiles ):
    result = []
    for file in reqfiles:
        for line in open( file ):
            line = line.strip()
            if line.startswith( '#' ):
                continue 
            else:
                if '#' in line:
                    line = line.split('#')[0].strip()
                result.append( line )
    return result 

def rm_virtualenv():
    sudo( 'rm -rf %s'%env.virtual_env, )

env.pips = load_requirements( REQUIREMENTS_FILE )
