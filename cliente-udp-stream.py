import socket
import struct
import sys
import numpy
import cv2
import heapq
#import threading
#import time

recibiendo = False
clicked = False
frames = []

def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = True

def ordenarbytes(h):
    r = b''
    for i in range(12):
        b = heapq.heappop(h)
        r+=b[1]
    return r

#def mostrar(heap,click):
#    time.sleep(3)
#    while not click:
#        if len(heap) >= 12:  # 12 20
#            framed = ordenarbytes(heap)
#            framed = numpy.frombuffer(framed, dtype=numpy.uint8)
#            framed = framed.reshape(360, 640, 3)
#            cv2.imshow("frame", framed)
#
#class Muestra(threading.Thread):
#   def __init__(self, heap, click):
#      threading.Thread.__init__(self)
#      self.heap = heap
#      self.click = click
#   def run(self):
#      print ("Starting viewing")
#      mostrar(self.heap,self.click)
#      print ("Finished viewing")

while 1:
    print("Los canales de video disponibles son:")
    print("1. Dead beats")
    print("2. Excuse my rudness but could you please die")
    print("3. Reaper ka Rapper")
    canal = input("Escriba el numero del canal que quiere ver (escriba 4 para terminar la ejecucion): ")

    multicast_group = ''
    server_address  = ''

    if canal == str(4):
        break
    elif canal == str(1):
        multicast_group = '224.3.29.74'
        server_address = ('', 10000)
    elif canal == str(2):
        multicast_group = '224.3.29.75'
        server_address = ('', 10001)
    elif canal == str(3):
        multicast_group = '224.3.29.76'
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
    sock.settimeout(10)
    # Receive/respond loop
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', onMouse)

    #video = Muestra(frames,clicked)
    #video.start()
    #video.join()
    try:
        c = 0
        while not clicked:
            data, addr = sock.recvfrom(57716)#57604 34564 6916
            c += 1
            n = struct.unpack('>I', data[0:4])
            print("Recibio data",n[0])
            heapq.heappush(frames,(n[0],data[4:]))
            #if c < 1200:
            #    continue
            #if len(frames) >= 12:#12 20 100
            #    frame = ordenarbytes(frames)
            #    frame = numpy.frombuffer(frame, dtype=numpy.uint8)
            #    frame = frame.reshape(360, 640)
            #    cv2.imshow("frame", frame)
            if len(frames) >= 1:
                frame = heapq.heappop(frames)
                frame = frame[1]
                frame = numpy.frombuffer(frame, dtype=numpy.uint8)
                frame = frame.reshape(180, 320)
                cv2.imshow("frame", frame)
            if cv2.waitKey(33) & 0xFF == ord('q'):
                break
        cv2.destroyWindow('frame')
        cv2.destroyAllWindows()
        clicked = False
    except socket.timeout as e:
        err = e.args[0]
        # this next if/else is a bit redundant, but illustrates how the
        # timeout exception is setup
        if err == 'timed out':
            print('se acabo la transmision')
            sys.exit(0)
        else:
            print(e)
            sys.exit(1)
    except socket.error as e:
        # Something else happened, handle error, exit, etc.
        print(e)
        sys.exit(1)