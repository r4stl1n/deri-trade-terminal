from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager

class PositionsUpdateThread(QThread):

    signeler = pyqtSignal(int,str,str,str,str,str) 

    def collectProcessData(self):
        config = ConfigManager.get_config()

        index = 0

        for x in config.tradeApis:

            client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)

            cposition = client.positions()

            if len(cposition) >= 1:

                position = cposition[0]

                direction = ""
                
                if position['direction'] == "buy":
                    direction = "Long"
                else:
                    direction = "Short"

                self.signeler.emit(index, x, direction, str(position["size"]), str(format(position["averagePrice"], '.4f')), str(format(position["profitLoss"], '.8f')))

            else:
                self.signeler.emit(index, x, "No Position", "", "", "")

            index = index + 1

    def __init__(self):
        QThread.__init__(self)


    def run(self):
        while True:
            self.collectProcessData()