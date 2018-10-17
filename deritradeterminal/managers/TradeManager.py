from deritradeterminal.util.Util import Util
from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager


class TradeManager:

    @staticmethod
    def market_buy(parent, accountid, amount):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
            client.buy(ConfigManager.get_config().tradeInsturment, float(amount), 0, "market")
        
        except Exception as e:
            Util.show_error_dialog(parent, "Market Buy Order Error" , "Failed to market buy on " + str(accountid) + " for amount: " + str(amount) + "\n" + str(e))

    @staticmethod
    def market_sell(parent, accountid, amount):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
            client.sell(ConfigManager.get_config().tradeInsturment, float(amount), 0, "market")

        except Exception as e:
            Util.show_error_dialog(parent, "Market Sell Order Error" , "Failed to market sell on " + str(accountid) + " for amount: " + str(amount) + "\n" + str(e))

    @staticmethod
    def stop_market_buy(parent, accountid, price, amount):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
            client.buy_stop_market_order(ConfigManager.get_config().tradeInsturment, float(amount), price)

        except Exception as e:
            Util.show_error_dialog(parent, "Stop Market Buy Order Error" , "Failed to stop market buy on " + str(accountid) + " for amount: " + str(amount) + "\n" + str(e))        

    @staticmethod
    def stop_market_sell(parent, accountid, price, amount):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
            client.sell_stop_market_order(ConfigManager.get_config().tradeInsturment, float(amount), price)

        except Exception as e:
            Util.show_error_dialog(parent, "Stop Market Sell Order Error" , "Failed to stop market sell on " + str(accountid) + " for amount: " + str(amount) + "\n" + str(e))      

    @staticmethod
    def limit_buy(parent, accountid, price, amount):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
            client.buy(ConfigManager.get_config().tradeInsturment, float(amount), float(price), "limit")
        
        except Exception as e:
            Util.show_error_dialog(parent, "Limit Buy Order Error" , "Failed to limit buy on " + str(accountid) + " for amount: " + str(amount) + "\n" + str(e))      

    @staticmethod
    def limit_sell(parent, accountid, price, amount):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
            client.sell(ConfigManager.get_config().tradeInsturment, float(amount), float(price), "limit")

        except Exception as e:
            Util.show_error_dialog(parent, "Limit Sell Order Error" , "Failed to limit sell on " + str(accountid) + " for amount: " + str(amount) + "\n" + str(e))   

    @staticmethod
    def close_position(parent, accountid):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)

            cposition = client.positions()

            if len(cposition) >= 1:

                if cposition[0]['size'] > 0:
                    client.sell(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")
                else:
                    client.buy(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")

        except Exception as e:
            Util.show_error_dialog(parent, "Close Position Error" , "Failed to close position on " + str(accountid) + "\n" + str(e))

    @staticmethod
    def cancel_open_orders(parent, accountid):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
            client.cancelall()
        
        except Exception as e:
            Util.show_error_dialog(parent, "Cancel Open Orders Error" , "Failed to cancel open orders on " + str(accountid) + "\n" + str(e))

    @staticmethod
    def cancel_open_stop_orders(parent, accountid):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
            orders = client.getopenorders(ordertype="stop_market")

            for order in orders:
                client.cancel(order['orderId'])
        
        except Exception as e:
            Util.show_error_dialog(parent, "Cancel Open Stop Orders Error" , "Failed to cancel open stop orders on " + str(accountid) + "\n" + str(e))

    @staticmethod
    def cancel_open_order(parent, accountid, orderid):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[accountid][0], config.tradeApis[accountid][1], ConfigManager.get_config().apiUrl)
            client.cancel(orderid)

        except Exception as e:
            Util.show_error_dialog(parent, "Cancel Open Order Error" , "Failed to cancel open order id: "+ str(orderid)+" on " + str(accountid) + "\n" + str(e))

    @staticmethod
    def market_buy_all(parent, amount):
        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.market_buy(parent, x, amount)
            

    @staticmethod
    def market_sell_all(parent):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.market_sell(parent, x, amount)

    @staticmethod
    def stop_market_buy_all(parent, price, amount):
        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.stop_market_buy(parent, x, price, amount)
            

    @staticmethod
    def stop_market_sell_all(parent, price, amount):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.stop_market_sell(parent, x, price, amount)

    @staticmethod
    def limit_buy_all(parent, price, amount):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.limit_buy(parent, x, price, amount)

    @staticmethod
    def limit_sell_all(parent, price, amount):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.limit_sell(parent, x, price, amount)

    @staticmethod
    def close_all_positions(parent):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.close_position(parent, x)

    @staticmethod
    def cancel_all_open_orders(parent):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.cancel_open_orders(parent, x)

    @staticmethod
    def cancel_all_open_stop_orders(parent):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            TradeManager.cancel_open_stop_orders(parent, x)   

