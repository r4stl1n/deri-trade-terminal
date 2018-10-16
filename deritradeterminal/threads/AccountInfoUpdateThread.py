from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from deritradeterminal.util.deribit_api import RestClient
from deritradeterminal.managers.ConfigManager import ConfigManager

class AccountInfoUpdateThread(QThread):

    signeler = pyqtSignal(list) 

    def collectProcessData(self):

        try:
            
            config = ConfigManager.get_config()

            toreturn = []

            for x in config.tradeApis:

                client = RestClient(config.tradeApis[x][0], config.tradeApis[x][1], ConfigManager.get_config().apiUrl)

                accountinfo = client.account()

                toreturn.append([x, str(format(accountinfo["equity"], '.8f')), str(format(accountinfo["balance"], '.8f')), 
                    str(format(accountinfo["availableFunds"], '.8f')), str(format(accountinfo["initialMargin"], '.8f')), str(format(accountinfo["maintenanceMargin"], '.8f'))])

            self.signeler.emit(toreturn)

        except Exception as e:
            print(e)

    def __init__(self):
        QThread.__init__(self)


    def run(self):
        while True:
            self.collectProcessData()
