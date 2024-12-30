from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from vidstream import StreamingServer
import threading

# Function to start the server
def start_server():
    server = StreamingServer('0.0.0.0', 9999)
    server.start_server()

# Django view to start the streaming server
def start_streaming_server(request):
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    return HttpResponse("Streaming server started. Ready to receive screen sharing.")






from vidstream import ScreenShareClient

# Function to start the screen sharing client
def start_screen_share():
    client = ScreenShareClient('127.0.0.1', 9999)  # Replace with the server's IP
    client.start_stream()

# Django view to start screen sharing
def start_screen_sharing(request):
    client_thread = threading.Thread(target=start_screen_share, daemon=True)
    client_thread.start()
    return HttpResponse("Screen sharing started.")



from django.shortcuts import render

def screen_share(request):
    return render(request, 'stream.html')
