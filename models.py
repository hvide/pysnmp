import typing
import ipaddress


class Device:
    def __init__(self, device_info: typing.Dict):
        self.device_id: int = device_info['device_id']
        self.disabled: bool = device_info['disabled']
        self.hostname: str = device_info['hostname']
        try:
            self.host_short: str = ".".join(
                device_info['hostname'].split(".", 3)[:3])
        except:
            self.host_short = self.hostname
        self.ip: str = device_info['ip']
        self.status: str = device_info['status']
        self.sysName: str = device_info['sysName']
        self.version: str = device_info['version']
        self.hardware: str = device_info['sysDescr'].split(' ', 3)[1][1:-1] \
            if device_info['os'] == "xos" \
            else device_info['hardware']
        self.serial: str = device_info['serial']
        self.sysDescr: str = device_info['sysDescr']

    def to_dict(self) -> typing.Dict:
        return {
            'device_id': self.device_id,
            'disabled': self.disabled,
            'hostname': self.hostname,
            'status': self.status,
            'sysName': self.sysName,
            'sysDescr': self.sysDescr,
            'hardware': self.hardware,
            'ip': self.ip,
            'version': self.version,
            'serial': self.serial
        }

    def __repr__(self):
        return str(self.hostname)


class SearchOxidizedResult:
    def __init__(self, search_oxidized_result: typing.Dict):
        self.dev_id: int = search_oxidized_result['dev_id']
        self.full_name: str = search_oxidized_result['full_name']
        self.node: str = search_oxidized_result['node']

    def to_dict(self) -> typing.Dict:
        return {
            'device_id': self.dev_id,
            'hostname': self.full_name,
            'sysName': self.node,
        }

    def __repr__(self):
        return self.full_name


class Port:
    def __init__(self, get_port_info: typing.Dict):
        self.port_id: int = get_port_info['port_id']
        self.device_id: str = get_port_info['device_id']
        self.ifDescr: str = get_port_info['ifDescr']
        self.ifName: str = get_port_info['ifName']
        self.portName: str = get_port_info['portName']
        self.ifIndex: str = get_port_info['ifIndex']
        self.ifOperStatus: str = get_port_info['ifOperStatus']
        self.ifAdminStatus: str = get_port_info['ifAdminStatus']
        self.ifMtu: str = get_port_info['ifMtu']
        self.ifAlias: str = get_port_info['ifAlias']

    def __repr__(self):
        return self.ifName


class OspfNbrResult:
    def __init__(self, neighbour: typing.Dict):
        self.id: int = neighbour['id']
        self.device_id: int = neighbour['device_id']
        self.ospfNbrIpAddr: str = neighbour['ospfNbrIpAddr']

        ip = ipaddress.ip_address(self.ospfNbrIpAddr)
        if self._is_even(int(ip)):  # % 2 == 0:
            self.ospfIntIpAddr = str(ip - 1)
        else:
            self.ospfIntIpAddr = str(ip + 1)

        self.ospfNbrRtrId: str = neighbour['ospfNbrRtrId']
        self.ospfNbrState: str = neighbour['ospfNbrState']

    def _is_even(self, num: int) -> bool:
        if num % 2 == 0:
            return True
        else:
            return False

    def to_dict(self) -> typing.Dict:
        return {
            'id': self.id,
            'device_id': self.device_id,
            'ospfNbrIpAddr': self.ospfNbrIpAddr,
            'ospfNbrIpAddr': self.ospfIntIpAddr,
            'ospfNbrRtrId': self.ospfNbrRtrId,
            'ospfNbrState': self.ospfNbrState,
        }

    def __repr__(self):
        return str(self.id)
