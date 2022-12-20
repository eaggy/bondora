# -*- coding: utf-8 -*-
"""I/O functions."""

import json
import configparser
import pandas as pd
from bondora.utils.paths import get_path_settings, get_path_transactions
from bondora.api.bondora_api import BondoraApi


def load_transactions() -> pd.DataFrame:
    with open(get_path_transactions(), "r") as handle:
        return pd.DataFrame(json.loads(handle.read()))


def save_transactions():
    config = configparser.ConfigParser()
    config.read_file(open(get_path_settings()))
    token = config.get("BONDORA", "TOKEN")
    api = BondoraApi(token)
    transactions_list = []
    idx = 1
    while True:
        transactions = api.get_investments_all(False,
                                               SalesStatus=1,
                                               IsInRepayment=True,
                                               PageSize=50000,
                                               PageNr=idx)
        idx += 1
        if transactions["Success"]:
            if transactions["Count"] > 0:
                transactions_list.extend(transactions["Payload"])
            else:
                break
        else:
            break
    if transactions_list:
        with open(get_path_transactions(), "w") as handle:
            handle.write(json.dumps(transactions_list))
