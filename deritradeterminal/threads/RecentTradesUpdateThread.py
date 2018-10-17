import datetime

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager

class RecentTradesUpdateThread(QThread):

    signeler = pyqtSignal(list) 

    def collectProcessData(self):

        try:
            config = ConfigManager.get_config()

            if len(config.tradeApis) >= 1:
                
                creds = list(config.tradeApis.values())[0]

                client = RestClient(creds[0], creds[1], ConfigManager.get_config().apiUrl)

                lastTrades = client.getlasttrades(ConfigManager.get_config().tradeInsturment)

                tradeList = []

                for trade in lastTrades:

                    direction = ""
                    
                    if trade['direction'] == "buy":
                        direction = "Long"
                    else:
                        direction = "Short"

                    tradeList.append([direction, trade["price"], trade["quantity"],datetime.datetime.utcfromtimestamp(trade["timeStamp"]/1000).strftime('%Y-%m-%d %H:%M:%S')])

                self.signeler.emit(tradeList)
                
        except Exception as e:
            print(e)

    def __init__(self):
        QThread.__init__(self)


    def run(self):
        while True:
            self.collectProcessData()
