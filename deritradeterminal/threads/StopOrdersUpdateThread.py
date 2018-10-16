from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager

class StopOrdersUpdateThread(QThread):

    signeler = pyqtSignal(list) 

    orders = None

    def collectProcessData(self):

        try:

            config = ConfigManager.get_config()

            openOrders = []

            for x in config.tradeApis:

                client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)

                orders = client.getopenorders(ordertype="stop_market")

                if len(orders) >= 1:

                    for order in orders:

                        direction = ""
                        
                        if order['direction'] == "buy":
                            direction = "Long"
                        else:
                            direction = "Short"

                        openOrders.append([x, direction, str(order["quantity"]), str(format(order["stopPx"], '.2f')), order['orderId']])

            
            self.signeler.emit(openOrders)
            
        except Exception as e:
            print(e)

    def __init__(self):
        QThread.__init__(self)


    def run(self):
        while True:
            self.collectProcessData()
