##############################################################################################
# modules
##############################################################################################

import paramiko
import datetime
from datetime import datetime
import re
import logging
import time


##############################################################################################
# Functions
##############################################################################################

def parse_resp(func):

    # Decorator function to parse th results of each command that is run in the server CLI.


    def inner(*args,**kwargs):

        resp = str(func(*args,**kwargs)).replace("'b'", "").replace("b'", "").replace("\\r\\n", " ").replace("\\r\\n?", " ").split()

        return resp

    return inner


##############################################################################################
# Classes
##############################################################################################

class SSHConnect:

    # Creates an instance of the paramiko.SSHClient() class, and opens an SSH session to the server


    def __init__(self, node, prompt, username, password):
        self.node = node
        self.prompt = prompt
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.node,username=self.username,password=self.password,timeout=60)
        self.conn = self.client.invoke_shell()
        

    def __repr__(self):
        return f'SSHConnect("{self.node}")'

    def __str__(self):
        return f'SSHConnect("{self.node}")'



    def init_connect(self):

        # Method to return the initial prompt after an SSH session is opened.


        logging.debug('## {} - {}.init_connect() -- ENTER'.format(__name__, self))

        try:
            def _init_connect(buffer=''):
                prompt_bolean = False
                output = self.conn.recv(65535)
                buffer += str(output)
                recursion_depth = 1
                max_recursion_depth = 10

                if self.prompt not in buffer and max_recursion_depth <= 10:
                    logging.debug('## {} - {}.init_connect() -- PROMPT == {}'.format(__name__, self, prompt_bolean))
                    recursion_depth += 1
                    return _init_connect(buffer)

                elif self.prompt not in buffer and max_recursion_depth > 10:
                    raise RecursionError('Too many loops.')

                elif self.prompt in buffer:
                    prompt_bolean = True
                    logging.debug('## {} - {}.init_connect() -- PROMPT == {}'.format(__name__, self, prompt_bolean))
                    return prompt_bolean

            return _init_connect()

        except Exception as e:
            logging.debug('## {} - {}.init_connect() -- EXCEPTION == {}'.format(__name__, self, e))
            return e



    def run_cmd(self, cmd):

        # Runs a CLI command on the target server and confirms the return of the prompt before completing.


        logging.debug('## {} - {}.run_cmd() -- ENTER'.format(__name__, self))

        try:
            self.conn.send(cmd + '\n')

            def _run_cmd(buffer=''):
                prompt_bolean = False
                output = self.conn.recv(65535)
                buffer += str(output)
                recursion_depth = 1
                max_recursion_depth = 10

                if self.prompt not in buffer and max_recursion_depth <= 10:
                    logging.debug('## {} - {}.run_cmd("{}") -- PROMPT == {}'.format(__name__, self, cmd, prompt_bolean))
                    recursion_depth += 1
                    return _run_cmd(buffer)

                elif self.prompt not in buffer and max_recursion_depth > 10:
                    raise RecursionError('Too many loops.')

                elif self.prompt in buffer:
                    prompt_bolean = True
                    logging.debug('## {} - {}.run_cmd("{}") -- PROMPT == {}'.format(__name__, self, cmd, prompt_bolean))
                    return buffer

            return _run_cmd()

        except Exception as e:
            logging.debug('## {} - {}.run_cmd("{}") -- EXCEPTION == {}'.format(__name__, self, cmd, e))
            return e



    def run_cmd_wait(self, cmd):

        # Runs a CLI command on the target server and confirms the return of the prompt before completing.


        logging.debug('## {} - {}.run_cmd() -- ENTER'.format(__name__, self))

        try:
            self.conn.send(cmd + '\n')

            time.sleep(2)

            def _run_cmd():
                output = self.conn.recv(65535)
                return output

            return _run_cmd()

        except Exception as e:
            logging.debug('## {} - {}.run_cmd("{}") -- EXCEPTION == {}'.format(__name__, self, cmd, e))
            return e



    def close_ssh(self):

        # Closes the SSH connection to the target server.


        self.client.close()
        logging.debug('## {} - {}.close_ssh()'.format(__name__, self))


##############################################################################################
# Run
##############################################################################################

if __name__ == '__main__':

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


    ips = [
        "192.168.188.142",
        "192.168.189.142",
        "192.168.188.141",
        "192.168.189.141",
        "192.168.182.21",
        "192.168.184.64",
        "192.168.186.64",
        "192.168.187.37",
        "192.168.184.35",
        "192.168.184.63",
        "192.168.182.29",
        "192.168.145.17",
        "192.168.132.91",
        "192.168.182.30",
        "192.168.132.77",
        "192.168.131.90",
        "192.168.132.96",
        "192.168.132.88",
        "192.168.131.94",
        "192.168.182.32",
        "192.168.131.95",
        "192.168.182.24",
        "192.168.131.96",
        "192.168.182.25",
        "192.168.136.26",
        "192.168.131.105",
        "192.168.131.107",
        "192.168.131.111",
        "192.168.131.108",
        "192.168.131.109",
        "192.168.131.110",
        "192.168.182.14",
        "192.168.144.21",
        "192.168.182.20",
        "192.168.182.15",
        "192.168.144.22",
        "192.168.182.16",
        "192.168.186.25",
        "192.168.184.25",
        "192.168.186.39",
        "192.168.184.39",
        "192.168.131.27",
        "82.118.66.251",
        "192.168.182.17",
        "192.168.135.77",
        "192.168.186.42",
        "192.168.186.52",
        "192.168.184.42",
        "192.168.184.52",
        "193.36.240.165",
        "82.118.66.166",
        "192.168.186.43",
        "192.168.184.43",
        "206.142.240.49",
        "206.142.240.220",
        "64.15.187.122",
        "64.15.186.62",
        "192.168.138.82",
        "192.168.138.85",
        "192.168.138.83",
        "192.168.138.86",
        "192.168.186.38",
        "192.168.174.200",
        "192.168.174.201",
        "192.168.186.24",
        "192.168.186.23",
        "193.36.240.90",
        "82.118.66.90",
        "192.168.184.24",
        "192.168.184.23",
        "192.168.184.36",
        "192.168.140.220",
        "193.36.240.91",
        "82.118.66.91",
        "82.118.66.153",
        "192.168.186.44",
        "192.168.136.19",
        "82.118.66.172",
        "192.168.189.150",
        "192.168.184.61",
        "192.168.186.61",
        "192.168.184.62",
        "192.168.186.62",
        "192.168.188.217",
        "192.168.189.217",
        "192.168.147.93",
        "192.168.147.94",
        "192.168.147.95",
        "192.168.147.96",
        "192.168.147.97",
        "192.168.147.98"
    ]

##############################################################################################

    def cp_parse(cli_resp):

        resp = str(cli_resp).replace("'b'", "").replace("b'", "").replace("\\r\\n", " ").replace("?", "").split()

        return resp



    checkpoint = SSHConnect('172.24.252.200', 'LN-RDC-DS1-IFW-1A', 'admin', 'password')

    print('Connected to IFW == '+ str(checkpoint.init_connect()))

    checkpoint.run_cmd('vsenv RDC-PROD-DMZ')

    for ip in ips:

        output = cp_parse(checkpoint.run_cmd(f'arp -a | grep "{ip}"'))

        if len(output) > 7:
            mac = output[7]
            interface = output[10]
            print(interface)

        else:
            print('NA')

    checkpoint.close_ssh()


##############################################################################################

    def pa_parse(cli_resp):

        resp = str(cli_resp).replace("'b'", "").replace("b'", "").replace("\\r\\x1b[K", "").replace("\\r\\n\\x1b[?1h\\x1b=\\r", " ").replace("\\r\\n\\x1b[?1l\\x1b>", " ").replace("\\x1b[?1l\\x1b>", " ").split()

        return resp
    


    paloalto = SSHConnect('172.24.252.203', 'admin@LN-RDC-DS1-EFW-1A(active)>', 'admin', 'password')

    print('Connected to EFW == '+ str(paloalto.init_connect()))

    for ip in ips:

        output = pa_parse(paloalto.run_cmd_wait(f'show arp all | match {ip}'))

        if len(output) > 29:
            interface = output[26]
            print(interface)

        else:
            print('NA')

    paloalto.close_ssh()