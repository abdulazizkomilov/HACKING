import socket

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('192.168.64.2', 8080))

str_data = "\n[+] Connection established.\n"

conn.send(str_data.encode())

received_data = conn.recv(1024)
print(received_data)

conn.close()
