from vidstream import StreamingServer
import threading

receiver = StreamingServer(host='192.168.29.242',port=9500)

t = threading.Thread(target=receiver.start_server)
t.start()

while input("") != 'STOP':
    continue
receiver.stop_server()