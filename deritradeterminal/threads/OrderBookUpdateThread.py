from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager

class OrderBookUpdateThread(QThread):

    signeler = pyqtSignal(list, list, str, str) 

    def collectProcessData(self):

        try:
            
            config = ConfigManager.get_config()

            if len(config.tradeApis) >= 1:
                
                creds = list(config.tradeApis.values())[0]

                client = RestClient(creds[0], creds[1], ConfigManager.get_config().apiUrl)

                orderbook = client.getorderbook(ConfigManager.get_config().tradeInsturment) 

                indexPrice = client.index()['btc']

                self.signeler.emit(orderbook['bids'], orderbook['asks'], str(format(orderbook['mark'], '.2f')), str(format(indexPrice, '.2f')))

        except Exception as e:
            print(e)

    def __init__(self):
        QThread.__init__(self)


    def run(self):
        while True:
            self.collectProcessData()
