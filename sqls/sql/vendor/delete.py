from ._vendor import VendorBase
from ..queries import DeleteQuery


class DeleteVendor(VendorBase):
    def delete(self) -> DeleteQuery:
        return DeleteQuery(pool=self.pool, query='DELETE')
