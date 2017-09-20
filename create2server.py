import socket
import sys, time
import queue, threading
import create2api

HOST = '' # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

#Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

print('Socket bind complete')

#Start listening on socket, limit to one connection
s.listen(1)
print('Socket now listening')

roomba = create2api.Create2()
commandQueue = queue.Queue()
queueLock = threading.Lock()

#Function for handling connections. This will be used to create threads
def clientthread(conn, com_queue):
	#infinite loop so that function does not terminate and thread does not end.
	while True:
		#Receiving from client
		data = conn.recv(256)

		if not data: 
			break

		try:
			print("got message: " + str(data.decode('utf-8')))
			data = str(data.decode('utf-8')).split(',')

			#Non-queued single byte commands
			if create2api.RequestType(data[0]) == create2api.RequestType.START:
				print("NQ START Roomba")
				roomba.start()
			elif create2api.RequestType(data[0]) == create2api.RequestType.RESET:
				print("NQ RESET Roomba")
				roomba.reset()
			elif create2api.RequestType(data[0]) == create2api.RequestType.STOP:
				print("NQ STOP Roomba")
				roomba.stop()
			elif create2api.RequestType(data[0]) == create2api.RequestType.SAFE:
				print("NQ SAFE Roomba")
				roomba.safe()
			elif create2api.RequestType(data[0]) == create2api.RequestType.FULL:
				print("NQ FULL Roomba")
				roomba.full()
			elif create2api.RequestType(data[0]) == create2api.RequestType.CLEAN:
				print("NQ CLEAN Roomba")
				roomba.clean()
			elif create2api.RequestType(data[0]) == create2api.RequestType.MAX:
				print("NQ MAX Roomba")
				roomba.max()
			elif create2api.RequestType(data[0]) == create2api.RequestType.SPOT:
				print("NQ SPOT Roomba")
				roomba.spot()
			elif create2api.RequestType(data[0]) == create2api.RequestType.DOCK:
				print("NQ DOCK Roomba")
				roomba.seek_dock()
			elif create2api.RequestType(data[0]) == create2api.RequestType.POWER:
				print("NQ POWER Roomba")
				roomba.power()

			#Non-queued multibyte commands, no reply
			elif create2api.RequestType(data[0]) == create2api.RequestType.DRIVE:
				print("NQ DRIVE Roomba")
				roomba.drive(int(data[1]), int(data[2]))
			elif create2api.RequestType(data[0]) == create2api.RequestType.MOTORS:
				print("NQ MOTORS Roomba")
				roomba.motors_pwm(int(data[1]), int(data[2]), int(data[3]))
			elif create2api.RequestType(data[0]) == create2api.RequestType.BAUD:
				print("NQ BAUD Roomba")
				roomba.baud(int(data[1]))
			elif create2api.RequestType(data[0]) == create2api.RequestType.TIME:
				print("NQ TIME Roomba")
				roomba.set_day_time(data[1].lower(), int(data[2]), int(data[3]))
			elif create2api.RequestType(data[0]) == create2api.RequestType.DIGIT_LED:
				print("NQ DIGIT_LED Roomba")
				roomba.digit_led_ascii(data[1])
			elif create2api.RequestType(data[0]) == create2api.RequestType.REQUEST_PACKET:
				print("NQ REQUEST_PACKET Roomba")
				roomba.request_packet(create2api.PacketType(int(data[1])))

			#Non-queued multibyte command with reply
			elif create2api.RequestType(data[0]) == create2api.RequestType.REQUEST_PACKET_DATA:
				print("NQ REQUEST_PACKET_DATA Roomba")
				conn.sendall(str(roomba.request_packet_data(create2api.PacketType(int(data[1])))))
			elif create2api.RequestType(data[0]) == create2api.RequestType.GET_STORED_PACKET_DATA:
				print("NQ GET_STORED_PACKET_DATA Roomba")
				conn.sendall(str(roomba.get_stored_packet_data(create2api.PacketType(int(data[1])))))


			#Queued single byte commands
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_START:
				queueLock.acquire()
				com_queue.put((roomba.start, tuple()))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_RESET:
				queueLock.acquire()
				com_queue.put((roomba.reset, tuple()))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_STOP:
				queueLock.acquire()
				com_queue.put((roomba.stop, tuple()))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_SAFE:
				queueLock.acquire()
				com_queue.put((roomba.safe, tuple()))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_FULL:
				queueLock.acquire()
				com_queue.put((roomba.full, tuple()))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_CLEAN:
				queueLock.acquire()
				com_queue.put((roomba.clean, tuple()))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_MAX:
				queueLock.acquire()
				com_queue.put((roomba.max, tuple()))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_SPOT:
				queueLock.acquire()
				com_queue.put((roomba.spot, tuple()))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_DOCK:
				queueLock.acquire()
				com_queue.put((roomba.seek_dock, tuple()))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_POWER:
				queueLock.acquire()
				com_queue.put((roomba.power, tuple()))
				queueLock.release()

			#Queued multibyte commands, no reply
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_DRIVE:
				queueLock.acquire()
				com_queue.put((roomba.drive, (int(data[1]), int(data[2]))))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_MOTORS:
				queueLock.acquire()
				com_queue.put((roomba.motors_pwm, (int(data[1]), int(data[2]), int(data[3]))))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_BAUD:
				queueLock.acquire()
				com_queue.put((roomba.baud, (int(data[1]),)))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_TIME:
				queueLock.acquire()
				com_queue.put((roomba.set_day_time, (data[1].lower(), int(data[2]), int(data[3]))))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_DIGIT_LED:
				queueLock.acquire()
				com_queue.put((roomba.digit_led_ascii, (data[1],)))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.QUEUE_REQUEST_PACKET:
				queueLock.acquire()
				com_queue.put((roomba.request_packet, (create2api.PacketType(int(data[1])),)))
				queueLock.release()

			#Queued multibyte command with reply
			elif create2api.RequestType(data[0]) == create2api.RequestType.REQUEST_PACKET_DATA:
				q_func = lambda conn, data: conn.sendall(roomba.request_packet_data(data))
				queueLock.acquire()
				com_queue.put((q_func, (conn, str(create2api.PacketType(int(data[1]))))))
				queueLock.release()
			elif create2api.RequestType(data[0]) == create2api.RequestType.GET_STORED_PACKET_DATA:
				q_func = lambda conn, data: conn.sendall(roomba.get_stored_packet_data(data))
				queueLock.acquire()
				com_queue.put((q_func, (conn, str(create2api.PacketType(int(data[1]))))))
				queueLock.release()


			#wait command
			elif create2api.RequestType(data[0]) == create2api.RequestType.WAIT:
				queueLock.acquire()
				com_queue.put((time.sleep, (int(data[1]),)))
				queueLock.release()

		except (UnicodeDecodeError, ValueError) as e:
			if isinstance(e, ValueError):
				print("Not a Valid Command")
			else:
				print("Unable to decode message")

	#came out of loop
	conn.close()

#wait to accept a connection - blocking call
conn, addr = s.accept()
print('Connected with ' + addr[0] + ':' + str(addr[1]))

conn.send(b'You are now connected to roomba') #send only takes string

#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
threading.Thread(target=clientthread, args=(conn, commandQueue)).start()

while True:
	#here we go through our command queue and execute them
	if not commandQueue.empty():
		queueLock.acquire()
		func, args = commandQueue.get()
		queueLock.release()
		conn.send(bytes("performing action: " + func.__name__ + " with args: " + str(args), encoding="utf-8"))
		func(*args)
 
s.close()