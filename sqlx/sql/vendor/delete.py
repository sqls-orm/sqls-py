from ._vendor import VendorBase
from ..queries import DeleteQuery


class DeleteVendor(VendorBase):
    def delete(self) -> DeleteQuery:
        return DeleteQuery(cnnmgr=self.default, query='DELETE')
