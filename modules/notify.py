import sys
import subprocess

if sys.platform == "win32":
    from win10toast import ToastNotifier


def show_notification(heading, text, seconds):
    """
    This function shows a desktop notification
    """
    if sys.platform.lower() == "linux":  # Linux Ubuntu
        subprocess.call(["notify-send", heading, text, "-t", f"{seconds}"])

    if sys.platform.lower() == "darwin":  # MacOS Mavericks +
        subprocess.call(
            [
                "osascript",
                "-e",
                'display notification "{0}" with title "{1}"'.format(text, heading),
            ]
        )

    elif sys.platform.lower() == "win32":  # Windows
        toaster = ToastNotifier()
        toaster.show_toast(heading, text, duration=seconds)
