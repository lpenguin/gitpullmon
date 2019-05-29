import argparse
import shlex
import subprocess
import sys

from git import Repo, Remote, Reference, Commit

def has_new_commit(repo_path: str='.')->bool:
    repo = Repo(repo_path)
    master:Reference = repo.heads.master
    cur_commit = master.commit

    origin: Remote = repo.remotes.origin
    origin.pull()
    
    last_commit = master.commit
    return last_commit != cur_commit

def execute_command(command: str):
    command_args = shlex.split(command)
    subprocess.call(command_args, 
        stdin=sys.stdin, 
        stdout=sys.stdout, 
        stderr=sys.stderr)
    
def main():
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--command', 
        help='Command to run on new commit', required=True)
    p.add_argument('-r', '--repository', default='.')
    args = p.parse_args()


    if has_new_commit(args.repository):
        print(f'Repository changed, executing command: {args.command}')
        execute_command(args.command)
    else:
        print('Nothing changed')
    