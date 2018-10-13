from PyQt5.QtGui import QPalette, QColor


WHITE =     QColor(255, 255, 255)
BLACK =     QColor(0, 0, 0)
RED =       QColor(255, 0, 0)
PRIMARY =   QColor(53, 53, 53)
SECONDARY = QColor(35, 35, 35)
TERTIARY =  QColor(42, 130, 218)


def css_rgb(color, a=False):
    """Get a CSS `rgb` or `rgba` string from a `QtGui.QColor`."""
    return ("rgba({}, {}, {}, {})" if a else "rgb({}, {}, {})").format(*color.getRgb())


class QDarkPalette:
    """Dark palette for a Qt application meant to be used with the Fusion theme."""
    def __init__(self):

        self.palette = QPalette()

        # Set all the colors based on the constants in globals
        self.palette.setColor(QPalette.Window,          PRIMARY)
        self.palette.setColor(QPalette.WindowText,      WHITE)
        self.palette.setColor(QPalette.Base,            SECONDARY)
        self.palette.setColor(QPalette.AlternateBase,   PRIMARY)
        self.palette.setColor(QPalette.ToolTipBase,     WHITE)
        self.palette.setColor(QPalette.ToolTipText,     WHITE)
        self.palette.setColor(QPalette.Text,            WHITE)
        self.palette.setColor(QPalette.Button,          PRIMARY)
        self.palette.setColor(QPalette.ButtonText,      WHITE)
        self.palette.setColor(QPalette.BrightText,      RED)
        self.palette.setColor(QPalette.Link,            TERTIARY)
        self.palette.setColor(QPalette.Highlight,       TERTIARY)
        self.palette.setColor(QPalette.HighlightedText, BLACK)

    @staticmethod
    def set_stylesheet(app):
        """Static method to set the tooltip stylesheet to a `QtWidgets.QApplication`."""
        app.setStyleSheet("QToolTip {{"
                          "color: {white};"
                          "background-color: {tertiary};"
                          "border: 1px solid {white};"
                          "}}".format(white=css_rgb(WHITE), tertiary=css_rgb(TERTIARY)))

    def set_app(self, app):
        """Set the Fusion theme and this palette to a `QtWidgets.QApplication`."""
        app.setStyle("Fusion")
        app.setPalette(self.palette)
        self.set_stylesheet(app)