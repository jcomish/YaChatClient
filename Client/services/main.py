from threading import Thread, Lock
import logging
import coloredlogs
import webview
from time import sleep
from Client.services.client import run_client
from http.client import HTTPConnection
import Client.services.GlobalVars as GlobalVars

server_lock = Lock()
GlobalVars.LOGGER = logging.getLogger(__name__)
# GlobalVars.LOGGER.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG')
coloredlogs.install(level='DEBUG', logger=GlobalVars.LOGGER)

"""
Pywebview wrapper around the Flask application. This was pulled verbatim from the Pywebview repository example.
"""


def url_ok(url, port):
    try:
        conn = HTTPConnection(url, port)
        sleep(1)
        conn.request("GET", "/")
        r = conn.getresponse()
        return r.status == 200
    except:
        GlobalVars.LOGGER.exception("Client not started")
        return False


if __name__ == '__main__':
    GlobalVars.LOGGER.debug("Starting client")
    t = Thread(target=run_client)
    t.daemon = True
    t.start()
    GlobalVars.LOGGER.debug("Checking client")

    while not url_ok("127.0.0.1", 23946):
        sleep(0.1)

    GlobalVars.LOGGER.debug("Server started")
    webview.create_window("YaChat",
                          "http://127.0.0.1:23946",
                          min_size=(640, 480))

#TODO: Fix the weird scrolling issue