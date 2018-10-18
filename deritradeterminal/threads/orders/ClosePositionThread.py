from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager

class ClosePositionThread(QThread):

    signeler = pyqtSignal(bool,str,str) 

    def processOrder(self):

        try:
            config = ConfigManager.get_config()

            client = RestClient(config.tradeApis[self.accountid][0], config.tradeApis[self.accountid][1], ConfigManager.get_config().apiUrl)

            cposition = client.positions()

            if len(cposition) >= 1:

                if cposition[0]['size'] > 0:
                    client.sell(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")
                else:
                    client.buy(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")

        
            self.signeler.emit(True, "Close Position Success", "Closed Position On Account: " + str(self.accountid))

        except Exception as e:
        	
            self.signeler.emit(False, "Close Position Error" , "Failed to close position on " + str(self.accountid) + "\n" + str(e))

    def __init__(self, accountid):
        QThread.__init__(self)
        self.accountid = accountid

    def run(self):
        self.processOrder()
