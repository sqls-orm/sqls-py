from ._vendor import VendorBase
from ..queries import InsertQuery


class InsertVendor(VendorBase):
    def insert(self) -> InsertQuery:
        return InsertQuery(cnnmgr=self.default, query='INSERT')
