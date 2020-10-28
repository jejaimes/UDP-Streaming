import socket
import struct
import sys
import numpy
import cv2
import heapq

clicked = False
frames = [] # Lista que se utilizara como pri

# Funcion para detectar cuando se hace click en el video
def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = True

# Ordena los bytes cuando el frame viene partido
#def ordenarbytes(h):
#    r = b''
#    for i in range(12):
#        b = heapq.heappop(h)
#        r+=b[1]
#    return r

while 1:
    # Imprime el menu en consola
    print("Los canales de video disponibles son:")
    print("1. Dead beats")
    print("2. Excuse my rudness but could you please die")
    print("3. Reaper ka Rapper")
    canal = input("Escriba el numero del canal que quiere ver (escriba 4 para terminar la ejecucion): ")

    multicast_group = ''
    server_address  = ''

    if canal == str(4): # Si escriben 4 se detiene la ejecucion del cliente
        break
    elif canal == str(1): # Primer canal de transmision
        multicast_group = '224.3.29.74'
        server_address = ('', 10000)
    elif canal == str(2): # Segundo canal de transmision
        multicast_group = '224.3.29.75'
        server_address = ('', 10001)
    elif canal == str(3): # Tercer canal de transmision
        multicast_group = '224.3.29.76'
        server_address = ('', 10002)

    # Crea el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Se ata el socket a la direccion correspondiente
    sock.bind(server_address)

    # Tell the operating system to add the socket to
    # the multicast group on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        mreq)

    # Timeout para cuando se deje de recibir data
    sock.settimeout(10)

    # Coloca nombre a la ventana en la que se transmite el video
    cv2.namedWindow('frame')
    # Se le asigna al la ventana la funcion para detectar el click en el video
    cv2.setMouseCallback('frame', onMouse)

    try:
        c = 0
        while not clicked:
            data, addr = sock.recvfrom(57716)# Se recibe data del socket
            c += 1
            n = struct.unpack('>I', data[0:4])
            print("Recibio data",n[0])
            heapq.heappush(frames,(n[0],data[4:])) # Se agrega la tupla id frame al priority queue

            # Para cuando se envia el video partiendo el frame en 12 partes
            #if len(frames) >= 12:#12 20 100
            #    frame = ordenarbytes(frames)
            #    frame = numpy.frombuffer(frame, dtype=numpy.uint8)
            #    frame = frame.reshape(360, 640)
            #    cv2.imshow("frame", frame)

            if len(frames) >= 1: # Si hay frames disponibles para visualizar
                frame = heapq.heappop(frames) # Saca una tupla id frame del priority queue
                frame = frame[1] # Solo la informacion del frame
                frame = numpy.frombuffer(frame, dtype=numpy.uint8) # Se pasa de bytes a un arreglo numpy
                frame = frame.reshape(180, 320) # Se pasa a un arreglo
                cv2.imshow("frame", frame) # Se muestra el frame

            if cv2.waitKey(33) & 0xFF == ord('q'): # Con q se puede detener la visualizacion del video
                break
         # Cuando se deja de ver el video se destruyen las ventanas
        cv2.destroyAllWindows()
        # Se vuelve a permitir hacer click para detener el video
        clicked = False

    # Cuando se detecta un time out se asume que se detiene la ejecucion del cliente
    except socket.timeout as e:
        err = e.args[0]
        if err == 'timed out':
            print('Se acabo la transmision')
            sys.exit(0)
        else:
            print(e)
            sys.exit(1)
    # Ocurrio un error de verdad
    except socket.error as e:
        print(e)
        sys.exit(1)

    finally: # Cuando se termina se cierra el socket
        print('closing socket')
        sock.close()