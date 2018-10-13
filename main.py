import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow

from deriui import Ui_MainWindow

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
 

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

class OrdersUpdateThread(QThread):

    signeler = pyqtSignal(list) 

    orders = None

    def collectProcessData(self):

        config = ConfigManager.get_config()

        openOrders = []

        for x in config.tradeApis:

            client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)

            orders = client.getopenorders()

            if len(orders) >= 1:

                for order in orders:

                    direction = ""
                    
                    if order['direction'] == "buy":
                        direction = "Long"
                    else:
                        direction = "Short"

                    openOrders.append([x, direction, str(order["quantity"]), str(format(order["price"], '.2f'))])

        
        self.signeler.emit(openOrders)

    def __init__(self):
        QThread.__init__(self)


    def run(self):
        while True:
            self.collectProcessData()

class OrderBookUpdateThread(QThread):

    signeler = pyqtSignal(list, list, str, str) 

    def collectProcessData(self):

        config = ConfigManager.get_config()

        index = 0

        if len(config.tradeApis) > 1:
            
            creds = list(config.tradeApis.values())[0]

            client = RestClient(creds[0], creds[1], ConfigManager.get_config().apiUrl)

            orderbook = client.getorderbook(ConfigManager.get_config().tradeInsturment) 

            indexPrice = client.index()['btc']

            self.signeler.emit(orderbook['bids'], orderbook['asks'], str(format(orderbook['mark'], '.2f')), str(format(indexPrice, '.2f')))

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
        self.openOrderTable.setColumnCount(4)

        self.positionsThread = PositionsUpdateThread()
        self.orderbookThread = OrderBookUpdateThread()
        self.openOrderThread = OrdersUpdateThread()
        
        self.positionsThread.start()
        self.orderbookThread.start()
        self.openOrderThread.start()

        self.positionsThread.signeler.connect(self.update_table)
        self.orderbookThread.signeler.connect(self.update_order_book)
        self.openOrderThread.signeler.connect(self.update_orders)

        self.marketBuyButton.clicked.connect(self.do_market_buy_button)
        self.marketSellButton.clicked.connect(self.do_market_sell_button)

        self.closePositionButton.clicked.connect(self.do_close_positions)
        self.closePositionButton2.clicked.connect(self.do_close_positions)

        self.limitBuyButton.clicked.connect(self.do_limit_buy_button)
        self.limitSellButton.clicked.connect(self.do_limit_sell_button)

        self.closeOrdersButton.clicked.connect(self.do_close_orders)

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

    def update_order_book(self, bids, asks, mark, indexprice):
        try:

            cBids = bids[:6]
            cAsks = asks[:6][::-1]

            index = 0

            for ask in cAsks:
                self.orderbookTable.setItem(index, 0, QTableWidgetItem(str(ask['price'])))
                self.orderbookTable.setItem(index, 1, QTableWidgetItem(str(ask['quantity'])))
                self.orderbookTable.setItem(index, 2, QTableWidgetItem(str(ask['cm_amount'])))

                self.orderbookTable.item(index, 0).setBackground(QColor(254,245,245))
                self.orderbookTable.item(index, 1).setBackground(QColor(254,245,245))
                self.orderbookTable.item(index, 2).setBackground(QColor(254,245,245))

                index = index + 1

            index = 7
            self.orderbookTable.setItem(6, 0, QTableWidgetItem("M: " + str(mark)))
            self.orderbookTable.setItem(6, 1, QTableWidgetItem(""))
            self.orderbookTable.setItem(6, 2, QTableWidgetItem("I: " + str(indexprice)))

            for bid in cBids:
                self.orderbookTable.setItem(index, 0, QTableWidgetItem(str(bid['price'])))
                self.orderbookTable.setItem(index, 1, QTableWidgetItem(str(bid['quantity'])))
                self.orderbookTable.setItem(index, 2, QTableWidgetItem(str(bid['cm_amount'])))
                
                self.orderbookTable.item(index, 0).setBackground(QColor(245,251,248))
                self.orderbookTable.item(index, 1).setBackground(QColor(245,251,248))
                self.orderbookTable.item(index, 2).setBackground(QColor(245,251,248))

                index = index + 1

            self.orderbookTable.update()

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))

    def update_orders(self, orders):
        try:

            index = 0


            if len(orders) != self.openOrderTable.rowCount:
                self.openOrderTable.setRowCount(0)

                for x in range(len(orders)):
                    self.openOrderTable.insertRow(x)

                self.openOrderTable.setRowCount(len(orders))

            for order in orders:
                self.openOrderTable.setItem(index, 0, QTableWidgetItem(str(order[0])))
                self.openOrderTable.setItem(index, 1, QTableWidgetItem(str(order[1])))
                self.openOrderTable.setItem(index, 2, QTableWidgetItem(str(order[2])))
                self.openOrderTable.setItem(index, 3, QTableWidgetItem(str(order[3])))
                index = index + 1

            self.openOrderTable.update()

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))

    def do_market_buy_button(self):

        try:
            config = ConfigManager.get_config()

            for x in config.tradeApis:

                client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)
                client.buy(ConfigManager.get_config().tradeInsturment, config.tradeApis[x][2], 0, "market")
                time.sleep(0.5)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_market_sell_button(self):

        try:

            config = ConfigManager.get_config()

            for x in config.tradeApis:

                client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)
                client.sell(ConfigManager.get_config().tradeInsturment, config.tradeApis[x][2], 0, "market")
                time.sleep(0.5)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_limit_buy_button(self):

        try:

            config = ConfigManager.get_config()

            for x in config.tradeApis:

                client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)
                client.buy(ConfigManager.get_config().tradeInsturment, config.tradeApis[x][2], float(self.limitPriceInput.text()), "limit")
                time.sleep(0.5)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_limit_sell_button(self):

        try:

            config = ConfigManager.get_config()

            for x in config.tradeApis:

                client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)
                client.sell(ConfigManager.get_config().tradeInsturment, config.tradeApis[x][2], float(self.limitPriceInput.text()), "limit")
                time.sleep(0.5)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_close_positions(self):

        try:

            config = ConfigManager.get_config()

            for x in config.tradeApis:

                client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)

                cposition = client.positions()

                if len(cposition) >= 1:

                    if cposition[0]['size'] > 0:
                        client.sell(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")
                    else:
                        client.buy(ConfigManager.get_config().tradeInsturment, abs(cposition[0]['size']), 0, "market")

                    time.sleep(0.5)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))

    def do_close_orders(self):
        config = ConfigManager.get_config()

        for x in config.tradeApis:

            client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)
            client.cancelall()

def main():
    ConfigManager.get_config()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()