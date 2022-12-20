# -*- coding: utf-8 -*-
"""Create control elements."""

from typing import List
from pages.dashboard.controls import create_control


def create_controls(data: List) -> List:
    """Create controls required for dashboards.

    Args:
        data: Data.

    Returns:
        Controls.

    """
    controls = [
        create_control(data[0])
    ]
    return controls
