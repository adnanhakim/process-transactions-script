"""
services.zerodhaservice
~~~~~~~~~~~~~~

This module contains a class to process Zerodha transactions

"""

from argparse import Namespace
from decimal import Decimal
import logging
from typing import Self

from enums.AssetType import AssetType
from enums.TransactionType import TransactionType
from models.Transaction import Transaction
from models.TransactionRow import TransactionRow
from services.TransactionService import TransactionService
from utils.dates import get_timestamp, to_datetime


class ZerodhaService(TransactionService):
    """Class to process Zerodha transactions"""

    _FIRST_ROW: int = 15
    _NAME_COL: int = 1
    _BUY_SELL_COL: int = 7
    _DATE_COL: int = 3
    _QTY_COL: int = 9
    _PRICE_COL: int = 10
    _DATE_FORMAT: str = "%Y-%m-%d"

    def __init__(self: Self, args: Namespace) -> None:
        output_filename: str | None = args.output_filename
        if output_filename is None:
            output_filename: str = "zerodha_output_" + get_timestamp() + ".xlsx"

        super().__init__(
            self._FIRST_ROW,
            self._NAME_COL,
            self._DATE_COL,
            self._QTY_COL,
            self._PRICE_COL,
            self._DATE_FORMAT,
            args.input_filename,
            output_filename,
            AssetType.MUTUAL_FUND,
        )

    def _create_txn_row_map(
        self: Self, txn_rows: list[TransactionRow]
    ) -> dict[str : list[TransactionRow]]:
        txn_row_map: dict[str : list[TransactionRow]] = {}

        for txn in txn_rows[self._FIRST_ROW :]:
            if txn[self._QTY_COL] is None or txn[self._QTY_COL] == 0:
                continue

            name: str = txn[self._NAME_COL].strip()

            txn_row = TransactionRow(
                buy_sell=TransactionType(txn[self._BUY_SELL_COL].upper()),
                qty=Decimal(str(txn[self._QTY_COL])),
                date=to_datetime(txn[self._DATE_COL], self._DATE_FORMAT),
                price=Decimal(str(txn[self._PRICE_COL])),
            )

            if name in txn_row_map:
                txn_row_map[name].append(txn_row)
            else:
                txn_row_map[name] = [txn_row]

        return txn_row_map

    def _get_buy_txns(
        self: Self, transaction_rows: list[TransactionRow]
    ) -> list[TransactionRow]:
        buy_txns: list[TransactionRow] = []

        i: int = 0
        while i < len(transaction_rows):
            if transaction_rows[i].buy_sell == TransactionType.SELL:
                i += 1
                continue

            qty: Decimal = transaction_rows[i].qty
            j: int = i + 1

            while (
                j < len(transaction_rows)
                and transaction_rows[i].buy_sell == transaction_rows[j].buy_sell
                and transaction_rows[i].date == transaction_rows[j].date
                and transaction_rows[i].price == transaction_rows[j].price
            ):
                qty += transaction_rows[j].qty
                j += 1

            if i != j + 1:
                transaction_rows[i].qty = qty

            buy_txns.append(transaction_rows[i])

            i = j

        logging.debug("Found %s buy transactions", len(buy_txns))

        return buy_txns

    def _get_sell_txns(
        self: Self, transaction_rows: list[TransactionRow]
    ) -> list[TransactionRow]:
        sell_txns: list[TransactionRow] = []

        i: int = 0
        while i < len(transaction_rows):
            if transaction_rows[i].buy_sell == TransactionType.BUY:
                i += 1
                continue

            qty: Decimal = transaction_rows[i].qty
            j: int = i + 1

            while (
                j < len(transaction_rows)
                and transaction_rows[i].buy_sell == transaction_rows[j].buy_sell
                and transaction_rows[i].date == transaction_rows[j].date
                and transaction_rows[i].price == transaction_rows[j].price
            ):
                qty += transaction_rows[j].qty
                j += 1

            if i != j + 1:
                transaction_rows[i].qty = qty

            sell_txns.append(transaction_rows[i])

            i = j

        logging.debug("Found %s sell transactions", len(sell_txns))

        return sell_txns

    def _compress_buy_transactions(
        self: Self, transactions: list[Transaction]
    ) -> list[Transaction]:
        compressed_txns: list[Transaction] = []

        i: int = 0
        while i < len(transactions):
            qty: Decimal = transactions[i].qty
            j: int = i + 1

            while (
                j < len(transactions)
                and transactions[i].buy_date == transactions[j].buy_date
                and transactions[i].buy_price == transactions[j].buy_price
            ):
                qty += transactions[j].qty
                j += 1
                logging.debug("Compressed transactions for %s", transactions[i].name)

            if i != j + 1:
                transactions[i].qty = qty

            compressed_txns.append(transactions[i])

            i = j

        return compressed_txns
