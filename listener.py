from mesh import Mesh
from utilities import *
# noinspection PyPackageRequirements
from pubsub import pub
from message import Message
import time
import os
import logging
from config import Config

logger = logging.getLogger(__name__)

class Listener():
    def __init__(self):
        self.retries = 4
        self.connect_to_mesh()

        config = Config()
        if not config.get('data.append_log', False):
            with open('packetlog.txt', 'w') as f:
                f.write(get_datestamp() + ': Initialized\n')
        else:
            with open('packetlog.txt', 'a') as f:
                f.write(get_datestamp() + ': Restarted\n')

        pub.subscribe(self.on_receive, "meshtastic.receive")
        pub.subscribe(self.on_disconnect, "meshtastic.connection.lost")

        print('Listener initialized')

    def connect_to_mesh(self):
        while self.retries:
            try:
                self.mesh = Mesh()
                self.retries = 4  # Reset retries after a successful connection
                break
            except Exception as e:
                self.retries -= 1
                if self.retries == 0:
                    logger.error(f"Failed to connect to Mesh after multiple attempts: {e}")
                    raise e
                else:
                    logger.warning(f"Connection error, retrying in 5 seconds... ({self.retries} retries left)")
                    time.sleep(5)

    def __del__(self):
        print("Listener is being destroyed")

    def on_receive(self, packet: dict, interface):
        msg = Message(interface, packet)
        msg.handle_message()

    def on_disconnect(self, interface):
        logger.warning('Disconnected from Mesh')
        self.retries = 4  # Reset retries for reconnection attempts
        self.reconnect_to_mesh()

    def reconnect_to_mesh(self):
        while self.retries:
            try:
                self.mesh.reconnect()
                logger.info('Reconnected to Mesh')
                self.retries = 4  # Reset retries after a successful reconnection
                break
            except Exception as e:
                self.retries -= 1
                if self.retries == 0:
                    logger.error(f"Failed to reconnect to Mesh after multiple attempts: {e}")
                    raise e
                else:
                    logger.warning(f"Reconnection error, retrying in 5 seconds... ({self.retries} retries left)")
                    time.sleep(5)
