import threading
import socketserver
from influxdb import InfluxDBClient
import os
from datetime import datetime, timedelta
import json

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        current_thread = threading.current_thread()
        print("Thread: {} client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        Split = threading.Thread(target=ParseIncomingData,args=(data,))
        Split.start()



class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

def publish_messages(data):
    """Publishes multiple messages to a Pub/Sub topic."""
    print('Published {} .'.format(data))
    
    client = InfluxDBClient(os.environ['DATABASE_HOST'], os.environ['DATABASE_PORT'], os.environ['DATABASE_USER'], os.environ['DATABASE_PASSWD'], os.environ['DATABASE_TABLE'])
    client.create_database(os.environ['DATABASE_TABLE'])
    
    json_msg = json.loads(data.decode('utf-8'))
    #json_msg = { "temperature": 12.2, "humidity": 46.3, "host": "dummy" }
    json_body = [
        {
            "measurement": "home_sensor",
            "tags": {
                "host": json_msg['host']
            },
            "time": datetime.today(),
            "fields": {
                "temperature_celsius": json_msg['temperature'],
                "relative_humidity": json_msg['humidity']
            }
        }
    ]
    print(json_body)
    client.write_points(json_body, 's')



def ParseIncomingData(message):
    sender = threading.Thread(target=publish_messages, args=(message,))
    sender.start()


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 20001
    try:
        serverUDP = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
        server_thread_UDP = threading.Thread(target=serverUDP.serve_forever)
        server_thread_UDP.daemon = True
        server_thread_UDP.start()
        serverUDP.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        serverUDP.shutdown()
        serverUDP.server_close()
        exit()
