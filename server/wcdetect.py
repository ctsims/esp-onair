#Code from https://gist.github.com/cobryan05/8e191ae63976224a0129a8c8f376adc6

import winreg

class WebcamDetect:
    REG_KEY = winreg.HKEY_CURRENT_USER
    WEBCAM_REG_SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam\\NonPackaged"
    WEBCAM_TIMESTAMP_VALUE_NAME = "LastUsedTimeStop"

    def __init__(self):
        self._regKey = winreg.OpenKey( WebcamDetect.REG_KEY, WebcamDetect.WEBCAM_REG_SUBKEY )

    def getActiveApps(self):
        activeApps = []
        # Enumerate over the subkeys of the webcam key
        subkeyCnt, valueCnt, lastModified = winreg.QueryInfoKey( self._regKey )
        for idx in range(subkeyCnt):
            subkeyName = winreg.EnumKey( self._regKey, idx )
            subkeyFullName = f"{WebcamDetect.WEBCAM_REG_SUBKEY}\\{subkeyName}"

            # Open each subkey and check the 'stopped' timestamp value. A value of 0 implies the camera is in use.
            subkey = winreg.OpenKey( WebcamDetect.REG_KEY, subkeyFullName )
            stoppedTimestamp, _ = winreg.QueryValueEx( subkey, WebcamDetect.WEBCAM_TIMESTAMP_VALUE_NAME )
            if 0 == stoppedTimestamp:
                activeApps.append( subkeyName.replace("#", "/" ) )

        return activeApps

    def isActive(self):
        return len(self.getActiveApps()) > 0
