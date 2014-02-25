import socket

s = socket.socket()
host = socket.gethostname()
s.connect((host, 12345))
print "Connected to Server"

def get_file(s, file_name):
    f = open('a.mp3', 'wb')
    print "Running..."
    cmd = 'get\n%s\n' % (file_name)
    s.sendall(cmd)
    r = s.recv(2)
    size = int(s.recv(16))
    recvd = ''
    while size > len(recvd):
        data = s.recv(1024)
        if not data: 
            break
        recvd += data
        f.write(data)
    s.sendall('ok')
    return recvd

get_file(s, '/Volumes/SEANS_THING/tnt.mp3')
#print get_file(s, 'file2')
s.sendall('end\n')
print "done!"
