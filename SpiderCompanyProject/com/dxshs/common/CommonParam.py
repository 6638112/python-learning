#根据公司名称查询

class CommonParam(object):
    def __init__(self, base_url, name, pn=1, ps=500):
        self.base_url = base_url
        self.name = name
        self.pn = pn
        self.ps = ps

    def get_url(self):
        url = self.base_url + '?' + 'pn=' + str(self.pn) + '&ps=' + str(self.ps) + '&name=' + self.name
        return url