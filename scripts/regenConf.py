#!/usr/bin/env python
from string import Template
import os
import re
import glob

class Braced(Template):
    pattern = r"""
    %(delim)s{(?P<braced>%(id)s)} |
    (?P<escaped>^$) |
    (?P<named>^$) |
    (?P<invalid>^$)
    """ % dict(delim=re.escape(Template.delimiter), id=Template.idpattern)

def regen():
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
            configPath=configPath,
            certbotChallengeDirectory=certbotChallengeDirectory
        )
        outString = src.substitute(mapping)
        fileout = open(confOutputPath, 'w')
        fileout.write(outString)
        fileout.close()
