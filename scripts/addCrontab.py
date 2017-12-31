import tempfile, os
from subprocess import check_output, PIPE, Popen, STDOUT
from printSubprocessStdout import printSubprocessStdout
from shlex import quote

def add(newEntry):
    print('Trying to save entry {} to crontab.'.format(newEntry))
    fd, path = tempfile.mkstemp()
    process = Popen('crontab -l > ' + quote(path), stdout=PIPE, stderr=PIPE, shell=True)
    out, err = process.communicate()
    printSubprocessStdout(out)
    printSubprocessStdout(err)
    code = process.returncode
    if code != 0 and code != 1:
        raise Exception(
            'Unrecognized issue when reading existing crontab entries (code {}).'.format(code))
    with open(path, 'a') as f:
        f.write(newEntry)
        f.write('\n')
    process = Popen('crontab ' + quote(path), stdout=PIPE, stderr=PIPE, shell=True) # Array form of Popen cannot be used here, a direct call to load new crontab was needed.
    out, err = process.communicate()
    printSubprocessStdout(out)
    printSubprocessStdout(err)
    code = process.returncode
    if code != 0:
        raise Exception('Cannot save new cron job.')
    print('New cron entry saved.')
    os.remove(path)
    print('Making sure rsyslog is running for logging. If not, it will be started.')
    printSubprocessStdout(
        check_output('service rsyslog status || service rsyslog start', shell=True))
    print('Making sure cron service is running. If not, it will be started.')
    printSubprocessStdout(
        check_output('service cron status || service cron start', shell=True))
