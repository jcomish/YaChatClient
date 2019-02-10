from Client.services.ChatSocket import ChatSocket
from Client.services.ChatSocketListener import ChatSocketListener
from datetime import datetime
import Client.services.GlobalVars as GlobalVars

class ChatSocketSender(ChatSocket):
    """
    This class handles all of the messages that will be sent from the client. This will be
    run on the primary thread.
    """
    def __init__(self, own_ip="127.0.0.1"):
        self.hosts = {}
        self.screen_name = ""
        self.host_ip = ""
        self.host_port = ""
        self.chat_port = ""
        self.own_ip = own_ip
        self.open_socket = None

    def get_group_name(self):
        users = list(self.hosts.keys())
        users.remove(self.screen_name)

        if (len(users) == 0):
            return self.chat_port + ": " + \
                   self.screen_name
        else:
            return self.chat_port + ": " + \
                   self.screen_name + ", " + \
                   ", ".join(users)

    def send_message_to_room(self, message):
        message = "MESG " + self.screen_name + ": " + message + "\n"
        for name in self.hosts:
            if name.lower != self.screen_name.lower(): # We don't want to send the message to ourselves.
                self.send_msg_over_udp(message, self.hosts[name], self.chat_port)
                GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ") SENT MESSAGE: " + message)

    def exit_chatroom(self):
        """
        Exits the Chatroom, telling the Membership server that it is done.
        :return: None
        """
        self.send_msg_over_tcp("EXIT\n")
        GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ") SENT EXIT MESSAGE")

    def parse_users(self, msg: str):
        """
        Using the welcome response sent from the Membership server, parse out the user data of people
        currently in the chatroom.
        :param acpt_message: The string version of the response from the HELO message to the Membership server/.
        :return: A dictionary of user data, with the screenname as the key, and the ip and host as the value in a tuple.
                 Returns False if a RJCT message was sent.
        """
        temp_dict = {}
        for user in msg:
            data = user.split(" ")
            temp_dict[data[0]] = (data[1])
        return temp_dict

    def connect_to_membership_server(self, name, host, port, chat_port):
        """
        Establishes the connection from the client to the Membership server.
        :param name: Screenname of the client.
        :param host: Host ip of the membership server.
        :param port: Port of the membership server.
        :param chat_port: Port of the chatroom you are establishing.
        :return: A dictionary of user data, with the screenname as the key, and the ip and host as the value in a tuple.
                 Returns False if a RJCT message was sent.
        """
        try:
            self.screen_name = name
            self.host_ip = host
            self.host_port = str(port)
            self.chat_port = str(chat_port)

            GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ")" + " ATTEMPTING CONNECTION TO " +
                                    self.host_port + " " + self.host_port)

            self.establish_tcp_socket()
            self.send_msg_over_tcp("HELO " + self.screen_name + " " + self.host_ip + " " + self.chat_port + "\n")
            msg = self.recv_msg_over_tcp()

            # Process the message
            if msg[:4] == "ACPT":
                users = self.parse_users(str(msg[5:-1]).split(":"))
            elif msg[:4] == "RJCT":
                GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ") SCREEN NAME ALREADY EXISTS! REJECTED")
                return False

            self.hosts = {**self.hosts, **users}

            GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ")" + " SUCCESSFUL CHATTER CREATION AT PORT " +
                                    self.chat_port)

            GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ")" + " STARTING LISTENER...")
            # Start up the listener!
            ChatSocketListener(self.own_ip, self.chat_port)
            GlobalVars.LOGGER.debug("(" + str(datetime.now()) + ")" + " SUCCESSFULLY STARTED LISTENER AT " +
                                    self.own_ip + " " + self.chat_port)
            return users
        except:
            return False
