import sys, requests
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QTimer

API_URL = "http://localhost:5000/satellites"  # your API

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = QWebEngineView()
        self.view.load("map.html")

        self.setCentralWidget(self.view)
        self.setWindowTitle("Satellite Tracker")

        # update every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)

    def update_data(self):
        try:
            data = requests.get(API_URL).json()

            js = f"updateSatellites({data});"
            self.view.page().runJavaScript(js)

        except Exception as e:
            print("API error:", e)


app = QApplication(sys.argv)
window = App()
window.showMaximized()  # fullscreen-ish
app.exec()