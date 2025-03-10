from typing import Union, overload

from ._vendor import VendorBase
from ..queries import CountQuery
from ...types import Schema


class CountVendor(VendorBase):
    @overload
    def count(
            self,
            table: type[Schema],
    ) -> CountQuery:
        """
        >>> .count(Schema)
        :param table:
        :return:
        """

    @overload
    def count(
            self,
            table: str,
    ) -> CountQuery:
        """
        >>> .count('table')
        :param table:
        :return:
        """

    def count(
            self,
            table: Union[
                type[Schema],
                str,
            ],
    ) -> CountQuery:
        if isinstance(table, str):
            ...
        elif table := getattr(table, '__table__', None):
            ...
        else:
            raise NotImplementedError('No matching @overload found for `sqls.update(...)`')

        return CountQuery(pool=self.pool, query=f'SELECT COUNT(*) AS `total` FROM `{table}`')
