import sys
from printSubprocessStdout import printSubprocessStdout

def livePrintStdout(process, colors=True):
    for line in process.stdout:
        printSubprocessStdout(line, colors)
        sys.stdout.flush()
    print('Quitting subprocess.')
    process.wait()
    code = process.returncode
    if code != 0:
        raise Exception('Subprocess returned non-zero exit code ({}).'.format(code))