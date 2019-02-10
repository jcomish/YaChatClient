from Client.services.ChatSocket import ChatSocket
import threading
import socket
import Client.services.GlobalVars as GlobalVars
from flask_socketio import emit
from datetime import datetime


class ChatSocketListener(ChatSocket):
    """
    This will be the servant thread, and will listen for any messages coming in from other users
    and the Membership Server.
    """

    def __init__(self, host_ip="127.0.0.1", host_port="27070"):
        self.host_ip = host_ip
        self.host_port = host_port
        chat_socket_sender = threading.Thread(target=self.listen_over_udp)
        chat_socket_sender.start()
        return

    def listen_over_udp(self):
        """
        This made more sense to be in this class...
        :return:
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host_ip, int(self.host_port)))

        while True:
            msg, addr = sock.recvfrom(1024)
            msg = str(msg, 'utf-8')
            GlobalVars.LOGGER.error("(" + str(datetime.now()) + " MESSAGED RECEIVED: " + msg)
            if "MESG" in msg:
                self.recieve_message_from_room(str(msg[5:-1]).split(":"))
            elif "JOIN" in msg:
                self.user_joined_room(str(msg[5:-1]).split(":"))
            elif "EXIT" in msg:
                self.user_exited_room(str(msg[5:-1]))
            else:
                GlobalVars.LOGGER.warning("(" + str(datetime.now()) + ") UNKNOWN MESSAGE: " + msg)

    def recieve_message_from_room(self, msg):
        sender = msg[0]
        message = msg[1].lstrip()
        timestamp = datetime.now()

        GlobalVars.LOGGER.debug("(" + str(timestamp) + ") PROCESSED MESSAGE (" + sender + "): " + message)

        # Send the message to the front end.
        GlobalVars.SOCKETIO.emit('post_message',
                                 {'user': sender,
                                  'message': message,
                                  'timestamp': timestamp.strftime("%-m/%-d/%Y %H:%M")},
                                 namespace='/chat_client')


    def user_joined_room(self, msg):
        new_user = GlobalVars.CHAT_SOCKET_SENDER.parse_users(msg)
        GlobalVars.CHAT_SOCKET_SENDER.hosts = {**GlobalVars.CHAT_SOCKET_SENDER.hosts, **new_user}
        GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ") PROCESSED USER JOIN: " + next(iter(new_user)) +
                                " AT IP: " + new_user[next(iter(new_user))])

        # Send the message to the front end.
        GlobalVars.SOCKETIO.emit('update_group_name',
                                 {'group_name': GlobalVars.CHAT_SOCKET_SENDER.get_group_name()},
                                 namespace='/chat_client')

        # GlobalVars.CHAT_SOCKET_SENDER.send_message_to_room("This is an automated message")


    def user_exited_room(self, msg):
        if msg.lower() in GlobalVars.CHAT_SOCKET_SENDER.screen_name.lower():
            GlobalVars.CHAT_SOCKET_SENDER.shutdown_tcp_socket()
            GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ") PROCESSED SELF LOGOUT")
        else:
            del GlobalVars.CHAT_SOCKET_SENDER.hosts[msg]
            GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ") PROCESSED USER EXIT: " + msg)

            # Send the message to the front end.
            GlobalVars.SOCKETIO.emit('update_group_name',
                                     {'group_name': GlobalVars.CHAT_SOCKET_SENDER.get_group_name()},
                                     namespace='/chat_client')
