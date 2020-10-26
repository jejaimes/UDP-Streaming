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
    print("Empezo thread",video)
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
        # print('sending {!r}'.format(message))
        cap = cv2.VideoCapture(video)

        # Look for responses from all recipients
        while True:
            ret, frame = cap.read()
            #cv2.imshow('frame', frame)
            if not ret:
                print("Problema en read")
                break
            d = frame.flatten()
            s = d.tostring()
            for i in range(20):
                data = struct.pack('>B', i)
                data = data + s[i * 34560:(i + 1) * 34560]
                sock.sendto(data, multicast_group)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    finally:
        print('closing socket')
        sock.close()


# Create new threads
thread1 = StreamingThread('DEAD BEATS.mp4','224.3.29.71',10000)
thread2 = StreamingThread('Live again.mp4','224.3.29.72',10001)
thread3 = StreamingThread('Reaper ka Rapper.mp4','224.3.29.73',10002)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
print ("Exiting Main Thread")