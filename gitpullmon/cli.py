import argparse
import shlex
import subprocess
import sys

from git import Repo, Remote, Reference, Commit

def has_new_commit(repo_path, branch_name, remote_name)->bool:
    repo = Repo(repo_path)
    master:Reference = repo.heads[branch_name]
    cur_commit = master.commit
    print(f'Current commit in {branch_name} branch: {cur_commit}')

    origin: Remote = repo.remotes[remote_name]
    print(f'Refreshing the repository remote: {remote_name}, {list(origin.urls)[0]}')
    origin.pull()
    
    last_commit = master.commit
    print(f'Latest commit in the {remote_name}/{branch_name}: {last_commit}')
    
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
    p.add_argument('-d', '--repository', default='.')
    p.add_argument('-b', '--branch-name', default='master')
    p.add_argument('-r', '--remote-name', default='origin')
    args = p.parse_args()


    if has_new_commit(args.repository, args.branch_name, args.remote_name):
        print(f'Repository changed, executing command: {args.command}')
        execute_command(args.command)
    else:
        print('Nothing changed')
    