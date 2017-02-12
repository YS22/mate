from fabric.api import *
env.hosts =['162.243.128.84']
env.user = 'root'
env.password ='1234pttk'

def deploy ():
	with cd('/srv/ysweb/mate'):
		run('git pull')
		run('../bin/supervisorctl restart mate')
		run('../bin/supervisorctl status')