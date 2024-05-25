"""
models.transactionrow
~~~~~~~~~~~~~~

This module contains a TransactionRow model class.

"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Self

from enums.TransactionType import TransactionType


class TransactionRow:
    """A class representing a transaction row model"""

    _buy_sell: TransactionType | None
    _qty: Decimal
    _date: datetime
    _price: Decimal

    def __init__(
        self: Self,
        qty: Decimal,
        date: datetime,
        price: Decimal,
        buy_sell: Optional[TransactionType] = None,
    ) -> None:
        self._buy_sell = buy_sell
        self._qty = qty
        self._date = date
        self._price = price

    @property
    def buy_sell(self: Self) -> TransactionType | None:
        return self._buy_sell

    @property
    def qty(self: Self) -> Decimal:
        return self._qty

    @qty.setter
    def qty(self: Self, qty: Decimal) -> Decimal:
        self._qty = qty

    @property
    def date(self: Self) -> datetime:
        return self._date

    @property
    def price(self: Self) -> Decimal:
        return self._price

    def __repr__(self):
        attrs: str = ", ".join([f"{key}={value}" for key, value in vars(self).items()])
        return "{" + attrs + "}"
