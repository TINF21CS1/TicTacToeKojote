from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
import logging
import time

logger = logging.getLogger(__name__)

def discover_games(timeout: int = 5) -> dict:
    """
    Returns a dictionary of games that are available to play.
    The key is the name of the game and the value is the IP address of the server as string.

    param: timeout. The time in seconds to wait for responses. Default is 5 seconds.

    return: dict. A dictionary of games on the network that are available to play. Key is the name, Value is the IP as string.
    """

    class MyListener(ServiceListener):
        def __init__(self):
            self.results = {}

        def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            info = zc.get_service_info(type_, name)
            if info:
                logger.info(f"Service {name} found, service address: {info.parsed_addresses()[0]}") # TODO only gets first address, so dual stack is not possible
                self.results.update({name.removesuffix('._tictactoe._tcp.local.'): info.parsed_addresses()[0]})
            else:
                logger.error(f"Service {name} found, no info")

        def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            logger.info(f"Service {name} removed")


    zeroconf = Zeroconf()
    listener = MyListener()
    ServiceBrowser(zeroconf, "_tictactoe._tcp.local.", listener)

    time.sleep(timeout)

    zeroconf.close()
    return listener.results

if __name__ == "__main__":
    while True:
        print(discover_games())
        time.sleep(5)
