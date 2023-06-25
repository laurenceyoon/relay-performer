from pythonosc import osc_message_builder
from pythonosc import udp_client
from ..config import OSC_CLIENT_IP, OSC_CLIENT_PORT


class Client:
    def __init__(self, ip, port):
        self.client = udp_client.UDPClient(ip, port)

    def send_message(self, address, value=None):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        if value:
            msg.add_arg(value)
        self.client.send(msg.build())


osc_client = Client(OSC_CLIENT_IP, OSC_CLIENT_PORT)
