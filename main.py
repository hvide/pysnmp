import logging
import os
from pysnmp.hlapi import *
from tqdm import tqdm
from dotenv import load_dotenv

from mail import Mail
from path import Path

import utils

logger = logging.getLogger()

logger.setLevel(logging.INFO)  # Overall minimum logging level

# Configure the logging messages displayed in the Terminal
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)

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


load_dotenv()
SNMP_COMMUNITY = os.getenv('SNMP_COMMUNITY')


def main():

    paths = []
    logger.info("Collecting data from hosts.")
    for device in tqdm(devices):

        logger.debug(f"Quering device: {device}")

        g = bulkCmd(SnmpEngine(),
                    CommunityData('test-agent', SNMP_COMMUNITY),
                    UdpTransportTarget((utils.ip(device), 161),
                                       timeout=1,
                                       retries=0
                                       ),
                    ContextData(), 0, 5,
                    ObjectType(ObjectIdentity(MIB['mplsTunnelName'])),
                    ObjectType(ObjectIdentity(MIB['mplsTunnelDescr'])),
                    ObjectType(ObjectIdentity(MIB['mplsTunnelIsIf'])),
                    ObjectType(ObjectIdentity(MIB['mplsTunnelOperStatus'])),
                    lexicographicMode=False)

        for errorIndication, errorStatus, errorIndex, varBinds in g:

            if isinstance(errorStatus, int):
                logger.debug(f"No data return for device {device}")
                break
            elif not errorStatus.prettyPrint() == "noError":
                print(errorStatus.prettyPrint())

            data = []
            for varBind in varBinds:

                data.append(varBind[1].prettyPrint())

            if data:
                if data[2] == "1":  # If path starts on the node
                    path_name = data[1].split(' ')[1][1:-1]

                    path = Path(device=device, path_name=path_name,
                                lsp_name=data[0],
                                oper_status=data[3])

                    paths.append(path)

    if paths:

        logger.info("Processing data.")
        dataset = [path.to_dict()
                   for path in tqdm(paths) if path.path_error() == True or path.in_use() == False]

        table = utils.as_table(dataset)
        print(table)

        mails = ["davide.gilardoni@bso.co"]
        subject = "RSVP lsp / path"
        content = table

        mail = Mail()
        mail.send(mails, subject, content)


if __name__ == "__main__":
    main()
