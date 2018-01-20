import os, re, glob, sys, argparse
from string import Template

class Braced(Template):
    pattern = r"""
    %(delim)s{(?P<braced>%(id)s)} |
    (?P<escaped>^$) |
    (?P<named>^$) |
    (?P<invalid>^$)
    """ % dict(delim=re.escape(Template.delimiter), id=Template.idpattern)

def regen():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-certs-yet', action='store_true', dest='noCertsYet')
    args = parser.parse_args()
    noCertsAvailableYet = args.noCertsYet

    print('Converting NGINX config template into regular config file by providing environment variables.')
    templates = glob.glob('/etc/nginx/**/*.template.conf', recursive=True)
    for templatePath in templates:
        confOutputPath = templatePath[:-len('.template.conf')] + '.conf'
        print('Updating {} from template.'.format(confOutputPath))
        filein = open(templatePath)
        src = Braced(filein.read())
        configPath = os.environ['NGINX_CONFIG_DIRECTORY'] + '/' + os.environ['NGINX_CONFIG_FILENAME']
        certbotChallengeDirectory = os.environ['CERTBOT_CHALLENGE_DIRECTORY']
        mapping = dict(
            userConfigInclude='include {};'.format(configPath) if not noCertsAvailableYet else '',
            certbotChallengeDirectory=certbotChallengeDirectory,
            certs='/etc/letsencrypt/live'
        )
        outString = src.substitute(mapping)
        fileout = open(confOutputPath, 'w')
        fileout.write(outString)
        fileout.close()
        sys.stdout.flush()
