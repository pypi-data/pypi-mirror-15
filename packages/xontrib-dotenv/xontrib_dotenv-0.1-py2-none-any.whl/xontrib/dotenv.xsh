import os
import builtins

def _dotenv():
    dirs = $PWD.split('/')

    env = None

    for d in reversed(range(len(dirs))):
        dir = dirs[:d + 1]
        dir.append('.env')

        env = '/' + os.path.join(*dir)

        if os.path.exists(env):
            break
        else:
            env = None

    if (not env or env != builtins.__xonsh_env__.get('DOTENV')) and builtins.__xonsh_env__.get('DOTENV_OLD'):
        for k, v in builtins.__xonsh_env__.get('DOTENV_OLD'):
            if not v:
                del builtins.__xonsh_env__[k]
            else:
                builtins.__xonsh_env__[k] = v
        $DOTENV_OLD = []

    if env and env != builtins.__xonsh_env__.get('DOTENV'):
        $DOTENV_OLD = []
        with open(env, 'r') as fh:
            for line in fh.readlines():
                line = line.strip()
                if len(line) > 0:
                    k, v = line.split('=', 1)
                    $DOTENV_OLD.append((k, builtins.__xonsh_env__.get(k)))
                    builtins.__xonsh_env__[k] = v

    $DOTENV = env

    return ''

$FORMATTER_DICT['dotenv'] = _dotenv
