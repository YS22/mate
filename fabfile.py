from fabric.api import *
env.hosts =['47.93.103.136']
env.user = 'root'
env.password ='1234pttK'

def deploy ():
	with cd('/srv/mate'):
		run('git pull')
		run('supervisorctl restart mate')
		run('/supervisorctl status')