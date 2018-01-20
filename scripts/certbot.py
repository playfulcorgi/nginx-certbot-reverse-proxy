from livePrintStdout import livePrintStdout
from subprocess import Popen, PIPE, STDOUT

def relative(subpath='', useCwd=False):
	import os
	basePath = os.getcwd() if useCwd else os.path.dirname(os.path.abspath(__file__))
	return os.path.normpath(os.path.join(basePath, os.path.expanduser(subpath)))

def run(email, challengeDirectory, domains, test = True, reloadNginx = True, colors = True):
    certbotCommand = [
        '/usr/bin/certbot', 'certonly',
        '-n', # --non-interactive
        '--agree-tos',
        '--renew-with-new-domains',
        '--keep-until-expiring',
        '-m', email,
        '--webroot',
        '-w', challengeDirectory
    ]
    if reloadNginx:
        print('After new certs are downloaded, Certbot will reload NGINX configuration.')
        certbotCommand.extend(['--deploy-hook', relative('server/reloadServer')])
    for domain in domains:
        certbotCommand.append('-d')
        certbotCommand.append(domain)
    if test:
        print('CERTBOT_STAGING is not False. Certbot will download and use test certificates instead of real ones for specified domains. To have Certbot download actual certificates for domains provided, set test=False.')
        certbotCommand.append('--test-cert')
    print('Running Certbot with provided configuration and using NGINX to serve the ACME challenge.')
    livePrintStdout(
        process=Popen(certbotCommand, stdout=PIPE, stderr=STDOUT), 
        colors=colors
    )
    print('Certbot call finished without errors.')