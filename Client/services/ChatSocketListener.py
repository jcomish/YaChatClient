from Client.services.ChatSocket import ChatSocket
import threading
import socket
import Client.services.GlobalVars as GlobalVars
from datetime import datetime


class ChatSocketListener(ChatSocket):
    """
    This will be the servant thread, and will listen for any messages coming in from other users
    and the Membership Server.
    """

    def __init__(self, local_ip="127.0.0.1", listener_port="27070"):
        self.local_ip = local_ip
        self.listener_port = listener_port
        self.chat_socket_listener = threading.Thread(target=self.listen_over_udp)
        self.chat_socket_listener.start()
        return

    def close_listener(self):
        self.chat_socket_listener.join()

    def listen_over_udp(self):
        """
        This made more sense to be in this class...
        :return:
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = (self.local_ip, int(self.listener_port))
            sock.bind(server_address)

            while True:
                msg, addr = sock.recvfrom(1024)
                msg = str(msg, 'utf-8')
                GlobalVars.LOGGER.info("(" + str(datetime.now()) + " MESSAGED RECEIVED: " + msg)
                if "MESG" in msg:
                    self.recieve_message_from_room(str(msg[5:-1]).split(":"))
                elif "JOIN" in msg:
                    self.user_joined_room(str(msg[5:-1]).split(":"))
                elif "EXIT" in msg:
                    self.user_exited_room(str(msg[5:-1]))
                else:
                    GlobalVars.LOGGER.warning("(" + str(datetime.now()) + ") UNKNOWN MESSAGE: " + msg)
        except:
            GlobalVars.LOGGER.exception("(" + str(datetime.now()) + ") FAILED TO CLAIM PORT " + self.listener_port + "!")

    def recieve_message_from_room(self, msg):
        sender = msg[0]
        message = msg[1].lstrip()
        timestamp = datetime.now()

        GlobalVars.LOGGER.debug("(" + str(timestamp) + ") PROCESSED MESSAGE (" + sender + "): " + message)

        # Send the message to the front end, but not if it is your own.
        if (sender.lower() != GlobalVars.CHAT_SOCKET_SENDER.screen_name.lower()):
            # Send the message to the front end.
            GlobalVars.SOCKETIO.emit('post_message',
                                     {'user': sender,
                                      'message': message,
                                      'timestamp': timestamp.strftime("%-m/%-d/%Y %H:%M")},
                                     namespace='/chat_client')


    def user_joined_room(self, msg):
        new_user = GlobalVars.CHAT_SOCKET_SENDER.parse_users(msg)
        user_str = next(iter(new_user))
        if (user_str.lower() != GlobalVars.CHAT_SOCKET_SENDER.screen_name.lower):
            GlobalVars.CHAT_SOCKET_SENDER.hosts = {**GlobalVars.CHAT_SOCKET_SENDER.hosts, **new_user}
            GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ") PROCESSED USER JOIN: " + user_str +
                                    " AT IP: " + new_user[user_str][0] + " " + new_user[user_str][1])

            # Send the message to the front end.
            GlobalVars.SOCKETIO.emit('update_group_name',
                                     {'group_name': GlobalVars.CHAT_SOCKET_SENDER.get_group_name(),
                                      'isEnter': True,
                                      'user': user_str},
                                     namespace='/chat_client')

        else: # This is just confirmation that you yourself have joined... no action required.
            return

    def user_exited_room(self, msg):
        if msg.lower() in GlobalVars.CHAT_SOCKET_SENDER.screen_name.lower():
            GlobalVars.CHAT_SOCKET_SENDER.shutdown_tcp_socket()
            GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ") PROCESSED SELF LOGOUT")
        else:
            del GlobalVars.CHAT_SOCKET_SENDER.hosts[msg]
            GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ") PROCESSED USER EXIT: " + msg)

        # Send the message to the front end.
        GlobalVars.SOCKETIO.emit('update_group_name',
                                 {'group_name': False,
                                  'isEnter': False,
                                  'user': msg},
                                 namespace='/chat_client')

