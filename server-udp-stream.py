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
    time.sleep(1) #Espera para preparme mentalmente para cuando empieze a enviar
    multicast_group = (ip, port)

    # Crea el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Establece un timeout
    sock.settimeout(0.2)

    # Time to live de 1 porque el paquete solo tiene que pasar por la red local
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        cap = cv2.VideoCapture(video) # Se abre el video
        n = 0
        while True:
            n+=1
            ret, frame = cap.read()#Extrae un frame
            if not ret: #Si ret es True se leyo correctamente el frame
                print("Se acabo el video",video)
                break

            frame = cv2.resize(frame, (320, 180)) #Cambia el tamano del video
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Cambia el color del video
            s = gray.tostring() #Vuelve el frame bytes

            data = struct.pack('>I', n)
            data = data + s #Pega un id al frame

            print("Enviando frame",n,"de",video)
            sock.sendto(data,multicast_group) #Envia el frame

            #Envio de datos dividiendo el frame en pedazos
            #d = frame.flatten()
            #s = d.tostring()
            #for i in range(12): #20 12 100
            #    n+=1
            #    data = struct.pack('>I', n)
            #    data = data + s[i * 57600:(i + 1) * 57600] #34560 57600 6912
            #    print("Enviando data",n,"parte",i,"del video "+video)
            #    sock.sendto(data, multicast_group)

            if cv2.waitKey(33) & 0xFF == ord('q'): #Espera para enviar el siguiente frame
                                                    # con esto tambien se puede detener el envio en el thread
                break

    finally: # Se cierra el socket
        print('closing socket')
        sock.close()


# Creacion de los threads
thread1 = StreamingThread('DEAD BEATS.mp4','224.3.29.74',10000)
thread2 = StreamingThread('RIP.mp4','224.3.29.75',10001)
thread3 = StreamingThread('Reaper ka Rapper.mp4','224.3.29.76',10002)

# Inicia los threads
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
print ("Exiting Main Thread")