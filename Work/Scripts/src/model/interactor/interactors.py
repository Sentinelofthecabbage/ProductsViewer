# -*- coding: utf-8 -*-

""" PyLinter Sublime Text Plugin

    This is a Pylint plugin for Sublime Text.

    Copyright R. de Laat, Elit 2011-2013

    For more information, go to https://github.com/biermeester/Pylinter#readme
"""
# Метод функция для получения средних цен по выбранным категориям
# продуктов и выбранному качеству

# Метод/функция на вход получает список групп продуктов и список категорий качества.
#   Исходя из входных данныx необходимо получить список средних цен
#   по каждой категории качества каждой группы вида
#   [[группа1-качество1, группа1-качество2], [группа2-качество1, группа2-качество2]]
import copy
import pickle

import os
import datetime
import time

import pandas
import pandas as pd

from Work.Scripts.src.controller.commands import CommandDelete, CommandUpdate, \
    CommandInsert, CommandSelect
from Work.Scripts.src.controller.key_words import CompareOp
from Work.Scripts.src.model.repository.DB_constants import TableName
from Work.Scripts.src.model.repository.interf_extractor import IDataExtractor


class MainTableInteractor:
    extractor: IDataExtractor

    def __init__(self, extractor: IDataExtractor):
        self.extractor = extractor

    def get_data(self):
        return self.get_main_table()

    def get_main_table(self):
        """
        Author: Suleymanov Nail
        Function returns list of lists that contain all needed information for main table
        as: product_id,product_name,product_price,product_producer,product_group,dicsount, quality
        Return[0]==list of headers for table
        """
        # result = [] * 1
        # result.append(list(self._db_products.columns))
        main_table: pandas.DataFrame = self.extractor._db_products.copy()

        def is_discount_works(discount_id: int):
            now = time.mktime(datetime.datetime.now().timetuple())
            date_begin = time.mktime(datetime.datetime.strptime(
                self.extractor._db_discounts['date_begin'].iloc[discount_id],
                "%d.%m.%Y").timetuple())
            date_end = time.mktime(
                datetime.datetime.strptime(
                    self.extractor._db_discounts['date_end'].iloc[
                        discount_id],
                    "%d.%m.%Y").timetuple())
            return date_begin <= now <= date_end

        discount_list = self.extractor._db_discounts.id.copy()

        for i in range(len(discount_list)):
            if is_discount_works(discount_list.iloc[i]):
                main_table.loc[main_table.discount_id == discount_list.iloc[
                    i], 'discount_id'] = \
                self.extractor._db_discounts.amount.iloc[i]
            else:
                main_table.discount_id.loc[
                    main_table.discount_id == discount_list.iloc[i]] = 0

        main_table.price *= round((1 - main_table.discount_id / 100.0), 2)
        main_table = main_table.rename(columns={
            'id': 'Id',
            'name': 'Product name',
            'price': 'Price',
            'producer_name': 'Producer name',
            'group_name': 'Category',
            'discount_id': 'Discount',
            'quality': 'Quality'
        })
        return main_table

    df = pd.DataFrame()
    select_df = pd.DataFrame()

    def __init__(self, extractor: IDataExtractor):
        self.extractor = extractor
        self.df = self.get_data()
        self.selector = CommandSelect(TableName.PRODUCTS.value)

    def get_data(self):
        return self.extractor.get_data()

    def set_data(self, data: pd.DataFrame):
        self.df = data

    def select(self, command_select: CommandSelect = None):
        if not (command_select is None):
            self.selector = command_select
        drop_list = [item for item in self.df.columns.values if item not in
                     self.selector.get_columns()]
        self.select_df = self.df.drop(drop_list, axis=1)
        for col, op, val in self.selector.items():
            self.select_df = self.select_df[self._filter(
                self.select_df, col, op, val)]
        return self.select_df

    @staticmethod
    def _filter(df: pd.DataFrame, field, compare_op: str,
                value, reverse=False):
        def get_type_of(series: pd.Series):
            if series.array:
                try:
                    float(series.array[0])
                    float(value)
                    return float
                except:
                    return str
            return None

        def reverse_op(op):
            return {
                CompareOp.EQUAL.value: CompareOp.NOT_EQUAL.value,
                CompareOp.NOT_EQUAL.value: CompareOp.EQUAL.value,
                CompareOp.LESS.value: CompareOp.MORE_OR_EQUAL.value,
                CompareOp.LESS_OR_EQUAL.value: CompareOp.MORE.value,
                CompareOp.MORE.value: CompareOp.LESS_OR_EQUAL.value,
                CompareOp.MORE_OR_EQUAL.value: CompareOp.LESS.value
            }[op]

        data_type = get_type_of(df[field])
        value = data_type(value)
        field_val = df[field].astype(data_type)
        if reverse:
            compare_op = reverse_op(compare_op)
        return {
            CompareOp.EQUAL.value: field_val == value,
            CompareOp.NOT_EQUAL.value: field_val != value,
            CompareOp.LESS.value: field_val < value,
            CompareOp.LESS_OR_EQUAL.value: field_val <= value,
            CompareOp.MORE.value: field_val > value,
            CompareOp.MORE_OR_EQUAL.value: field_val >= value
        }[compare_op]

    def insert(self, command_insert: CommandInsert):
        row = command_insert.get_row()
        self.df = self.df.append(row, ignore_index=True)
        return row.values()

    def update(self, command_update: CommandUpdate):
        command_update.get_values()
        for col, op, val in command_update.items():
            for field, set_val in command_update.get_values().items():
                self.df.loc[self._filter(
                    self.df, col, op, val
                ), field] = set_val
        return self.select(self.selector)

    def delete(self, command_delete: CommandDelete):
        for col, op, val in command_delete.items():
            self.df = self.df[self._filter(self.df, col, op, val, True)]
        return self.select(self.selector)

    def get_vals_by_col(self, column: str):
        vals = list(set(self.df[column].tolist()))
        vals.sort()
        return vals

    def get_db_copy(self):
        return copy.deepcopy(self.df)


class ReportsInteractor:
    """
    docstring
    """
    extractor: IDataExtractor

    def __init__(self, extractor: IDataExtractor):
        self.extractor = extractor

    def get_prices_by_group_and_quality(self, groups: list, qualities: list):
        """Author: Suleymanov Nail
        output: result,qualities
        result={
            'group1': [q1_value,q2_value,q3_value...],
            ...
        }
        qualities=['q1','q2',...]

        """
        products_table = self.extractor._db_products
        result = products_table[(products_table.group_name.isin(groups)) & (
            products_table.quality.isin(qualities))].groupby(
            ['group_name', 'quality'])['price'].mean()
        return result

    def get_prices_by_group(self, product_group: str, products: list):
        """Author: Suleymanov Nail
        output: result
        result=[
            {'product[i].name': price[i] },
            ...
        ]
        product[i] is in products and have product[i].group_name == product_group

        """
        result = {}
        table = self.extractor._db_products
        result = table[(table.group_name == product_group)
                       & (table.name.isin(products))].copy()[['name', 'price']]
        return result

    def get_products_groups(self):
        return self.extractor._db_groups["name"]

    def get_products_by_group(self, group: str):
        db_products = self.extractor._db_products
        return db_products[db_products["group_name"] == group]["name"]

    def get_box_and_whisker_prices(self, product_group: str, qualities: list,
                                   products: list):
        """Author: Suleymanov Nail
        output: result
        I forgot for what it was created but it works !=)

        """

        def get_quality_pos(quality: str, quality_list: str):
            for i, item in enumerate(quality_list):
                if quality == item:
                    return i
            return None

        database: pandas.DataFrame = self.extractor._db_products
        result = {}
        list_of_list = [None] * len(qualities)
        for i, item in enumerate(list_of_list):
            item = []

        result = result.fromkeys(qualities, [])
        for i in range(len(database)):
            if (database.iloc[i]['name'] in products) and (
                    database.iloc[i]['quality'] in qualities) and (
                    database.iloc[i]['group_name'] == product_group):
                current_quality_pos = get_quality_pos(
                    database.iloc[i]['quality'], qualities)
                list_of_list[current_quality_pos].append(
                    int(database.iloc[i]['price']))
        for i, item in enumerate(list_of_list):
            result[qualities[i]] = item

        return result

    def get_spreading(self, product_group: str, date: str):
        """Author: Suleymanov Nail
        output: result
        Return information about amount of sold production of product_group and price
        in DD.MM.YYYY date
        Return =[
            {'price': price of 1 object,
             'amount': amount of this product},
            ...
        ]

        """
        vouchers = self.extractor._db_vouchers[
            self.extractor._db_vouchers.date == date]
        sales = self.extractor._db_sales[
            self.extractor._db_sales.check_id.isin(vouchers.id)]

        result = sales.groupby(['products_id'])['amount'].sum()

        # оставить только элементы подходящего типа продукции
        for i in result.keys().tolist():
            if list(self.extractor._db_products[
                        self.extractor._db_products.id == i].group_name)[
                0] != product_group:
                result = result.drop(i)
            else:
                # result[i] *= int(
                #     self._db_products[self._db_products.id == i].price)
                result = result.rename({
                    i: list(self.extractor._db_products[
                                self.extractor._db_products.id == i]['price'])[
                        0]
                })
        return result

    def get_groups_list(self):
        """Author: Suleymanov Nail
        Returns list of products groups

        """
        return list(self.extractor._db_groups['name'])

    def get_quality_list(self):
        """Author: Suleymanov Nail
        output: result
        Returns list of sorted products qualities

        """
        result = list(set(list(self.extractor._db_products['quality'])))
        result.sort()
        return result