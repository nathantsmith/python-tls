from socket import create_connection
from ssl import CERT_NONE, SSLContext, PROTOCOL_TLS_CLIENT


ip = '192.168.1.50'
hostname='192.168.1.50'
port = 4544
context = SSLContext(PROTOCOL_TLS_CLIENT)
# context.load_verify_locations('Medtronic.pem')
context.check_hostname = False
context.verify_mode = CERT_NONE
with create_connection((ip, port)) as client:
    with context.wrap_socket(client, server_hostname=hostname, server_side=False ) as tls:
        print(f'Using {tls.version()}')
        tls.sendall(b'Hello, world')

        data = tls.recv(1024)
        print(f'Server says: {data}')
