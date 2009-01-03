#! /usr/bin/env python
# encoding: utf-8

import os
import intltool, gnome

API_VERSION = '1.0'

# the following two variables are used by the target "waf dist"
VERSION = '0.0.1'
if os.path.exists('.bzr'):
    try:
        from bzrlib.branch import Branch
        branch = Branch.open_containing('.')[0]
        revno = branch.revno()
        parent_url = branch.get_parent()
        if parent_url is None:
            # use the nick instead
            branch_name = branch.nick
        else:
            if parent_url[-1] == '/':
                parent_url = parent_url[:-1]
            branch_name = os.path.basename(parent_url)
        VERSION += '-bzr%d-%s' % (revno, branch_name)
    except ImportError:
        pass

APPNAME = 'libdesktop-agnostic'

# these variables are mandatory ('/' are converted automatically)
srcdir = '.'
blddir = 'build'

config_backend = None

def set_options(opt):
    [opt.tool_options(x) for x in ['compiler_cc', 'gnome']]
    opt.sub_options('libdesktop-agnostic')
    opt.add_option('--enable-debug', action='store_true',
                   dest='debug', default=False,
                   help='Enables the library to be built with debug symbols.')

def configure(conf):
    print 'Configuring %s %s' % (APPNAME, VERSION)

    import Options
    if len(Options.options.config_backends) == 0:
        conf.fatal('At least one configuration backend needs to be built.')
    conf.env['BACKENDS_CFG'] = Options.options.config_backends.split(',')

    conf.env['DEBUG'] = Options.options.debug

    conf.check_tool('compiler_cc misc gnome vala')
    conf.check_tool('intltool')

    conf.check_cfg(package='gmodule-2.0', uselib_store='GMODULE',
                   atleast_version='2.6.0', mandatory=True,
                   args='--cflags --libs')
    conf.check_cfg(package='gobject-2.0', uselib_store='GOBJECT',
                   mandatory=True, args='--cflags --libs')
    # Needed for the Color class
    conf.check_cfg(package='gdk-2.0', uselib_store='GDK', mandatory=True,
                   args='--cflags --libs')
    conf.check_cfg(package='vala-1.0', uselib_store='VALA',
                   atleast_version='0.5.3', mandatory=True,
                   args='--cflags --libs')
    if 'gconf' in conf.env['BACKENDS_CFG']:
        conf.check_cfg(package='gconf-2.0', uselib_store='GCONF',
                       mandatory=True, args='--cflags --libs')

    conf.define('API_VERSION', str(API_VERSION))
    conf.define('VERSION', str(VERSION))
    conf.define('GETTEXT_PACKAGE', APPNAME + '-1.0')
    conf.define('PACKAGE', APPNAME)
    
    if conf.env['DEBUG']:
        conf.env.append_value('VALAFLAGS', '-g')
        conf.env.append_value('CCFLAGS', '-ggdb')

    conf.env.append_value('CCFLAGS', '-DHAVE_CONFIG_H')

    conf.write_config_header('config.h')

def build(bld):
    # process subfolders from here
    bld.add_subdirs('libdesktop-agnostic data')

#    if bld.env['INTLTOOL']:
#        bld.add_subdirs('po')