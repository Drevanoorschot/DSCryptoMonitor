import datetime


class DataSet:
    def __init__(self):
        self.exchanges: list[Exchange] = []
        self.trades: list[Trade] = []
        self.issues: list[Issue] = []

    def convert_to_dict(self):
        return {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'record': {
                'exchanges': list(map(lambda e: e.convert_to_dict(), self.exchanges)),
                'trades': list(map(lambda t: t.convert_to_dict(), self.trades)),
                'issues': list(map(lambda i: i.convert_to_dict(), self.issues))
            }
        }


class Exchange:

    def __init__(self, name: str):
        self.name: str = name
        self.coins: dict[str, Coin] = {}

    def add_coin(self, shorthand: str, value: float) -> None:
        coin = Coin(shorthand, value, self)
        self.coins[shorthand] = coin

    def convert_to_dict(self):
        return {
            "name": self.name,
            "coins": list(map(lambda c: c.convert_to_dict(), self.coins.values()))
        }


class Coin:
    def __init__(self, shorthand: str, value: float, exchange: Exchange):
        self.shorthand: str = shorthand
        self.exchange: Exchange = exchange
        self.value: float = value

    def convert_to_dict(self):
        return {
            "name": self.shorthand,
            "value": self.value
        }


class Trade:

    def __init__(self, buy: Coin, sell: Coin):
        self.buy: Coin = buy
        self.sell: Coin = sell

    @property
    def gain(self) -> float:
        return (self.sell.value - self.buy.value) / self.sell.value

    def convert_to_dict(self):
        return {
            "coin": self.buy.shorthand,
            "gain": self.gain,
            "buy": {
                "exchange": self.buy.exchange.name,
                "value": self.buy.value
            },
            "sell": {
                "exchange": self.sell.exchange.name,
                "value": self.sell.value
            }
        }


class Issue:
    def __init__(self, coin_shorthand: str, exchange_name: str, stack_trace: str):
        self.coin_shorthand: str = coin_shorthand
        self.exchange_name: str = exchange_name
        self.stack_trace: str = stack_trace

    def convert_to_dict(self):
        return {
            "coin": self.coin_shorthand,
            "exchange": self.exchange_name,
            "trace": self.stack_trace
        }
