import socket

def sendToNetworkDB(temperature, humidity):
    
  msgFromClient       = "{{ 'temperature' : {0}, 'humidity': {1} }}".format(temperature, humidity)
  
  bytesToSend         = msgFromClient.encode('utf-8')
  serverAddressPort   = ("169.254.237.34", 20001)
  bufferSize          = 1024
  
  # Create a UDP socket at client side
  UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  
  # Send to server using created UDP socket
  UDPClientSocket.sendto(bytesToSend, serverAddressPort)
