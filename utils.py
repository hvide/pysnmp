from asyncio.log import logger
import logging
import socket
import yaml

logger = logging.getLogger()


def ip(host):
    domain = '.as43531.net'
    try:
        return socket.gethostbyname(host + domain)
    except socket.gaierror as e:
        logger.warning(
            '%s\nThe hostname %s could not be resolved.' % (str(e), host))
        # sys.exit(1)


def yml_load(x):
    with open(x) as f:
        try:
            return yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
