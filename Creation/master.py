import Creation.instanceTools as instanceTools
import time
from tkinter import Tk


def startInstance(token, instance, zone, price):
    reqID = instanceTools.reqInstance(token, instance, zone, price)
    print('Now putting the system to hold for 10 seconds to let the request process')
    time.sleep(10)
    instID = instanceTools.getInstance(reqID)
    instanceTools.addtoILedger(instID, token)
    instDict = instanceTools.readyInst(instID)
    return instDict['PublicIpAddress']
    # r = Tk()
    # r.withdraw()
    # r.clipboard_clear()
    # r.clipboard_append(instDict['PublicIpAddress'])
    # r.update()  # now it stays on the clipboard after the window is closed
    # r.destroy()


# startInstance('ledgerformat', 't2.micro', 'eu-central-1a', '0.005')
