import threading

from pythonosc import dispatcher, osc_message_builder, osc_server, udp_client

from ..config import OSC_CLIENT_IP, OSC_CLIENT_PORT, ENABLE_OSC


class OSCClient:
    def __init__(self, ip, port):
        self.client = udp_client.UDPClient(ip, port)

    def send_message(self, address, value=None):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        if value:
            msg.add_arg(value)
        self.client.send(msg.build())


osc_client = OSCClient(OSC_CLIENT_IP, OSC_CLIENT_PORT) if ENABLE_OSC else None


class OSCServer:
    def __init__(self, ip, port):
        self.dispatcher = dispatcher.Dispatcher()
        self.server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever)

    def start(self):
        print(f"Serving on {self.server.server_address}")
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server_thread.join()

    def add_handler(self, address, handler):
        self.dispatcher.map(address, handler)
        print(f"Handler added for {address}")
