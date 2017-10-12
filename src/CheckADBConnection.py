import subprocess
import sys
sys.path.append('./GUI')
from MessageUI import Message
import re
from adbRobot import ADBRobot

class checkADB_Connection:
    def __init__(self):
        self.SerialNo = ""
        self.DisplayW = ""
        self.DisplayH = ""

    def check(self):
        message = Message.getMessage(self)
        try:
            deviceInfo = subprocess.getoutput('adb devices')
            deviceNames = deviceInfo.splitlines()
            print(deviceNames)
            finddevices = []
            for i in range(len(deviceNames)):
                if deviceNames[i].find("emulator") >= 0:
                    subprocess.check_call('adb kill-server')
                    self.check()

                if deviceNames[i].find("device") >= 0:
                    finddevices.append(deviceNames[i])

            finddevices.pop(0)
            if len(finddevices) == 0:
                return "No Connect"
            else:
                self.SerialNo = finddevices[0]
                real_size_pattern = r"real (\d+) x (\d+),"
                result = subprocess.check_output('adb shell dumpsys display | grep mBaseDisplayInfo').__str__()
                match = re.search(real_size_pattern, result)
                self.DisplayW, self.DisplayH = match.group(1), match.group(2)
                print("display = ", self.DisplayW, self.DisplayH)
                return "Connect"

        except subprocess.CalledProcessError as e:
            pass

    def get_SerialNo(self):
        return self.SerialNo

    def get_Display(self):
        return self.DisplayW , self.DisplayH
