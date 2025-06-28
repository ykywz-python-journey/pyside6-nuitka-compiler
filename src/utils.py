import winreg
import os


def find_chrome_path():
    try:
        # Try to get path from registry first
        with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        ) as key:
            path = winreg.QueryValue(key, None)
            if os.path.exists(path):
                return path

        # Common default installation locations if registry fails
        common_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path
    except WindowsError as e:
        print(f"Error accessing registry: {e}")


import os
import pathlib


def get_chrome_default_profile_path(profile=None):
    # Get the user's home directory
    home_dir = str(pathlib.Path.home())

    # Construct the default profile path
    default_profile_path = os.path.join(
        home_dir, "AppData", "Local", "Google", "Chrome", "User Data"
    )

    if profile:
        default_profile_path = os.path.join(default_profile_path, profile)

    # Check if the path exists
    if os.path.exists(default_profile_path):
        return default_profile_path
    else:
        return None


import os
import pathlib


def get_all_chrome_profiles():
    # Get the user's home directory
    home_dir = str(pathlib.Path.home())

    # Construct the user data directory path
    user_data_dir = os.path.join(home_dir, "AppData", "Local", "Google", "Chrome", "User Data")

    # Check if the user data directory exists
    if not os.path.exists(user_data_dir):
        return None

    # List to hold profile paths
    profiles = []

    # Check for the Default profile
    default_profile_path = os.path.join(user_data_dir, "Default")
    if os.path.exists(default_profile_path):
        profiles.append(default_profile_path)

    # Check for other profiles
    for entry in os.listdir(user_data_dir):
        if entry.startswith("Profile ") and os.path.isdir(os.path.join(user_data_dir, entry)):
            profiles.append(os.path.join(user_data_dir, entry))

    return profiles


import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#
# profiles = get_all_chrome_profiles()
# if profiles:
#     print("Existing Chrome profiles:")
#     for profile in profiles:
#         print(profile)
# else:
#     print("No Chrome profiles found.")

# default_profile = get_chrome_default_profile_path()
# if default_profile:
#     print(f"Default Chrome profile path: {default_profile}")
# else:
#     print("Default Chrome profile not found.")

# chrome_path = find_chrome_path()
# if chrome_path:
#     print(f"Found Chrome at: {chrome_path}")
# else:
#     print("Could not find Chrome executable")
