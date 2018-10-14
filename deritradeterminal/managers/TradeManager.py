from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager


class TradeManager:

    @staticmethod
    def market_buy(accountid):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
        client.buy(ConfigManager.get_config().tradeInsturment, config.tradeApis[accountid][2], 0, "market")
        

    @staticmethod
    def market_sell(accountid):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
        client.sell(ConfigManager.get_config().tradeInsturment, config.tradeApis[accountid][2], 0, "market")

    @staticmethod
    def limit_buy(accountid, price):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
        client.buy(ConfigManager.get_config().tradeInsturment, config.tradeApis[accountid][2], float(price), "limit")

    @staticmethod
    def limit_sell(accountid, price):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
        client.sell(ConfigManager.get_config().tradeInsturment, config.tradeApis[accountid][2], float(price), "limit")


    @staticmethod
    def close_position(accountid):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)

        cposition = client.positions()

        if len(cposition) >= 1:

            if cposition[0]['size'] > 0:
                client.sell(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")
            else:
                client.buy(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")

    @staticmethod
    def cancel_open_orders(accountid):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
        client.cancelall()

    @staticmethod
    def cancel_open_order(accountid, orderid):
        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
        client.cancel(orderid)     

    @staticmethod
    def market_buy_all():
        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.market_buy(x)
            

    @staticmethod
    def market_sell_all():

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.market_sell(x)

    @staticmethod
    def limit_buy_all(price):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.limit_buy(x, price)

    @staticmethod
    def limit_sell_all(price):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.limit_sell(x, price)

    @staticmethod
    def close_all_positions():

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.close_position(x)

    @staticmethod
    def cancel_all_open_orders():

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.cancel_open_orders(x)

