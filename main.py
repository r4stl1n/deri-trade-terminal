import sys
import threading

from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from deriui import Ui_MainWindow

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from deritradeterminal.util.Util import Util

from deritradeterminal.util.QDarkPalette import QDarkPalette

from deritradeterminal.managers.TradeManager import TradeManager
from deritradeterminal.managers.ConfigManager import ConfigManager

from deritradeterminal.threads.OrdersUpdateThread import OrdersUpdateThread
from deritradeterminal.threads.OrderBookUpdateThread import OrderBookUpdateThread
from deritradeterminal.threads.PositionsUpdateThread import PositionsUpdateThread

class MainWindow(QMainWindow, Ui_MainWindow):

    repeatedTask = None
    positionsThread = None

    def firstRun(self):
        config = ConfigManager.get_config()
        index = 0

        for x in config.tradeApis:
            self.currentPositionsTable.insertRow(index)
            index = index + 1

            # Add options to the acction selection
            self.limitOrderComboBox.addItem(x)
            self.marketOrderComboBox.addItem(x)


        self.currentPositionsTable.setColumnCount(5)

        index = 0
        for x in range(13):
            self.orderbookTable.insertRow(index)
            index = index + 1

        self.orderbookTable.setRowCount(25)
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

        self.closeOrdersButton.clicked.connect(self.do_cancel_all_open_orders)

        self.webView = QtWebEngineWidgets.QWebEngineView(self)
        self.webView.setUrl(QtCore.QUrl("https://www.deribit.com/ftu_chart?instr=BTC-PERPETUAL"))
        self.webView.setObjectName("webView")

        self.horizontalLayout_4.addWidget(self.webView)
        self.horizontalLayout_4.removeWidget(self.placeHolderFrame)
        self.placeHolderFrame.deleteLater()



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

            cBids = bids[:12]
            cAsks = asks[:12][::-1]

            index = 0

            for ask in cAsks:
                self.orderbookTable.setItem(index, 0, QTableWidgetItem(str(ask['price'])))
                self.orderbookTable.setItem(index, 1, QTableWidgetItem(str(ask['quantity'])))
                self.orderbookTable.setItem(index, 2, QTableWidgetItem(str(ask['cm_amount'])))


                index = index + 1

            index = 13
            self.orderbookTable.setItem(12, 0, QTableWidgetItem("M: " + str(mark)))
            self.orderbookTable.setItem(12, 1, QTableWidgetItem(""))
            self.orderbookTable.setItem(12, 2, QTableWidgetItem("I: " + str(indexprice)))

            for bid in cBids:
                self.orderbookTable.setItem(index, 0, QTableWidgetItem(str(bid['price'])))
                self.orderbookTable.setItem(index, 1, QTableWidgetItem(str(bid['quantity'])))
                self.orderbookTable.setItem(index, 2, QTableWidgetItem(str(bid['cm_amount'])))

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

            selection = str(self.marketOrderComboBox.currentText())

            if selection == "All":

                threading.Thread(target=TradeManager.market_buy_all).start()

                Util.show_info_dialog(self, "Order Info", "Market Buy Executed On All Accounts")

            else:
                threading.Thread(target=TradeManager.market_buy, args=(selection,)).start()

                Util.show_info_dialog(self, "Order Info", "Market Buy Executed On Account " + selection)


        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_market_sell_button(self):

        try:

            selection = str(self.marketOrderComboBox.currentText())

            if selection == "All":

                threading.Thread(target=TradeManager.market_sell_all).start()

                Util.show_info_dialog(self, "Order Info", "Market Sell Executed On All Accounts")

            else:
                threading.Thread(target=TradeManager.market_sell, args=(selection,)).start()

                Util.show_info_dialog(self, "Order Info", "Market Sell Executed On Account " + selection)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_limit_buy_button(self):

        try:

            selection = str(self.limitOrderComboBox.currentText())

            if selection == "All":
                
                threading.Thread(target=TradeManager.limit_buy_all, args=(self.limitPriceInput.text(),)).start()
                
                Util.show_info_dialog(self, "Order Info", "Limit Buy Executed On All Accounts")

            else:
                
                threading.Thread(target=TradeManager.limit_buy, args=(selection, self.limitPriceInput.text(),)).start()

                Util.show_info_dialog(self, "Order Info", "Limit Buy Executed On Account " + selection)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_limit_sell_button(self):

        try:

            selection = str(self.limitOrderComboBox.currentText())

            if selection == "All":

                threading.Thread(target=TradeManager.limit_sell_all, args=(self.limitPriceInput.text(),)).start()

                Util.show_info_dialog(self, "Order Info", "Limit Sell Executed")

            else:

                threading.Thread(target=TradeManager.limit_sell, args=(selection, self.limitPriceInput.text(),)).start()

                Util.show_info_dialog(self, "Order Info", "Limit Sell Executed On Account " + selection)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_close_positions(self):

        try:

            selection = str(self.marketOrderComboBox.currentText())

            if selection == "All":

                threading.Thread(target=TradeManager.close_all_positions).start()
                
                Util.show_info_dialog(self, "Order Info", "All Positions On All Accounts Closed")

            else:

                threading.Thread(target=TradeManager.close_position, args=(selection,)).start()

                Util.show_info_dialog(self, "Order Info", "Position Closed on Account " + selection)

        except Exception as e:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage(str(e))


    def do_cancel_all_open_orders(self):

        try:
            
            threading.Thread(target=TradeManager.cancel_all_open_orders).start()

            Util.show_info_dialog(self, "Order Info", "All Open Orders On All Accounts Cancelled")

        except Exception as e:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage(str(e))

    def do_cancel_orders(slef):

        selection = str(self.marketOrderComboBox.currentText())

        threading.Thread(target=TradeManager.close_open_orders, args=(selection,)).start()

        Util.show_info_dialog(self, "Order Info", "All Open Orders On Account " + selection + " closed")

def main():
    ConfigManager.get_config()
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    
    dark_palette = QDarkPalette()

    dark_palette.set_app(app)


    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()