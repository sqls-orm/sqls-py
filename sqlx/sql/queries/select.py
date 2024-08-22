from __future__ import annotations

from .. import mixin
from ...types import Schema


class SelectQuery[S: Schema](
    mixin.FromMixin,
    mixin.WhereMixin,
    mixin.OrderByMixin,
    mixin.LimitMixin,
    mixin.OffsetMixin,
):
    ...
    # @overload
    # def select(
    #         self,
    #         string: str,
    # ) -> Self:
    #     """
    #     >>> .select('COUNT(column) as count_column')
    #     >>> .select(f'COUNT({Schema.model().column}) as count_column')
    #     >>> .select({alias1: Schema.model().col1, alias2: Schema.model().col2})
    #     :param alias:
    #     :return:
    #     """
    #
    # @overload
    # def select(
    #         self,
    #         alias: dict[str, Union[Column, str]],
    # ) -> Self:
    #     """
    #     >>> .select({alias1: 'col1', alias2: 'col2'})
    #     >>> .select({alias1: Schema.model().col1, alias2: Schema.model().col2})
    #     :param alias:
    #     :return:
    #     """
    #
    # @overload
    # def select(
    #         self,
    #         *columns: Iterable[Union[Column, str]],
    # ) -> Self:
    #     """
    #     >>> .select('col1', 'col2')
    #     >>> .select(Schema.model().col1, Schema.model().col2)
    #     :param columns:
    #     :return:
    #     """
    #
    # @overload
    # def select(
    #         self,
    #         **alias: Union[Column, str],
    # ) -> Self:
    #     """
    #     >>> .select(alias1='col1', alias2='col2')
    #     >>> .select(alias1=Schema.model().col1, alias2=Schema.model().col2)
    #     :param alias:
    #     :return:
    #     """
    #
    # @overload
    # def select(
    #         self,
    #         *columns: Iterable[Union[Column, str]],
    #         **alias: Union[Column, str],
    # ) -> Self:
    #     """
    #     >>> .select('col1', Schema.model().col2, alias3='col3', alias4=Schema.model().col4)
    #     :param columns:
    #     :param alias:
    #     :return:
    #     """
    #
    # def select(
    #         self,
    #         *as_dict_or_args: Union[
    #             dict[str, Union[Column, str]],
    #             Iterable[Union[Column, str]]
    #         ],
    #         **alias: Union[Column, str],
    # ) -> Self:
    #     if as_dict_or_args:
    #         if isinstance(as_dict_or_args[0], dict) and alias:
    #             as_dict = as_dict_or_args | alias
    #             columns = ', '.join(f'`{column}` AS `{_alias}`' for _alias, column in as_dict.items())
    #         elif isinstance(as_dict_or_args[0], dict):
    #             as_dict = as_dict_or_args[0]
    #             columns = ', '.join(f'`{column}` AS `{_alias}`' for _alias, column in as_dict.items())
    #         else:  # Union[Column, str]
    #             as_args = as_dict_or_args
    #             columns = ', '.join(f'`{column}`' for column in as_args)
    #     elif alias:
    #         as_dict = alias
    #         columns = ', '.join(f'`{column}` AS `{alias}`' for alias, column in as_dict.items())
    #     else:
    #         columns = '*'
    #
    #     self._query.update(f'SELECT {columns}')
    #
    #     return self
