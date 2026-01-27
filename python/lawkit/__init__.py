"""
lawkit - Statistical law analysis toolkit for fraud detection and data quality assessment

Example:
    import lawkit

    # Benford's law analysis
    data = [123, 456, 789, 1234, 5678]
    result = lawkit.law("benf", data)
    print(result)

    # Pareto analysis
    values = [100, 200, 300, 1000, 2000]
    result = lawkit.law("pareto", values)
    print(result)
"""

from ._lawkit import (
    law,
)

__all__ = [
    "law",
]
__version__ = "2.6.0"
