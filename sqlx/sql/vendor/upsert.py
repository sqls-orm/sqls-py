from ._vendor import VendorBase
from ..queries import UpsertQuery


class UpsertVendor(VendorBase):
    def upsert(self) -> UpsertQuery:
        return UpsertQuery(cnnmgr=self.default, query='REPLACE')
