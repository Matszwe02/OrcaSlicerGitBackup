import subprocess
from datetime import datetime
import os
import traceback

cwd = os.path.dirname(os.path.abspath(__file__))


def log(msg):
    with open(os.path.join(cwd, 'git.log'), 'a') as f:
        f.write(datetime.now().strftime(f"%d/%m/%Y, %H:%M:%S | {msg}\n"))
        print(msg)


status = subprocess.check_output('git status', cwd=cwd).decode()


if '(use "git push" to publish your local commits)' in status:
    push = subprocess.check_output('git push', cwd=cwd).decode()
    log(push)
    exit()


if "Your branch is up to date with" not in status:
    
    pull = subprocess.check_output('git pull', cwd=cwd).decode()
    log(pull)
    exit()


if "nothing to commit, working tree clean" not in status:
    
    msg = datetime.now().strftime("Update %d/%m/%Y, %H:%M:%S")
    try:
        diff = subprocess.check_output(f'git diff', cwd=cwd).decode()
        changes = []
        changes_raw = []
        for line in diff.splitlines():
            if line[0] in '+-':
                if line.__contains__('":'):
                    line = line[line.index('"'):]
                    if line.removesuffix(',') in changes_raw:
                        changes_raw.remove(line.removesuffix(','))
                        print(line)
                    else:
                        changes_raw.append(line.removesuffix(','))
        
        
        for change in changes_raw:
            index1 = change.index('"')
            index2 = change.index('"', index1 + 1)
            changes.append(change[index1 + 1 : index2].removesuffix(','))
        
        changes = list(set(changes))
        log('changes: ' + ', '.join(changes))
        if changes.__len__() in range(1,5):
            msg = "Update " + ', '.join(changes)
    except Exception: log(traceback.format_exc())
    commit = subprocess.check_output(f'git commit -a -m "{msg}"', cwd=cwd).decode()
    
    log(commit)
    
    push = subprocess.check_output('git push', cwd=cwd).decode()

    log(push)
    exit()
    
log(status)