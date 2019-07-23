#根据公司id查询

class Param(object):
    def __init__(self, base_url, company_id, company_name, pn=1, ps=100):
        self.base_url = base_url
        # 公司id
        self.company_id = company_id
        self.company_name = company_name
        self.pn = pn
        self.ps = ps

    def get_url_by_company_id(self):
        url = self.base_url + '?' + 'pn=' + str(self.pn) + '&ps=' + str(self.ps) + '&id=' + self.company_id
        return url

    def get_url_by_company_name(self):
        url = self.base_url + '?' + 'pn=' + str(self.pn) + '&ps=' + str(self.ps) + '&name=' + self.company_name
        return url