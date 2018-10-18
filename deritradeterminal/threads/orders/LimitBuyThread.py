from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager

class LimitBuyThread(QThread):

    signeler = pyqtSignal(bool,str,str) 

    def processOrder(self):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[self.accountid][0], config.tradeApis[self.accountid][1], ConfigManager.get_config().apiUrl)
            client.buy(ConfigManager.get_config().tradeInsturment, float(self.amount), float(self.price), "limit")
        
            self.signeler.emit(True, "Limit Order Success", "Limit Buy On Account: " + str(self.accountid) + " For Amount: " + str(self.amount) + " At Price: " + str(self.price))

        except Exception as e:
        	
            self.signeler.emit(False, "Limit Buy Order Error" , "Failed to limit buy on " + str(self.accountid) + " for amount: " + str(self.amount) + "\n" + str(e))      

    def __init__(self, accountid, price , amount):
        QThread.__init__(self)
        self.accountid = accountid
        self.price = price
        self.amount = amount

    def run(self):
        self.processOrder()
