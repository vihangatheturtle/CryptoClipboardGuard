import time
import threading
import pyperclip
import time
import plyer.platforms.win.notification
from plyer import notification

oldEthereumAddress = ""
lastEthereumAddress = ""
lastWalletUpdate = 0
skipCheck = False

print("WalletGuard V1")
print("by Turtlee#2000 (708335358667915285)")

def is_ethereum_wallet(text):
    text = text.replace(" ", "")
    if len(text) == 42 and text.startswith("0x"):
        return True
    return False

def print_to_stdout(clipboard_content):
    global lastWalletUpdate
    global lastEthereumAddress
    global n
    global skipCheck
    if skipCheck:
        skipCheck = False
        return
    print ("Found address: %s" % str(clipboard_content))
    if int(time.time()) - lastWalletUpdate < 5:
        print("Potential clipboard modification detected")
        print(lastEthereumAddress, "-->", clipboard_content, "(change within 5 seconds)")
        print("Reverting the change")
        pyperclip.copy(" " + lastEthereumAddress + " ")
        skipCheck = True
        notification.notify("Wallet Guardian", "Detected a malicious clipboard modification. We have reverted this change.\n" + lastEthereumAddress + " --> " + clipboard_content)
    else:
        lastEthereumAddress = clipboard_content
    lastWalletUpdate = int(time.time())

class ClipboardWatcher(threading.Thread):
    def __init__(self, predicate, callback, pause=5.):
        super(ClipboardWatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                if self._predicate(recent_value):
                    self._callback(recent_value)
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True

def main():
    watcher = ClipboardWatcher(is_ethereum_wallet, 
                               print_to_stdout,
                               0.01)
    watcher.start()
    print("Waiting for changed clipboard...")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            watcher.stop()
            break


if __name__ == "__main__":
    main()