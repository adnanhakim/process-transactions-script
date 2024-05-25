"""
models.transactionrow
~~~~~~~~~~~~~~

This module contains a TransactionRow model class.

"""

from datetime import datetime
from decimal import Decimal
from typing import Self


class TransactionRow:
    """A class representing a transaction row model"""

    _qty: Decimal
    _date: datetime
    _price: Decimal

    def __init__(
        self: Self,
        qty: Decimal,
        date: datetime,
        price: Decimal,
    ) -> None:

        self._qty = qty
        self._date = date
        self._price = price

    @property
    def qty(self: Self) -> Decimal:
        return self._qty

    @property
    def date(self: Self) -> datetime:
        return self._date

    @property
    def price(self: Self) -> Decimal:
        return self._price

    def __str__(self):
        attrs: str = ", ".join([f"{key}={value}" for key, value in vars(self).items()])
        return "{" + attrs + "}"
