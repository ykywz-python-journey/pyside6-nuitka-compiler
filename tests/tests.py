import os
import asyncio
import pathlib
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                               QWidget, QPushButton, QLabel, QHBoxLayout)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from datetime import datetime


class ChromeProfileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chrome Profile Manager")
        self.setGeometry(100, 100, 600, 400)

        # Setup icons (using embedded SVG as fallback)
        self.setup_icons()

        # Create UI
        self.create_ui()

    def setup_icons(self):
        """Setup icons using embedded SVG as fallback"""
        # Main window icon
        self.setWindowIcon(self.load_icon("chrome"))

        # Action icons
        self.icons = {
            "create": self.load_icon("plus-circle"),
            "list": self.load_icon("list"),
            "open": self.load_icon("folder-open"),
            "delete": self.load_icon("trash"),
            "chrome": self.load_icon("chrome")
        }

    def load_icon(self, name):
        """Load icon from resources or use fallback SVG"""
        # Try to load from system theme first
        icon = QIcon.fromTheme(name)

        if icon.isNull():
            # Fallback to embedded SVG
            icon = self.get_fallback_icon(name)

        return icon

    def get_fallback_icon(self, name):
        """Generate fallback SVG icons"""
        from PySide6.QtSvg import QSvgRenderer
        from PySide6.QtGui import QPixmap, QPainter

        svg_data = ""
        size = QSize(32, 32)

        if name == "chrome":
            svg_data = """
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
                <path fill="#E53935" d="M24 9.5A19.5 19.5 0 1 0 43.5 29 19.5 19.5 0 0 0 24 9.5z"/>
                <path fill="#FFC107" d="M24 9.5a19.4 19.4 0 0 1 16 8.5l-6.8 1.7a12 12 0 0 0-20.4 0L8 18a19.4 19.4 0 0 1 16-8.5z"/>
                <path fill="#4CAF50" d="M40 18l-6.8 1.7a12 12 0 0 1 0 18.6L40 40a19.5 19.5 0 0 0 0-22z"/>
                <circle cx="24" cy="29" r="8" fill="#1E88E5"/>
                <circle cx="24" cy="29" r="5" fill="#1565C0"/>
            </svg>
            """
        elif name == "plus-circle":
            svg_data = """
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#4CAF50">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/>
            </svg>
            """
        elif name == "list":
            svg_data = """
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#2196F3">
                <path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zm0-10v2h14V7H7z"/>
            </svg>
            """
        elif name == "folder-open":
            svg_data = """
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FF9800">
                <path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/>
            </svg>
            """
        elif name == "trash":
            svg_data = """
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#F44336">
                <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
            </svg>
            """

        if svg_data:
            renderer = QSvgRenderer()
            renderer.load(svg_data.encode())
            pixmap = QPixmap(size)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            return QIcon(pixmap)

        return QIcon()

    def create_ui(self):
        """Create the main application UI"""
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Title with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(self.icons["chrome"].pixmap(48, 48))
        title_text = QLabel("Chrome Profile Manager")
        title_text.setStyleSheet("font-size: 20px; font-weight: bold;")

        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_text)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)

        # Main buttons
        btn_layout = QHBoxLayout()

        self.create_btn = QPushButton("Create Profile")
        self.create_btn.setIcon(self.icons["create"])
        self.create_btn.setStyleSheet("padding: 10px;")

        self.list_btn = QPushButton("List Profiles")
        self.list_btn.setIcon(self.icons["list"])
        self.list_btn.setStyleSheet("padding: 10px;")

        self.open_btn = QPushButton("Launch Profile")
        self.open_btn.setIcon(self.icons["open"])
        self.open_btn.setStyleSheet("padding: 10px;")

        btn_layout.addWidget(self.create_btn)
        btn_layout.addWidget(self.list_btn)
        btn_layout.addWidget(self.open_btn)
        main_layout.addLayout(btn_layout)

        # Profile list
        self.profile_list = QLabel("No profiles loaded. Click 'List Profiles' to view.")
        self.profile_list.setWordWrap(True)
        main_layout.addWidget(self.profile_list)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect signals
        self.create_btn.clicked.connect(self.create_profile)
        self.list_btn.clicked.connect(self.list_profiles)
        self.open_btn.clicked.connect(self.launch_profile)

    async def async_create_profile(self, profile_name):
        """Create a new Chrome profile (async)"""
        home_dir = str(pathlib.Path.home())
        user_data_dir = os.path.join(
            home_dir, "AppData", "Local", "Google", "Chrome", "User Data"
        )

        if not profile_name:
            profile_name = f"Profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            from pyppeteer import launch
            browser = await launch({
                'headless': False,
                'userDataDir': user_data_dir,
                'args': [f'--profile-directory={profile_name}'],
                'handleSIGINT': False,
                'handleSIGTERM': False,
                'handleSIGHUP': False
            })
            await browser.close()
            return True, f"Successfully created profile: {profile_name}"
        except Exception as e:
            return False, f"Failed to create profile: {str(e)}"

    def create_profile(self):
        """Wrapper for profile creation to handle asyncio"""
        profile_name = f"Profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        async def runner():
            success, message = await self.async_create_profile(profile_name)
            self.profile_list.setText(message)

        asyncio.create_task(runner())

    def list_profiles(self):
        """List existing Chrome profiles"""
        home_dir = str(pathlib.Path.home())
        user_data_dir = os.path.join(
            home_dir, "AppData", "Local", "Google", "Chrome", "User Data"
        )

        if not os.path.exists(user_data_dir):
            self.profile_list.setText("Chrome user data directory not found")
            return

        profiles = []

        # Default profile
        if os.path.exists(os.path.join(user_data_dir, "Default")):
            profiles.append("Default")

        # Other profiles
        for entry in os.listdir(user_data_dir):
            if entry.startswith("Profile") and os.path.isdir(os.path.join(user_data_dir, entry)):
                profiles.append(entry)

        if profiles:
            self.profile_list.setText("Available profiles:\n" + "\n".join(profiles))
        else:
            self.profile_list.setText("No profiles found")

    def launch_profile(self):
        """Launch selected Chrome profile"""
        current_text = self.profile_list.text()
        if not current_text.startswith("Available profiles"):
            self.profile_list.setText("Please list profiles first")
            return

        profiles = current_text.split("\n")[1:]
        if not profiles:
            self.profile_list.setText("No profiles available to launch")
            return

        # For simplicity, just launch the first profile
        profile_to_launch = profiles[0].strip()
        self.profile_list.setText(f"Launching profile: {profile_to_launch}...")

        async def runner():
            home_dir = str(pathlib.Path.home())
            user_data_dir = os.path.join(
                home_dir, "AppData", "Local", "Google", "Chrome", "User Data"
            )

            try:
                from pyppeteer import launch
                browser = await launch({
                    'headless': False,
                    'userDataDir': user_data_dir,
                    'args': [f'--profile-directory={profile_to_launch}'],
                    'handleSIGINT': False,
                    'handleSIGTERM': False,
                    'handleSIGHUP': False
                })
                await browser.newPage()
                self.profile_list.setText(f"Profile {profile_to_launch} launched successfully")
            except Exception as e:
                self.profile_list.setText(f"Failed to launch profile: {str(e)}")

        asyncio.create_task(runner())


if __name__ == "__main__":
    app = QApplication([])

    # Set application style for better look
    app.setStyle("Fusion")

    window = ChromeProfileManager()
    window.show()
    app.exec()
