from vidstream import ScreenShareClient
import threading

sender = ScreenShareClient(host='192.168.29.1',port=9500)

t = threading.Thread(target=sender.start_stream)
t.start()

while input("") != 'STOP':
    continue
sender.stop_stream()