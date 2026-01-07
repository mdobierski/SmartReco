"""
Utility functions for pagination and scoring.
"""

import math
from typing import List, Tuple


def paginate(items: List, page: int, per_page: int) -> Tuple[List, int]:
    """
    Paginate a list of items.

    Args:
        items: List of items to paginate
        page: Current page number (1-indexed)
        per_page: Number of items per page

    Returns:
        Tuple of (page_items, total_pages)
    """
    total_pages = max(1, math.ceil(len(items) / per_page))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total_pages


def pick_page_size(total: int) -> int:
    """
    Determine appropriate page size based on total items.

    Args:
        total: Total number of items

    Returns:
        Page size (10, 15, or 20)
    """
    if total > 20:
        return 20
    if total > 15:
        return 15
    if total > 10:
        return 10
    return total or 1
