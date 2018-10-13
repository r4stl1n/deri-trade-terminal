import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow

from deriui import Ui_MainWindow

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
 

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.util.RepeatedTimer import RepeatedTimer
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

                print(position)

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

class OrderBookUpdateThread(QThread):

    signeler = pyqtSignal(list, list, str) 

    def collectProcessData(self):

        config = ConfigManager.get_config()

        index = 0

        if len(config.tradeApis) > 1:
            
            creds = list(config.tradeApis.values())[0]

            client = RestClient(creds[0], creds[1], ConfigManager.get_config().apiUrl)

            orderbook = client.getorderbook(ConfigManager.get_config().tradeInsturment) 

            self.signeler.emit(orderbook['bids'], orderbook['asks'], str(format(orderbook['mark'], '.2f')))

            index = index + 1

    def __init__(self):
        QThread.__init__(self)


    def run(self):
        while True:
            self.collectProcessData()

class MainWindow(QMainWindow, Ui_MainWindow):

    repeatedTask = None
    positionsThread = None

    def firstRun(self):
        config = ConfigManager.get_config()
        index = 0
        for x in config.tradeApis:
            self.currentPositionsTable.insertRow(index)
            index = index + 1

        self.currentPositionsTable.setColumnCount(5)

        index = 0
        for x in range(13):
            self.orderbookTable.insertRow(index)
            index = index + 1

        self.orderbookTable.setColumnCount(13)

        self.positionsThread = PositionsUpdateThread()
        self.orderbookThread = OrderBookUpdateThread()
        self.positionsThread.start()
        self.orderbookThread.start()

        self.positionsThread.signeler.connect(self.update_table)
        self.orderbookThread.signeler.connect(self.update_order_book)

        self.marketBuyButton.clicked.connect(self.do_market_buy_button)
        self.marketSellButton.clicked.connect(self.do_market_sell_button)
        self.closePositionButton.clicked.connect(self.do_close_positions)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.firstRun()

    def update_table(self, index, account, insturment, size, averageprice, pnl):
        self.currentPositionsTable.setItem(index,0,  QTableWidgetItem(account))
        self.currentPositionsTable.setItem(index, 1, QTableWidgetItem(insturment))
        self.currentPositionsTable.setItem(index, 2, QTableWidgetItem(size))
        self.currentPositionsTable.setItem(index, 3, QTableWidgetItem(averageprice))
        self.currentPositionsTable.setItem(index, 4, QTableWidgetItem(pnl))
        self.currentPositionsTable.update()

    def update_order_book(self, bids, asks, mark):
        cBids = bids[:6]
        cAsks = asks[:6][::-1]

        print(cBids)

        index = 0

        for ask in cAsks:
            self.orderbookTable.setItem(index, 0, QTableWidgetItem(str(ask['price'])))
            self.orderbookTable.setItem(index, 1, QTableWidgetItem(str(ask['quantity'])))
            self.orderbookTable.setItem(index, 2, QTableWidgetItem(str(ask['cm_amount'])))
            index = index + 1

        index = 7
        self.orderbookTable.setItem(6, 0, QTableWidgetItem("M: " + str(mark)))
        self.orderbookTable.setItem(6, 1, QTableWidgetItem(""))
        self.orderbookTable.setItem(6, 2, QTableWidgetItem("I: " + str(mark)))

        for bid in cBids:
            self.orderbookTable.setItem(index, 0, QTableWidgetItem(str(bid['price'])))
            self.orderbookTable.setItem(index, 1, QTableWidgetItem(str(bid['quantity'])))
            self.orderbookTable.setItem(index, 2, QTableWidgetItem(str(bid['cm_amount'])))
            index = index + 1

        self.orderbookTable.update()

    def do_market_buy_button(self):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)
            client.buy(ConfigManager.get_config().tradeInsturment, config.tradeApis[x][2], 0, "market")
            time.sleep(0.5)

    def do_market_sell_button(self):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)
            client.sell(ConfigManager.get_config().tradeInsturment, config.tradeApis[x][2], 0, "market")
            time.sleep(0.5)

    def do_close_positions(self):

        config = ConfigManager.get_config()

        for x in config.tradeApis:

            client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)

            cposition = client.positions()

            if len(cposition) >= 1:

                if cposition[0]['size'] > 0:
                    client.sell(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")
                else:
                    client.buy(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")

def main():
    ConfigManager.get_config()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()