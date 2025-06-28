import asyncio

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import QThread
from pyppeteer import launch

from utils import find_chrome_path, get_chrome_default_profile_path, resource_path


class BrowserThread(QThread):

    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        print('ahihih')
        async def launch_browser():
            browser = await launch({
                'handleSIGINT': False,
                'handleSIGTERM': False,
                'handleSIGHUP': False,
                'executablePath': find_chrome_path(),  # Specify your custom Chrome path
                'userDataDir': get_chrome_default_profile_path('tests'),
                'headless': False  # Set to True if you want to run in headless mode
            })

            page = await browser.newPage()
            await page.goto('https://example.com')

            await asyncio.sleep(1000)
            # Perform actions on the page
            # await browser.close()

        asyncio.run(launch_browser())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chrome Profile Launcher")
        self.setGeometry(100, 100, 400, 200)

        # Create UI
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        btn = QPushButton(f"Launch")
        btn.clicked.connect(self.launch_profile)
        self.layout.addWidget(btn)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def launch_profile(self):
        self.browser_thread = BrowserThread(self)
        self.browser_thread.start()

    def show_message(self, message):
        print(message)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon(resource_path('app.png')))
    window = MainWindow()
    window.show()
    app.exec()

