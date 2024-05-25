"""
enums.assettype
~~~~~~~~~~~~~~

This module contains an enum class with different types of assets.

"""

from enum import Enum


class AssetType(Enum):
    MUTUAL_FUND = "MF"
    STOCK = "Stock"
