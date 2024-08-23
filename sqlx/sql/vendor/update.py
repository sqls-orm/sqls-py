from typing import Union, overload

from ._vendor import VendorBase
from ..queries import UpdateQuery
from ...types import Schema


class UpdateVendor(VendorBase):
    @overload
    def update(
            self,
            table: type[Schema],
    ) -> UpdateQuery:
        """
        >>> .update(Schema)
        :param table:
        :return:
        """

    @overload
    def update(
            self,
            table: str,
    ) -> UpdateQuery:
        """
        >>> .update('table')
        :param table:
        :return:
        """

    @overload
    def update(
            self,
            table: Union[
                type[Schema],
                str,
            ],
    ) -> UpdateQuery:
        if isinstance(table, str):
            table = table
        elif issubclass(table, Schema):
            table = table.__table__
        else:
            raise NotImplementedError('No matching @overload found for `sqlx.update(...)`')

        return UpdateQuery(pool=self.pool, query=f'UPDATE {table}')
