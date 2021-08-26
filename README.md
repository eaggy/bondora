# Bondora
Trading on [Bondora](https://www.bondora.com/en) marketplace including API, webhooks listener, and analytics.

Bondora as a leading Estonian marketplace for peer-to-peer consumer lending has a well-established secondary market and provides historical data on all secondary market transactions in a transparent way.

## Usage
### Installation
TO DO

### Project structure
The project is organized as follows:
```
.
├── analytics
│   └── loader.py
├── api
│   ├── bondora_api.py
│   └── urls.py
├── examples
│   ├── offer_green_loans.py
│   ├── offer_red_loans.py
│   └── reset_webhooks.py
├── hooks
│   ├── application.py
│   ├── hooks.wsgi
│   └── listener.py
├── trading
│   └── bondora_trading.py
├── settings.cfg
└── setup_logger.py
```
* The folder `analytics` contains analytical tools:
  * `loader.py` - Python class to load the resale statistic from Internet, process it, and save to a file
* The folder `api` contains a low-level Python wrapper of the official Bondora API:
  * `bondora_api.py` - Python wrapper class
  * `urls.py` - collection of API endpoints
* The folder `examples` contains a few examples of using this project:
  * `offer_green_loans.py` - how to offer current (green) loans for selling on the secondary market
  * `offer_red_loans.py` - how to offer defaulted (red) loans for selling on the secondary market
  * `reset_webhooks.py` - how to unblock a webhook endpoint, if it has been blocked by Bondora. Bondora blocs a webhook endpoint after generating 25 errors as a response to the POST request.
* The folder `hooks` contains functionality required for receiving and proceeding webhook notifications from Bondora:
  * `application.py` - Python class to communicate with the Bondora API web interface
  * `hooks.wsgi` - *mod_wsgi* application file
  * `listener.py` - webhook listener
* The folder `trading` contains functionality for trading using the Bondora API:
  * `bondora_trading.py` - high-level Python class for trading

* `settings.cfg` - project settings file
* `setup_logger.py` - logger class

### Functionality
#### API
The following resources of the official Bondora API are currently implemented in **BondoraApi** class at `./api/bondora_api.py`:
| API Endpoint | Method | Description |
| ------------ | ------------ | ------------ |
| GET [api/v1/account/balance](https://api.bondora.com/doc/Api/GET-api-v1-account-balance?v=1) | get_balance | Get account balance information |
| GET [api/v1/account/investments](https://api.bondora.com/doc/Api/GET-api-v1-account-investments?v=1) | get_investments | Get list of investments |
| GET [api/v1/eventlog](https://api.bondora.com/doc/Api/GET-api-v1-eventlog?v=1) | get_eventlog | Get events that have been made with this application |
| GET [api/v1/auctions](https://api.bondora.com/doc/Api/GET-api-v1-auctions?v=1) | get_auctions | Get list of active auctions |
| POST [api/v1/bid](https://api.bondora.com/doc/Api/POST-api-v1-bid?v=1) | bid_on_auction | Make bid into auctions |
| GET [api/v1/secondarymarket](https://api.bondora.com/doc/Api/GET-api-v1-secondarymarket?v=1) | get_secondarymarket | Get list of active secondary market items |
| GET [api/v1/loanpart/list](https://api.bondora.com/doc/Api/GET-api-v1-loanpart-list?v=1) | get_loanparts | Get loan part info |
| POST [api/v1/secondarymarket/buy](https://api.bondora.com/doc/Api/POST-api-v1-secondarymarket-buy?v=1) | buy_on_secondarymarket | Buy loans from secondary market |
| POST [api/v1/secondarymarket/sell](https://api.bondora.com/doc/Api/POST-api-v1-secondarymarket-sell?v=1) | sell_on_secondarymarket | Sell loans on secondary market |
| POST [api/v1/secondarymarket/cancel](https://api.bondora.com/doc/Api/POST-api-v1-secondarymarket-cancel?v=1) | cancel_on_secondarymarket | Cancel sale of loans offered on secondary market |

#### Trading
The following high-level trading methods are currently implemented in **BondoraTrading** class at `./trading/bondora_trading.py`:
| Method | Description |
| ------------ | ------------ |
| bid_loan | Make bid into specified auction |
| buy_green_loan | Buy green loan on secondary market, if buying conditions are satisfied |
| buy_red_loan | Buy red loan on secondary market, if buying conditions are satisfied |
| cancel_sm_offers | Cancel selling of own loans offered on secondary market |
| place_sm_offers | Place loans for selling on secondary market |


#### Hooks
##### `listener.py`
Listen to webhooks and execute the methods buy_red_loan and buy_green_loan from the **BondoraTrading** class.
##### `application.py`
The following methods are currently implemented:
| Method | Description |
| ------------ | ------------ |
| get_webhooks | Log into Bondora's API web interface and get list of webhooks |
| reset_webhooks | Reset webhooks, if the number of failures are above threshold |

#### Examples
##### `offer_green_loans.py`
Example how to offer for selling current (green) loans on bondora's secondary market. The loans are initially offered with a max_price (gain of 5% in this example). If a min_price (0% in this example) is provided, the selling price will be reduced daily by 1% to reach the min_price two day before the next planned payment.
Bondora token must be provided in `settings.cfg` to run this example.
##### `offer_red_loans.py`
Example how to offer for selling defaulted (red) loans on bondora's secondary market. Only the defaulted loans without any payments within last 12 months and with the latest debt management stage type of write off will be offered with a discount of -80%.
Bondora token must be provided in `settings.cfg` to run this example.
##### `reset_webhooks.py`
Example how to reset webhook errors via web interface, if the current number of errors is above the threshold (5 in this example). It can be used to unblock a webhook endpoint.
Bondora username, password, and application ID must be provided in `settings.cfg` to run this example.

## Important Risk Disclosure
Any investment carries the risk of a total loss of the invested amount or even to additional payments. Therefore, it is not suitable for everyone. Any decision for a particular investment should be based solely on your own trading objectives. The usage of this trading system is at your own risk!

## License
MIT License
