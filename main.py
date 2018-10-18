import sys

from functools import partial

from deriui import Ui_MainWindow

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWebEngineWidgets

from deritradeterminal.util.Util import Util
from deritradeterminal.util.QDarkPalette import QDarkPalette

from deritradeterminal.managers.ConfigManager import ConfigManager

from deritradeterminal.threads.OrdersUpdateThread import OrdersUpdateThread
from deritradeterminal.threads.OrderBookUpdateThread import OrderBookUpdateThread
from deritradeterminal.threads.PositionsUpdateThread import PositionsUpdateThread
from deritradeterminal.threads.StopOrdersUpdateThread import StopOrdersUpdateThread
from deritradeterminal.threads.AccountInfoUpdateThread import AccountInfoUpdateThread
from deritradeterminal.threads.RecentTradesUpdateThread import RecentTradesUpdateThread

from deritradeterminal.threads.orders.LimitBuyThread import LimitBuyThread
from deritradeterminal.threads.orders.LimitSellThread import LimitSellThread
from deritradeterminal.threads.orders.MarketBuyThread import MarketBuyThread
from deritradeterminal.threads.orders.MarketSellThread import MarketSellThread
from deritradeterminal.threads.orders.ClosePositionThread import ClosePositionThread
from deritradeterminal.threads.orders.StopMarketBuyThread import StopMarketBuyThread
from deritradeterminal.threads.orders.StopMarketSellThread import StopMarketSellThread
from deritradeterminal.threads.orders.CancelOpenOrderThread import CancelOpenOrderThread
from deritradeterminal.threads.orders.CancelOpenOrdersThread import CancelOpenOrdersThread
from deritradeterminal.threads.orders.CancelOpenStopOrdersThread import CancelOpenStopOrdersThread


class MainWindow(QMainWindow, Ui_MainWindow):

    repeatedTask = None
    positionsThread = None


    def firstRun(self):
        config = ConfigManager.get_config()
        index = 0

        for x in config.tradeApis:
            
            self.currentPositionsTable.insertRow(index)
            self.accountInfoTable.insertRow(index)

            index = index + 1

            # Add options to the acction selection
            self.limitOrderComboBox.addItem(x)
            self.marketOrderComboBox.addItem(x)
            self.stopOrderComboBox.addItem(x)


        self.currentPositionsTable.setColumnCount(8)

        index = 0
        for x in range(13):
            self.orderbookTable.insertRow(index)
            index = index + 1

        self.orderbookTable.setRowCount(25)
        self.recentTradesTable.setRowCount(25)
        self.openOrderTable.setColumnCount(5)
        self.accountInfoTable.setColumnCount(8)
        self.recentTradesTable.setColumnCount(4)

        self.positionsThread = PositionsUpdateThread()
        self.orderbookThread = OrderBookUpdateThread()
        self.openOrderThread = OrdersUpdateThread()
        self.stopOrderThread = StopOrdersUpdateThread()
        self.accountInfoThread = AccountInfoUpdateThread()
        self.recentTradesThread = RecentTradesUpdateThread()
        
        self.positionsThread.start()
        self.orderbookThread.start()
        self.openOrderThread.start()
        self.stopOrderThread.start()
        self.accountInfoThread.start()
        self.recentTradesThread.start()

        self.positionsThread.signeler.connect(self.update_positions)
        self.orderbookThread.signeler.connect(self.update_order_book)
        self.openOrderThread.signeler.connect(self.update_orders)
        self.stopOrderThread.signeler.connect(self.update_stop_orders)
        self.accountInfoThread.signeler.connect(self.update_account_info)
        self.recentTradesThread.signeler.connect(self.update_recent_trades)

        self.marketBuyButton.clicked.connect(self.do_market_buy_button)
        self.marketSellButton.clicked.connect(self.do_market_sell_button)

        self.closePositionButton.clicked.connect(self.do_close_positions)

        self.limitBuyButton.clicked.connect(self.do_limit_buy_button)
        self.limitSellButton.clicked.connect(self.do_limit_sell_button)

        self.closeOrdersButton.clicked.connect(self.do_cancel_all_open_orders)
        self.closeStopOrdersButton.clicked.connect(self.do_cancel_all_stop_orders)

        self.stopMarketBuyButton.clicked.connect(self.do_stop_market_buy_button)
        self.stopMarketSellButton.clicked.connect(self.do_stop_market_sell_button)

        self.marketAmountInput.setValidator(QDoubleValidator())
        self.limitPriceInput.setValidator(QDoubleValidator())
        self.limitAmountInput.setValidator(QDoubleValidator())
        self.stopOrderAmountInput.setValidator(QDoubleValidator())
        self.stopOrderPriceInput.setValidator(QDoubleValidator())

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
        self.orderButtonMap = {}
        self.runningThreads = []

    def update_positions(self, index, account, insturment, size, sizeb, averageprice, pnl, initialmargin):

        self.currentPositionsTable.setItem(index, 0,  QTableWidgetItem(account))
        self.currentPositionsTable.setItem(index, 1,  QTableWidgetItem(insturment))
        self.currentPositionsTable.setItem(index, 2,  QTableWidgetItem(size))
        self.currentPositionsTable.setItem(index, 3,  QTableWidgetItem(sizeb))
        self.currentPositionsTable.setItem(index, 4,  QTableWidgetItem(averageprice))
        self.currentPositionsTable.setItem(index, 5,  QTableWidgetItem(pnl))
        

        if pnl:

            self.currentPositionsTable.setItem(index, 6,  QTableWidgetItem(str(format(Util.percentageOf(pnl,initialmargin), ".2f")) + str("%")))

            if float(str(pnl)) > 0:
                self.currentPositionsTable.item(index, 5).setBackground(QtGui.QColor(27,94,32))
                self.currentPositionsTable.item(index, 6).setBackground(QtGui.QColor(27,94,32))
            elif float(str(pnl)) < 0:
                self.currentPositionsTable.item(index, 5).setBackground(QtGui.QColor(213,0,0))
                self.currentPositionsTable.item(index, 6).setBackground(QtGui.QColor(213,0,0))
            else:
                self.currentPositionsTable.item(index, 5).setBackground(QtGui.QColor(26,35,126))
                self.currentPositionsTable.item(index, 6).setBackground(QtGui.QColor(26,35,126))
        else:
            self.currentPositionsTable.setItem(index, 6,  QTableWidgetItem(""))

        self.currentPositionsTable.item(index, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.currentPositionsTable.item(index, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.currentPositionsTable.item(index, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.currentPositionsTable.item(index, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.currentPositionsTable.item(index, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.currentPositionsTable.item(index, 5).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.currentPositionsTable.item(index, 6).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        orderButton = QPushButton(self.currentPositionsTable)
        orderButton.setText("Close Position")
        orderButton.clicked.connect(partial(self.do_close_position, account))
        self.currentPositionsTable.setCellWidget(index, 7, orderButton)

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

                self.orderbookTable.item(index, 0).setBackground(QtGui.QColor(213,0,0))
                self.orderbookTable.item(index, 1).setBackground(QtGui.QColor(213,0,0))
                self.orderbookTable.item(index, 2).setBackground(QtGui.QColor(213,0,0))

                self.orderbookTable.item(index, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.orderbookTable.item(index, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.orderbookTable.item(index, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


                index = index + 1

            index = 13
            self.orderbookTable.setItem(12, 0, QTableWidgetItem("M: " + str(mark)))
            self.orderbookTable.setItem(12, 1, QTableWidgetItem(""))
            self.orderbookTable.setItem(12, 2, QTableWidgetItem("I: " + str(indexprice)))

            self.orderbookTable.item(12, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.orderbookTable.item(12, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.orderbookTable.item(12, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            for bid in cBids:
                
                self.orderbookTable.setItem(index, 0, QTableWidgetItem(str(bid['price'])))
                self.orderbookTable.setItem(index, 1, QTableWidgetItem(str(bid['quantity'])))
                self.orderbookTable.setItem(index, 2, QTableWidgetItem(str(bid['cm_amount'])))

                self.orderbookTable.item(index, 0).setBackground(QtGui.QColor(27,94,32))
                self.orderbookTable.item(index, 1).setBackground(QtGui.QColor(27,94,32))
                self.orderbookTable.item(index, 2).setBackground(QtGui.QColor(27,94,32))

                self.orderbookTable.item(index, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.orderbookTable.item(index, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.orderbookTable.item(index, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                index = index + 1

            self.orderbookTable.update()

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

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

                orderButton = QPushButton(self.openOrderTable)
                orderButton.setText("Cancel Order")
                orderButton.clicked.connect(partial(self.do_cancel_order, [str(order[0]),str(order[4])]))
                self.openOrderTable.setCellWidget(index, 4, orderButton)

                self.openOrderTable.item(index, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.openOrderTable.item(index, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.openOrderTable.item(index, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.openOrderTable.item(index, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    
                index = index + 1

            self.openOrderTable.update()

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def update_stop_orders(self, orders):
        try:

            index = 0

            if len(orders) != self.stopOrderTable.rowCount:
                self.stopOrderTable.setRowCount(0)

                for x in range(len(orders)):
                    self.stopOrderTable.insertRow(x)

                self.stopOrderTable.setRowCount(len(orders))

            for order in orders:
                self.stopOrderTable.setItem(index, 0, QTableWidgetItem(str(order[0])))
                self.stopOrderTable.setItem(index, 1, QTableWidgetItem(str(order[1])))
                self.stopOrderTable.setItem(index, 2, QTableWidgetItem(str(order[2])))
                self.stopOrderTable.setItem(index, 3, QTableWidgetItem(str(order[3])))

                orderButton = QPushButton(self.stopOrderTable)
                orderButton.setText("Cancel Order")
                orderButton.clicked.connect(partial(self.do_cancel_order, [str(order[0]),str(order[4])]))
                self.stopOrderTable.setCellWidget(index, 4, orderButton)

                self.stopOrderTable.item(index, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.stopOrderTable.item(index, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.stopOrderTable.item(index, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.stopOrderTable.item(index, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                index = index + 1

            self.stopOrderTable.update()

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def update_account_info(self, accounts):
        try:

            index = 0

            for account in accounts:
                self.accountInfoTable.setItem(index, 0, QTableWidgetItem(str(account[0])))
                self.accountInfoTable.setItem(index, 1, QTableWidgetItem(str(account[1])))
                self.accountInfoTable.setItem(index, 2, QTableWidgetItem(str(account[2])))
                self.accountInfoTable.setItem(index, 3, QTableWidgetItem(str(account[3])))
                self.accountInfoTable.setItem(index, 4, QTableWidgetItem(str(account[4])))
                self.accountInfoTable.setItem(index, 5, QTableWidgetItem(str(account[5])))
                self.accountInfoTable.setItem(index, 6, QTableWidgetItem(str(account[6])))
                self.accountInfoTable.setItem(index, 7, QTableWidgetItem(str(account[7])))

                self.accountInfoTable.item(index, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.accountInfoTable.item(index, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.accountInfoTable.item(index, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.accountInfoTable.item(index, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.accountInfoTable.item(index, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.accountInfoTable.item(index, 5).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.accountInfoTable.item(index, 6).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.accountInfoTable.item(index, 7).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                if float(account[7]) == 0:
                    pass
                elif float(account[7]) < 40:
                    self.accountInfoTable.item(index, 7).setBackground(QtGui.QColor(27,94,32))
                elif float(account[7]) > 40 and float(account[7]) < 80:
                    self.accountInfoTable.item(index, 7).setBackground(QtGui.QColor(255,214,0))
                elif float(account[7]) > 80 and float(account[7]) < 90:
                    self.accountInfoTable.item(index, 7).setBackground(QtGui.QColor(255,109,0))
                else:
                    self.accountInfoTable.item(index, 7).setBackground(QtGui.QColor(213,0,0))



                index = index + 1

            self.accountInfoTable.update()

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def update_recent_trades(self, trades):
        try:


            index = 0

            for trade in trades:

                self.recentTradesTable.setItem(index, 0, QTableWidgetItem(str(trade[0])))
                self.recentTradesTable.setItem(index, 1, QTableWidgetItem(str(trade[1])))
                self.recentTradesTable.setItem(index, 2, QTableWidgetItem(str(trade[2])))
                self.recentTradesTable.setItem(index, 3, QTableWidgetItem(str(trade[3])))

                if self.recentTradesTable.item(index, 0):
                    self.recentTradesTable.item(index, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.recentTradesTable.item(index, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.recentTradesTable.item(index, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.recentTradesTable.item(index, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                if trade[0] == "Long":
                    if self.recentTradesTable.item(index, 0):
                        self.recentTradesTable.item(index, 0).setBackground(QtGui.QColor(27,94,32))
                else:
                    if self.recentTradesTable.item(index, 0):
                        self.recentTradesTable.item(index, 0).setBackground(QtGui.QColor(213,0,0))

                index = index + 1

            self.recentTradesTable.update()

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_market_buy_button(self):

        try:
            
            config = ConfigManager.get_config()

            selection = str(self.marketOrderComboBox.currentText())

            if selection == "All":

                for x in config.tradeApis:

                    thread = MarketBuyThread(x, float(self.marketAmountInput.text()))
                    thread.signeler.connect(self.show_dialogs)
                    thread.start()
                    self.runningThreads.append(thread)

            else:

                thread = MarketBuyThread(selection, float(self.marketAmountInput.text()))
                thread.signeler.connect(self.show_dialogs)
                thread.start()
                self.runningThreads.append(thread)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_market_sell_button(self):

        try:

            config = ConfigManager.get_config()

            selection = str(self.marketOrderComboBox.currentText())

            if selection == "All":

                for x in config.tradeApis:

                    thread = MarketSellThread(x, float(self.marketAmountInput.text()))
                    thread.signeler.connect(self.show_dialogs)
                    thread.start()
                    self.runningThreads.append(thread)

            else:

                thread = MarketSellThread(selection, float(self.marketAmountInput.text()))
                thread.signeler.connect(self.show_dialogs)
                thread.start()
                self.runningThreads.append(thread)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_stop_market_buy_button(self):

        try:

            config = ConfigManager.get_config()

            selection = str(self.stopOrderComboBox.currentText())

            if selection == "All":

                for x in config.tradeApis:

                    thread = StopMarketBuyThread(x, float(self.stopOrderPriceInput.text()), float(self.stopOrderAmountInput.text()))
                    thread.signeler.connect(self.show_dialogs)
                    thread.start()
                    self.runningThreads.append(thread)

            else:

                thread = StopMarketBuyThread(selection, float(self.stopOrderPriceInput.text()), float(self.stopOrderAmountInput.text()))
                thread.signeler.connect(self.show_dialogs)
                thread.start()
                self.runningThreads.append(thread)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_stop_market_sell_button(self):

        try:

            config = ConfigManager.get_config()

            selection = str(self.stopOrderComboBox.currentText())

            if selection == "All":

                for x in config.tradeApis:

                    thread = StopMarketSellThread(x, float(self.stopOrderPriceInput.text()), float(self.stopOrderAmountInput.text()))
                    thread.signeler.connect(self.show_dialogs)
                    thread.start()
                    self.runningThreads.append(thread)

            else:

                thread = StopMarketSellThread(selection, float(self.stopOrderPriceInput.text()), float(self.stopOrderAmountInput.text()))
                thread.signeler.connect(self.show_dialogs)
                thread.start()
                self.runningThreads.append(thread)
                
        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_limit_buy_button(self):

        try:

            config = ConfigManager.get_config()

            selection = str(self.limitOrderComboBox.currentText())

            if selection == "All":
                
                for x in config.tradeApis:

                    thread = LimitBuyThread(x, float(self.limitPriceInput.text()), float(self.limitAmountInput.text()))
                    thread.signeler.connect(self.show_dialogs)
                    thread.start()
                    self.runningThreads.append(thread)

            else:
                thread = LimitBuyThread(selection, float(self.limitPriceInput.text()), float(self.limitAmountInput.text()))
                thread.signeler.connect(self.show_dialogs)
                thread.start()
                self.runningThreads.append(thread)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_limit_sell_button(self):

        try:

            config = ConfigManager.get_config()

            selection = str(self.limitOrderComboBox.currentText())

            if selection == "All":

                for x in config.tradeApis:

                    thread = LimitSellThread(x, float(self.limitPriceInput.text()), float(self.limitAmountInput.text()))
                    thread.signeler.connect(self.show_dialogs)
                    thread.start()
                    self.runningThreads.append(thread)

            else:
                
                thread = LimitSellThread(selection, float(self.limitPriceInput.text()), float(self.limitAmountInput.text()))
                thread.signeler.connect(self.show_dialogs)
                thread.start()
                self.runningThreads.append(thread)

        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))
            print(e)

    def do_close_position(self, accountid):

        thread = ClosePositionThread(accountid)
        thread.signeler.connect(self.show_dialogs)
        thread.start()
        self.runningThreads.append(thread)
                
    def do_close_positions(self):

        config = ConfigManager.get_config()

        try:

            selection = str(self.marketOrderComboBox.currentText())

            if selection == "All":

                for x in config.tradeApis:

                    thread = ClosePositionThread(x)
                    thread.signeler.connect(self.show_dialogs)
                    thread.start()
                    self.runningThreads.append(thread)
                
            else:

                thread = ClosePositionThread(selection)
                thread.signeler.connect(self.show_dialogs)
                thread.start()
                self.runningThreads.append(thread)

        except Exception as e:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage(str(e))
            print(e)


    def do_cancel_all_open_orders(self):

        config = ConfigManager.get_config()

        try:
            
            for x in config.tradeApis:

                thread = CancelOpenOrdersThread(x)
                thread.signeler.connect(self.show_dialogs)
                thread.start()
                self.runningThreads.append(thread)

            Util.show_info_dialog(self, "Order Info", "All Open Orders On All Accounts Cancelled")

        except Exception as e:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage(str(e))
            print(e)

    def do_cancel_all_stop_orders(self):

        config = ConfigManager.get_config()

        try:
            
            for x in config.tradeApis:

                thread = CancelOpenStopOrdersThread(x)
                thread.signeler.connect(self.show_dialogs)
                thread.start()
                self.runningThreads.append(thread)

            Util.show_info_dialog(self, "Order Info", "All Stop Orders On All Accounts Cancelled")

        except Exception as e:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage(str(e))
            print(e)

    def do_cancel_order(self, data):

        thread = CancelOpenOrderThread(data[0], data[1])
        thread.signeler.connect(self.show_dialogs)
        thread.start()
        self.runningThreads.append(thread)

    def show_dialogs(self, success, title, text):

        if success:
            Util.show_info_dialog(self, title, text)
        else:
            Util.show_error_dialog(self, title, text)



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