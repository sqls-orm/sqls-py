from typing import Any, Iterable

from sqlx.core.result import Result

from .count import CountVendor
from .insert import InsertVendor
from .upsert import UpsertVendor
from .select import SelectVendor
from .update import UpdateVendor
from .delete import DeleteVendor


class SQLVendor(
    InsertVendor,
    UpsertVendor,
    SelectVendor,
    CountVendor,
    UpdateVendor,
    DeleteVendor,
):
    def __call__(self, query: str, args: Iterable[Any] = ()) -> Result:
        """
        >>> sqlx('SELECT * FROM `table` WHERE id = %s;', (1, ))
        :param query:
        :param args:
        :return:
        """
        return Result(pool=self.pool, query=query, args=args)
