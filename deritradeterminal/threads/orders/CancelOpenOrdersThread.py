from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager

class CancelOpenOrdersThread(QThread):

    signeler = pyqtSignal(bool,str,str) 

    def processOrder(self):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[self.accountid][0], config.tradeApis[self.accountid][1], ConfigManager.get_config().apiUrl)

            orders = client.getopenorders()

            for order in orders:
                client.cancel(order['orderId'])

            self.signeler.emit(True, "Cancel All Open Orders Success", "Closed All Open Orders On Account: " + str(self.accountid))

        except Exception as e:
        	
            self.signeler.emit(False, "Cancel Open Orders Error" , "Failed to cancel open orders on " + str(self.accountid) + "\n" + str(e))

    def __init__(self, accountid):
        QThread.__init__(self)
        self.accountid = accountid

    def run(self):
        self.processOrder()
