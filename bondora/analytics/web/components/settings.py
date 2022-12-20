# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Dataclass containing required settings."""
    name: str = "Bondora Analytics"
    host: str = "localhost"
    port: int = 8080
    debug: bool = True
    root: str = os.path.dirname(os.path.dirname(__file__).replace("\\", "/"))
    prefix: str = "bondora"
