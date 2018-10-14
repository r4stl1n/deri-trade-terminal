from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager


class TradeManager:

    @staticmethod
    def market_buy(exchangeid):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[exchangeid][0], config.tradeApis[exchangeid][1], ConfigManager.get_config().apiUrl)
        client.buy(ConfigManager.get_config().tradeInsturment, config.tradeApis[exchangeid][2], 0, "market")
        

    @staticmethod
    def market_sell(exchangeid):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[exchangeid][0], config.tradeApis[exchangeid][1], ConfigManager.get_config().apiUrl)
        client.sell(ConfigManager.get_config().tradeInsturment, config.tradeApis[exchangeid][2], 0, "market")

    @staticmethod
    def limit_buy(exchangeid, price):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[exchangeid][0], config.tradeApis[exchangeid][1], ConfigManager.get_config().apiUrl)
        client.buy(ConfigManager.get_config().tradeInsturment, config.tradeApis[exchangeid][2], float(price), "limit")

    @staticmethod
    def limit_sell(exchangeid, price):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[exchangeid][0], config.tradeApis[exchangeid][1], ConfigManager.get_config().apiUrl)
        client.sell(ConfigManager.get_config().tradeInsturment, config.tradeApis[exchangeid][2], float(price), "limit")


    @staticmethod
    def close_position(exchangeid):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[exchangeid][0], config.tradeApis[exchangeid][1], ConfigManager.get_config().apiUrl)

        cposition = client.positions()

        if len(cposition) >= 1:

            if cposition[0]['size'] > 0:
                client.sell(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")
            else:
                client.buy(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")

    @staticmethod
    def close_open_orders(exchangeid):

        config = ConfigManager.get_config()

        client = RestClient(config.tradeApis[exchangeid][0], config.tradeApis[exchangeid][1], ConfigManager.get_config().apiUrl)
        client.cancelall()

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

            TradeManager.close_open_orders(x)

