class Session:

    def __init__(self, **kwargs):
        self.ubnt_net = kwargs.get('net')
        self.ubnt_protect = kwargs('protect')
        self.ubnt_access = kwargs('access')

