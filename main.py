import logging
from pysnmp.hlapi import *
from pprint import pprint

import utils

logger = logging.getLogger()

logger.setLevel(logging.INFO)  # Overall minimum logging level

# Configure the logging messages displayed in the Terminal
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
# Minimum logging level for the StreamHandler
stream_handler.setLevel(logging.DEBUG)

# # Configure the logging messages written to a file
# file_handler = logging.FileHandler('info.log')
# file_handler.setFormatter(formatter)
# # Minimum logging level for the FileHandler
# file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)


class Path:
    def __init__(self, name, in_use, lsp, oper_status):
        self.name = name
        self.in_use = in_use
        self.lsp = lsp
        self.oper_status = oper_status

    def is_active(self):
        if self.oper_status == "1":
            return True
        elif self.oper_status == "2":
            return False
        else:
            return f"Status not recognized: {self.oper_status}"

    def __repr__(self) -> str:
        return f"<Path {self.name}>"


MIB = {
    'mplsTunnelName': '1.3.6.1.2.1.10.166.3.2.2.1.5',
    'mplsTunnelDescr': '1.3.6.1.2.1.10.166.3.2.2.1.6',
    'mplsTunnelIsIf': '1.3.6.1.2.1.10.166.3.2.2.1.7',
    'mplsTunnelRole': '1.3.6.1.2.1.10.166.3.2.2.1.10',
    'mplsTunnelSessionAttributes': '1.3.6.1.2.1.10.166.3.2.2.1.15',
    'mplsTunnelPathInUse': '1.3.6.1.2.1.10.166.3.2.2.1.21',
    'mplsTunnelTotalUpTime': '1.3.6.1.2.1.10.166.3.2.2.1.27',
    'mplsTunnelInstanceUpTime': '1.3.6.1.2.1.10.166.3.2.2.1.28',
    'mplsTunnelCreationTime': '1.3.6.1.2.1.10.166.3.2.2.1.32',
    'mplsTunnelStateTransitions': '1.3.6.1.2.1.10.166.3.2.2.1.33',
    'mplsTunnelOperStatus': '1.3.6.1.2.1.10.166.3.2.2.1.35',
}

devices = utils.yml_load('devices.yml')['devices']


def main():

    for device in devices:

        logger.debug(f"Quering device: {device}")

        g = bulkCmd(SnmpEngine(),
                    CommunityData('test-agent', 'x98wuyf89qwudsfg8'),
                    UdpTransportTarget((utils.ip(device), 161),
                                       timeout=1,
                                       retries=0
                                       ),
                    ContextData(), 0, 5,
                    ObjectType(ObjectIdentity(MIB['mplsTunnelName'])),
                    ObjectType(ObjectIdentity(MIB['mplsTunnelDescr'])),
                    ObjectType(ObjectIdentity(MIB['mplsTunnelIsIf'])),
                    ObjectType(ObjectIdentity(MIB['mplsTunnelPathInUse'])),
                    ObjectType(ObjectIdentity(MIB['mplsTunnelOperStatus'])),
                    lexicographicMode=False)

        paths = []
        for errorIndication, errorStatus, errorIndex, varBinds in g:

            if isinstance(errorStatus, int):
                logger.debug(f"No data return for device {device}")
                break
            elif not errorStatus.prettyPrint() == "noError":
                print(errorStatus.prettyPrint())

            data = []
            for varBind in varBinds:
                data.append(varBind[1].prettyPrint())

            # continue
            if data:
                if data[2] == "1":  # If path starts on the node
                    name = data[1].split(' ')[1][1:-1]

                    path = Path(name=name,
                                in_use=data[3],
                                lsp=data[0],
                                oper_status=data[4])

                    paths.append(path)

        if paths:
            for path in paths:
                if path.is_active() == False:
                    print(
                        f"Device: {device} - Lsp: {path.lsp} - Path: {path.name} - Active: {path.is_active()}")


if __name__ == "__main__":
    main()
