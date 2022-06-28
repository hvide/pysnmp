from asyncio.log import logger
import logging
import socket
import yaml
from tabulate import tabulate


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


def as_table(data, tablefmt: str = "simple"):
    header = data[0].keys()
    rows = [x.values() for x in data]
    return tabulate(rows, header, tablefmt)
