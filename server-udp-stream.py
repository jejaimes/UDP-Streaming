import socket
import struct
import cv2
import threading
import time

class StreamingThread (threading.Thread):
   def __init__(self, video, ip, port):
      threading.Thread.__init__(self)
      self.video = video
      self.ip = ip
      self.port = port
   def run(self):
      print ("Starting " + self.video)
      thread(self.video,self.ip,self.port)
      print ("Exiting " + self.video)

def thread(video,ip,port):
    time.sleep(1)
    multicast_group = (ip, port)

    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    sock.settimeout(0.2)

    # Set the time-to-live for messages to 1 so they do not
    # go past the local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:

        # Send data to the multicast group
        cap = cv2.VideoCapture(video)
        n = 0
        #t1 = time.time()
        while True:
            n+=1
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.resize(frame, (320, 180))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            s = gray.tostring()
            #cv2.imshow('frame', frame)
            if not ret:
                #t2 = time.time()
                print("Se acabo el video",video)#,n,t2-t1)
                break
            data = struct.pack('>I', n)
            data = data + s
            print("Enviando frame",n,"de",video)
            sock.sendto(data,multicast_group)
            #d = frame.flatten()
            #s = d.tostring()
            #for i in range(12): #20 12 100
            #    n+=1
            #    data = struct.pack('>I', n)
            #    data = data + s[i * 57600:(i + 1) * 57600] #34560 57600 6912
            #    print("Enviando data",n,"parte",i,"del video "+video)
            #    sock.sendto(data, multicast_group)
            if cv2.waitKey(33) & 0xFF == ord('q'):
                break

    finally:
        print('closing socket')
        sock.close()


# Create new threads
thread1 = StreamingThread('DEAD BEATS.mp4','224.3.29.74',10000)
thread2 = StreamingThread('RIP.mp4','224.3.29.75',10001)
thread3 = StreamingThread('Reaper ka Rapper.mp4','224.3.29.76',10002)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
print ("Exiting Main Thread")