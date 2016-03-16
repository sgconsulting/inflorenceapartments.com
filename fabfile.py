from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ["root@www1.sgconsulting.it:32"]
env.base_dir = '/home/httpd/'
env.project_name = 'inflorenceapartments.com'
env.path = env.base_dir+env.project_name

def service_restart(service):
    run("/etc/init.d/%s restart" % service)

def service_reload(service):
    run("/etc/init.d/%s reload" % service)

def deploy():
    with settings(warn_only=True):
        if run("test -d %s" % env.path).failed:
            #get code from git repository
            sudo("git clone git@git02.sgconsulting.it:sgconsulting/%s.git %s" % (env.project_name, env.path), user="sgcons", pty=True)
            #config nginx
            run("nginx_tmpl.sh %s" % env.project_name)
            #reload nginx
            service_reload('nginx')
        else:
            with cd(env.path):
                sudo("git pull", user="sgcons", pty=True)
