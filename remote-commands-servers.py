#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2017 DennyZhang.com
## Licensed under MIT
##   https://raw.githubusercontent.com/DennyZhang/devops_public/master/LICENSE
##
## File : remote-commands-servers.py
## Author : Denny <contact@dennyzhang.com>
## Description :
## --
## Created : <2017-09-05>
## Updated: Time-stamp: <2017-09-07 16:58:58>
##-------------------------------------------------------------------
import sys
import paramiko
import argparse

def remote_commands_servers(server_list, executor_count, avoid_abort, command_list, ssh_parameter_list):
    print("Run remote commands: %s" % (command_list))
    # TODO: implement this logic
    for server in server_list:
        [ip, port] = server
        (status, detail) = run_remote_ssh(ip, port, command_list, ssh_parameter_list)
        print("status: %s, Detail:\n%s" % (status, detail))

################################################################################
def get_ssh_server_list(server_list):
    l = []
    for line in server_list.split(','):
        line = line.strip()
        if line == '' or line.startswith('#') is True:
            continue
        # TODO: error handling
        [ip, port] = line.split(':')
        port = int(port)
        l.append([ip, port])
    return l

def run_remote_ssh(ip, port, ssh_command, ssh_parameter_list):
    [ssh_username, ssh_key_file, key_passphrase] = ssh_parameter_list
    print("Run ssh command in %s:%d" % (ip, port))
    import logging
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    output = ""
    info_dict = {}
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file(ssh_key_file, password=key_passphrase)
        ssh.connect(ip, username=ssh_username, port=port, pkey=key)
        # TODO: trap exit code and report it
        stdin, stdout, stderr = ssh.exec_command(ssh_command)
        stdout_str = "\n".join(stdout.readlines())
        stderr_str = "\n".join(stderr.readlines())
        ssh.close()
        return ("OK", "stdout: %s\nstderr: %s" % (stdout_str, stderr_str))
    except:
        return ("ERROR", "Unexpected on server: %s error: %s" % (ip, sys.exc_info()[0]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--server_list', required=True, \
                        help="A list of ip-port. Separated by comma.", type=str)
    parser.add_argument('--command_list', required=True, \
                        help="A list of commands to run", type=str)
    parser.add_argument('--executor_count', default=1, \
                        help="How many concurrent executors to run. Default value is 1.", type=int)
    parser.add_argument('--ssh_username', default="root", \
                        help="SSH username", type=str)
    parser.add_argument('--ssh_key_file', required=True, \
                        help="SSH private key file. Here we assume the same key file works for all servers.", type=str)
    parser.add_argument('--key_passphrase', default="", \
                        help="Key passphrase for SSH private key file. If not given, key file is assumed unencrypted.", \
                        type=str)
    parser.add_argument('--avoid_abort', dest='avoid_abort', action='store_true', default=False, \
                        help="Whether to avoid abort. By default, any node failure will abort the whole process")
    l = parser.parse_args()

    server_list = get_ssh_server_list(l.server_list)
    # TODO: get return code
    ssh_parameter_list = [l.ssh_username, l.ssh_key_file, l.key_passphrase]
    remote_commands_servers(server_list, l.executor_count, l.avoid_abort, l.command_list, ssh_parameter_list)
## File : remote-commands-servers.py ends
