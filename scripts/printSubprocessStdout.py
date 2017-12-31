def printSubprocessStdout(message, colors=True):
    if colors:
        print('\033[92m' + message.decode() + '\033[0m', end='')
    else:
        print('Subprocess: ' + message.decode(), end='')