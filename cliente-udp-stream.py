import socket
import struct
import numpy
import cv2

while 1:
    print("Los canales de video disponibles son:")
    print("1. Dead beats")
    print("2. Live again")
    print("3. Reaper ka Rapper")
    canal = input("Escriba el numero del canal que quiere ver (escriba 4 para terminar la ejecucion): ")

    multicast_group = ''
    server_address  = ''

    if canal == str(4):
        break
    elif canal == str(1):
        multicast_group = '224.3.29.71'
        server_address = ('', 10000)
    elif canal == str(2):
        multicast_group = '224.3.29.72'
        server_address = ('', 10001)
    elif canal == str(3):
        multicast_group = '224.3.29.73'
        server_address = ('', 10002)


    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the server address
    sock.bind(server_address)

    # Tell the operating system to add the socket to
    # the multicast group on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        mreq)

    # Receive/respond loop
    s = b''
    primera = True

    while True:
        data, addr = sock.recvfrom(34561)
        s += data[1:]
        if primera:
            n = struct.unpack('>B', data[0:1])
            if n[0] != 0:
                print("nada")
                continue
            else:
                print("empezamos")
                primera = False
            s = b''
        if len(s) == (34560 * 20):
            frame = numpy.fromstring(s, dtype=numpy.uint8)
            frame = frame.reshape(360, 640, 3)
            cv2.imshow("frame", frame)

            s = b''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
