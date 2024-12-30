from vidstream import StreamingServer
import threading

receiver = StreamingServer(host='192.168.29.1',port=9500)

t = threading.Thread(target=receiver.start_server)
t.start()