from nmsclient import NmsClient


class Path(NmsClient):
    def __init__(self, device, path_name, lsp_name, oper_status):
        super(Path, self).__init__()
        self.device = device
        self.path_name = path_name
        self.lsp_name = lsp_name
        self.oper_status = oper_status

    def path_error(self):
        if self.oper_status == "1":
            return False
        elif self.oper_status == "2":
            return True
        else:
            return f"Status not recognized: {self.oper_status}"

    def in_use(self):

        result = self.search_oxidized("add mpls lsp " + self.lsp_name)

        if result:
            return True
        else:
            return False

    def to_dict(self):
        return {
            "device": self.device,
            "lsp_name": self.lsp_name,
            "path_name": self.path_name,
            "path_error": self.path_error(),
            "in_use": self.in_use(),
        }

    def __repr__(self) -> str:
        return f"<Path {self.name}>"
