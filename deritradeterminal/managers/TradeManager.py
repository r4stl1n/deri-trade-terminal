from deritradeterminal.util.Util import Util
from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager


class TradeManager:

    @staticmethod
    def market_buy_all(parentlocation, amount):
        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.market_buy(parentlocation, x, amount)
            

    @staticmethod
    def market_sell_all(parentlocation, amount):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.market_sell(parentlocation, x, amount)

    @staticmethod
    def stop_market_buy_all(parentlocation, price, amount):
        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.stop_market_buy(parentlocation, x, price, amount)
            

    @staticmethod
    def stop_market_sell_all(parentlocation, price, amount):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.stop_market_sell(parentlocation, x, price, amount)

    @staticmethod
    def limit_buy_all(parentlocation, price, amount):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.limit_buy(parentlocation, x, price, amount)

    @staticmethod
    def limit_sell_all(parentlocation, price, amount):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.limit_sell(parentlocation, x, price, amount)

    @staticmethod
    def close_all_positions(parentlocation):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.close_position(parentlocation, x)

    @staticmethod
    def cancel_all_open_orders(parentlocation):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.cancel_open_orders(parentlocation, x)

    @staticmethod
    def cancel_all_open_stop_orders(parentlocation):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.cancel_open_stop_orders(parentlocation, x)   

