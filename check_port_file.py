
import socket
import time
import sys

def check_port():
    host = "127.0.0.1"
    port = 8000
    start = time.time()
    
    with open("port_check_status.txt", "w") as f:
        f.write("Checking...\n")
        
    while time.time() - start < 10:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                with open("port_check_status.txt", "w") as f:
                    f.write("OPEN")
                return
            else:
                time.sleep(1)
        except Exception as e:
             with open("port_check_status.txt", "w") as f:
                f.write(f"ERROR: {e}")
             return

    with open("port_check_status.txt", "w") as f:
        f.write("CLOSED")

if __name__ == "__main__":
    check_port()
