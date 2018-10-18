from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager

class CancelOpenOrderThread(QThread):

    signeler = pyqtSignal(bool,str,str) 

    def processOrder(self):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[self.accountid][0], config.tradeApis[self.accountid][1], ConfigManager.get_config().apiUrl)

            client.cancel(self.orderid)

            self.signeler.emit(True, "Cancel Open Order Success", "Closed Open Order On Account: " + str(self.accountid) + " With id: " + str(self.orderid))

        except Exception as e:
        	
            self.signeler.emit(False, "Cancel Open Order Error" , "Failed to cancel open order id: "+ str(self.orderid)+" on " + str(self.accountid) + "\n" + str(e))

    def __init__(self, accountid, orderid):
        QThread.__init__(self)
        self.accountid = accountid
        self.orderid = orderid

    def run(self):
        self.processOrder()
