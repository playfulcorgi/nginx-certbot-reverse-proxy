from subprocess import check_output
from printSubprocessStdout import printSubprocessStdout
from shlex import quote

def generate():
	envFilePath = '/root/.env'
	printSubprocessStdout(
		check_output('env > {}'.format(quote(envFilePath)), shell=True))
