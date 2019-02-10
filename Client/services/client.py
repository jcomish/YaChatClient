import os
from flask import Flask, render_template, jsonify, request
import webview
import webbrowser
from Client.services.ChatSocketSender import ChatSocketSender
import Client.services.GlobalVars as GlobalVars
from flask_socketio import SocketIO

client = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static"),
                         template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates"))
client.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1  # disable caching
GlobalVars.SOCKETIO = SocketIO(client)
"""
Flask code to make the front end interact with the ChatSocketManager services.
The initial code was pulled from the sample provided by the pywebview github repository
"""



@client.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@client.route("/")
def chat():
    """[
    Render the index page.. Initialization is performed asynchronously in initialize() function
    """
    return render_template("chat.html")

@client.route("/exit_room", methods=["POST"])
def exit_room():
    """[
    Render the index page.. Initialization is performed asynchronously in initialize() function
    """
    try:
        GlobalVars.CHAT_SOCKET_SENDER.exit_chatroom()
        response = {
            "status": "Successfully disconnected!"
        }
    except:
        response = {
            "status": "Failed to  Disconnect!"
        }
    return jsonify(response)

@client.route("/send_message", methods=["POST"])
def send_message():
    pass

@client.route("/connect_to_mms", methods=["POST"])
def connect_to_mms():
    """[
    Connect to the MMS
    """
    users = GlobalVars.CHAT_SOCKET_SENDER.connect_to_membership_server(request.form.get("name"),
                                                                       request.form.get("host"),
                                                                       request.form.get("port"),
                                                                       request.form.get("chat_port"))

    users = list(GlobalVars.CHAT_SOCKET_SENDER.hosts.keys())
    users.remove(GlobalVars.CHAT_SOCKET_SENDER.screen_name)

    if users:
        response = {
            "status": "Successfully connected!",
            "name": GlobalVars.CHAT_SOCKET_SENDER.screen_name,
            # "host_ip": request.form.get("host_ip"),
            "port": GlobalVars.CHAT_SOCKET_SENDER.chat_port,
            "group_name": GlobalVars.CHAT_SOCKET_SENDER.get_group_name()
        }
    else:
        response = {
            "status": "Failed to connect!"
        }

    return jsonify(response)


@client.route("/fullscreen")
def fullscreen():
    webview.toggle_fullscreen()
    return jsonify({})


@client.route("/open-url", methods=["POST"])
def open_url():
    url = request.json["url"]
    webbrowser.open_new_tab(url)

    return jsonify({})


def run_client():
    # global chat_socket_sender
    own_ip = "127.0.0.1"
    GlobalVars.CHAT_SOCKET_SENDER = ChatSocketSender(own_ip)

    client.run(host=own_ip, port=23946, threaded=True)


# @client.route("/init")
# def initialize():
#     """
#     Perform heavy-lifting initialization asynchronously.
#     :return:
#     """
#     # if can_start:
#     response = {
#         "status": "ok",
#     }
#     # else:
#     #     response = {
#     #         "status": "error"
#     #     }
#
#     return jsonify(response)


# @client.route("/choose/path")
# def choose_path():
#     """
#     Invoke a folder selection dialog here
#     :return:
#     """
#     dirs = webview.create_file_dialog(webview.FOLDER_DIALOG)
#     if dirs and len(dirs) > 0:
#         directory = dirs[0]
#         if isinstance(directory, bytes):
#             directory = directory.decode("utf-8")
#
#         response = {"status": "ok", "directory": directory}
#     else:
#         response = {"status": "cancel"}
#
#     return jsonify(response)


# @client.route("/do/stuff")
# def do_stuff():
#     result = app.do_stuff()
#
#     if result:
#         response = {"status": "ok", "result": result}
#     else:
#         response = {"status": "error"}
#
#     return jsonify(response)


# @client.route("/")
# def check_connection_status():
#     return render_template("chat.html")


if __name__ == "__main__":
    run_client()
