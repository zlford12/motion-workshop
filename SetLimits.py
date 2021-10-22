from tkinter import *
from tkinter import messagebox, Entry
from opcua import Client, ua
import threading
import time

# Initialize Tkinter
root = Tk()
root.title("Set Limits V1.0")
root.geometry("640x480")
root.resizable(width=False, height=False)
root.configure(bg="#333333")
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)


# Initialize OPC UA Client
client = Client("opc.tcp://" + open("ip.txt", "r").read() + ":4840", timeout=3)


# Connection Status
def threadstart():
    threading.Thread(target=isconnected).start()


def isconnected():
    global statusdisplay

    isalive = str(client.keepalive).find("started") != -1
    if isalive:
        try:
            client.get_node("ns=2;s=Application.CommissioningVar.bCommissioningHeartbeat").set_value(True)
        except:
            disconnect()
            root.after(200, func=threadstart)
            return
        getposition()

        statusdisplay.configure(text="Connected", bg="#00FF00")
        root.after(200, func=threadstart)
    else:
        connected = False
        statusdisplay.configure(text="Disconnected", bg="#FF0000")


# Header Button Functions
def openclient():
    try:
        client.connect()
        threadstart()
    except:
        messagebox.showerror(title="OPC Error", message="Failure Connecting\nto OPC UA Server")
        return
    getaxes()


def disconnect():
    global rightside
    try:
        client.disconnect()
    except:
        messagebox.showerror(title="OPC Error", message="Connection\nError")

    for child in rightside.winfo_children():
        child.destroy()

    drawrightside([""])


def clearerr():
    try:
        client.get_node("ns=2;s=Application.IO_Names.command").set_value(2, ua.VariantType.Int16)
    except:
        messagebox.showerror(title="OPC Error", message="Failure Writing Data\nto OPC UA Server")


# Connection Management Functions
def getaxes():
    global rightside
    global AxisList
    AxisList = [""]
    try:
        AxisString = client.get_node("ns=2;s=Application.CommissioningVar.sRealAxes").get_value()
        AxisList = AxisString.split(",")
    except:
        messagebox.showerror(title="OPC Error", message="Failure Reading Data\nfrom OPC UA Server")

    for child in rightside.winfo_children():
        child.destroy()

    drawrightside(AxisList)


def setaxisnumber(axisname):
    global AxisList
    global AxisNumber

    if (axisname != ""):
        AxisNumber = AxisList.index(axisname) + 1
        insertlimits()

    drawfooter()


def getaxisinfo():
    global AxisNumber

    positivelimit = client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Limits.PositionLimitPositive").get_value()
    negativelimit = client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Limits.PositionLimitNegative").get_value()
    spdunit = client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Units.Velocity").get_value()
    accunit = client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Units.Acceleration").get_value()
    maxspeed = client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Limits.VelocityLimitBipolar").get_value()
    maxaccel = client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Limits.AccelerationLimitBipolar").get_value()

    return(positivelimit, negativelimit, spdunit, accunit, maxspeed, maxaccel)


def getposition():
    global AxisNumber
    global currentposlabel

    try:
        AxisNumber
    except NameError:
        AxisNumber = None

    if AxisNumber == None:
        return
    else:
        currentposition = str(client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".ActualValues.ActualPosition").get_value())

        try:
            currentposlabel.configure(text=currentposition)
        except:
            return


# Jog Control Functions
def jogpos():
    global AxisNumber
    (positivelimit, _, _, _, maxspeed, maxaccel) = getaxisinfo()

    speed = float(jogspd.get())
    if (speed > maxspeed):
        speed = maxspeed

    accel = float(jogacc.get())
    if (accel > maxaccel):
        accel = maxaccel

    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Position").set_value((positivelimit - 10),ua.VariantType.Float)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Velocity").set_value(speed,ua.VariantType.Float)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Accel").set_value(accel,ua.VariantType.Float)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissionJog_AxisNo").set_value(AxisNumber,ua.VariantType.Int16)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(True)


def jogneg():
    global AxisNumber
    (_, negativelimit, _, _, maxspeed, maxaccel) = getaxisinfo()

    speed = float(jogspd.get())
    if (speed > maxspeed):
        speed = maxspeed

    accel = float(jogacc.get())
    if (accel > maxaccel):
        accel = maxaccel

    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Position").set_value((negativelimit + 10),ua.VariantType.Float)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Velocity").set_value(speed,ua.VariantType.Float)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Accel").set_value(accel,ua.VariantType.Float)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissionJog_AxisNo").set_value(AxisNumber,ua.VariantType.Int16)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(True)


def stopjog():
    global AxisNumber

    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissionJog_AxisNo").set_value(AxisNumber,ua.VariantType.Int16)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(True)


def gotopos():
    global AxisNumber
    (positivelimit, negativelimit, _, _, maxspeed, maxaccel) = getaxisinfo()
    global gotoentry

    gotoposition = float(gotoentry.get())
    if gotoposition > (positivelimit - 10):
        gotoposition = positivelimit
    if gotoposition < (negativelimit + 10):
        gotoposition = negativelimit

    speed = float(jogspd.get())
    if (speed > maxspeed):
        speed = maxspeed

    accel = float(jogacc.get())
    if (accel > maxaccel):
        accel = maxaccel

    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Position").set_value(gotoposition,ua.VariantType.Float)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Velocity").set_value(speed,ua.VariantType.Float)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Accel").set_value(accel,ua.VariantType.Float)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissionJog_AxisNo").set_value(AxisNumber,ua.VariantType.Int16)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(True)


# Gear In Functions
def gearinmaster1(master):
    global AxisList
    global AxisNumber
    global Master1

    Master1 = master
    MasterNumber = AxisList.index(master) + 1


    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissioningGearInMaster_1").set_value(MasterNumber, ua.VariantType.Int16)


def gearinmaster2(master):
    global AxisList
    global AxisNumber
    global Master2

    Master2 = master
    MasterNumber = AxisList.index(master) + 1

    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissioningGearInMaster_2").set_value(MasterNumber, ua.VariantType.Int16)


def gearinslave1(slave):
    global AxisList
    global AxisNumber
    global Slave1

    Slave1 = slave
    SlaveNumber = AxisList.index(slave) + 1

    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissioningGearInSlave_1").set_value(SlaveNumber, ua.VariantType.Int16)


def gearinslave2(slave):
    global AxisList
    global AxisNumber
    global Slave2

    Slave2 = slave
    SlaveNumber = AxisList.index(slave) + 1

    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissioningGearInSlave_2").set_value(SlaveNumber, ua.VariantType.Int16)


def gearin1():

    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_1").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(True)


def gearin2():
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_2").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(True)


def gearout1():
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_1").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_1").set_value(True)


def gearout2():
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_2").set_value(False)
    client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_2").set_value(True)


# Set Limits Functions
def insertlimits():
    global neglimitentry
    global poslimitentry
    global setpositionentry

    try:
        neglimitentry.delete(0, 100)
        neglimit = str(client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Limits.PositionLimitNegative").get_value())
        neglimitentry.insert(0, neglimit)

        poslimitentry.delete(0, 100)
        poslimit = str(client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Limits.PositionLimitPositive").get_value())
        poslimitentry.insert(0, poslimit)

        setpositionentry.delete(0, 100)
    except:
        return


def setlimits():
    global neglimitentry
    global poslimitentry

    neglimit = ua.DataValue(ua.Variant(float(neglimitentry.get()), ua.VariantType.Double))
    poslimit = ua.DataValue(ua.Variant(float(poslimitentry.get()), ua.VariantType.Double))
    client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Limits.PositionLimitNegative").set_attribute(ua.AttributeIds.Value, neglimit)
    client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber) + ".Limits.PositionLimitPositive").set_attribute(ua.AttributeIds.Value, poslimit)


def setposition():
    global AxisNumber
    global setpositionentry

    node = client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(AxisNumber)).get_referenced_nodes()

    for child in node:
        if (str(child).find("s=Physical") > -1):
            drivenode = str(child)

    client.get_node(nodeid=drivenode + '.ParameterSet."S-0-0052"').set_value(int(setpositionentry.get()) * 10000, ua.VariantType.Int32)
    client.get_node(nodeid=drivenode + '.ParameterSet."S-0-0447"').set_value(3, ua.VariantType.Int16)
    client.get_node(nodeid=drivenode + '.ParameterSet."S-0-0447"').set_value(0, ua.VariantType.Int16)

# Draw Body Functions
def body1():
    global body
    global currentposlabel
    global gotoentry
    btnx = 10
    btny = 4

    for child in body.winfo_children():
        child.destroy()

    jogposbtn = Button(body)
    jogposbtn.configure(text="Jog\nPositive", width=btnx, height=btny, command=jogpos, bg="#999999")
    jogposbtn.grid(row=0, column=0, padx=10, pady=10)

    jognegbtn = Button(body)
    jognegbtn.configure(text="Jog\nNegative", width=btnx, height=btny, command=jogneg, bg="#999999")
    jognegbtn.grid(row=0, column=1, padx=10, pady=10)

    stopjogbtn = Button(body)
    stopjogbtn.configure(text="Stop\nJog", width=btnx, height=btny, command=stopjog, bg="#999999")
    stopjogbtn.grid(row=0, column=2, padx=10, pady=10)

    gotobtn = Button(body)
    gotobtn.configure(text="GoTo\nPosition", width=btnx, height=btny, command=gotopos, bg="#999999")
    gotobtn.grid(row=1, column=0, rowspan=2, padx=10, pady=10)

    gotolabel = Label(body)
    gotolabel.configure(text="GoTo Position:", bg="#333333", fg="#999999")
    gotolabel.grid(row=1, column=1, padx=10, pady=10, sticky=S)

    gotoentry = Entry(body)
    gotoentry.configure(width=btnx, bg="#999999")
    gotoentry.grid(row=2, column=1, padx=10, sticky=N)

    currentposlabellabel = Label(body)
    currentposlabellabel.configure(text="Current Position:", bg="#333333", fg="#999999")
    currentposlabellabel.grid(row=1, column=2, padx=10, pady=10, sticky=S)

    currentposlabel = Label(body)
    currentposlabel.configure(text="xxxxx.xxx", bg="#333333", fg="#999999")
    currentposlabel.grid(row=2, column=2, padx=10, sticky=N)


def body2():
    global body
    global AxisList
    global Master1
    global Master2
    global Slave1
    global Slave2
    btnx = 10
    btny = 4

    for child in body.winfo_children():
        child.destroy()

    SelectedMaster1 = StringVar()
    SelectedMaster2 = StringVar()
    SelectedSlave1 = StringVar()
    SelectedSlave2 = StringVar()

    try:
        SelectedMaster1.set(Master1)
    except:
        Master1 = ""

    try:
        SelectedMaster2.set(Master2)
    except:
        Master2 = ""

    try:
        SelectedSlave1.set(Slave1)
    except:
        Slave1 = ""

    try:
        SelectedSlave2.set(Slave2)
    except:
        Slave2 = ""

    mastermenu1 = OptionMenu(body, SelectedMaster1, *AxisList, command=gearinmaster1)
    mastermenu1.configure(bg="#999999", highlightthickness=0)
    mastermenu1.grid(row=2, column=1, padx=10, pady=10)

    mastermenu2 = OptionMenu(body, SelectedMaster2, *AxisList, command=gearinmaster2)
    mastermenu2.configure(bg="#999999", highlightthickness=0)
    mastermenu2.grid(row=5, column=1, padx=10, pady=10)

    slavemenu1 = OptionMenu(body, SelectedSlave1, *AxisList, command=gearinslave1)
    slavemenu1.configure(bg="#999999", highlightthickness=0)
    slavemenu1.grid(row=2, column=2, padx=10, pady=10)

    slavemenu2 = OptionMenu(body, SelectedSlave2, *AxisList, command=gearinslave2)
    slavemenu2.configure(bg="#999999", highlightthickness=0)
    slavemenu2.grid(row=5, column=2, padx=10, pady=10)

    gearinbutton1 = Button(body)
    gearinbutton1.configure(text="Gear In", bg="#999999", command=gearin1)
    gearinbutton1.grid(row=2, column=3, padx=10, pady=10)

    gearoutbutton1 = Button(body)
    gearoutbutton1.configure(text="Gear Out", bg="#999999", command=gearout1)
    gearoutbutton1.grid(row=2, column=4, padx=10, pady=10)

    gearinbutton2 = Button(body)
    gearinbutton2.configure(text="Gear In", bg="#999999", command=gearin2)
    gearinbutton2.grid(row=5, column=3, padx=10, pady=10)

    gearoutbutton2 = Button(body)
    gearoutbutton2.configure(text="Gear Out", bg="#999999", command=gearout2)
    gearoutbutton2.grid(row=5, column=4, padx=10, pady=10)

    Label(body,text="Gear 1", bg="#333333", fg="#999999").grid(row=2, column=0)
    Label(body, text="Gear 2", bg="#333333", fg="#999999").grid(row=5, column=0)
    Label(body, text="Master", bg="#333333", fg="#999999").grid(row=0, column=1)
    Label(body, text="Slave", bg="#333333", fg="#999999").grid(row=0, column=2)


def body3():
    global body
    global AxisNumber
    global currentposlabel
    global neglimitentry
    global poslimitentry
    global setpositionentry
    btnx = 10
    btny = 4

    for child in body.winfo_children():
        child.destroy()

    neglimitlabel = Label(body)
    neglimitlabel.configure(text="Negative Limit:", bg="#333333", fg="#999999")
    neglimitlabel.grid(row=0, column=0, padx=10, sticky=S)

    neglimitentry = Entry(body)
    neglimitentry.configure(width=btnx, bg="#999999")
    neglimitentry.grid(row=1, column=0, padx=10, pady=(0,10), sticky=N)

    poslimitlabel = Label(body)
    poslimitlabel.configure(text="Positive Limit:", bg="#333333", fg="#999999")
    poslimitlabel.grid(row=0, column=1, padx=10, sticky=S)

    poslimitentry = Entry(body)
    poslimitentry.configure(width=btnx, bg="#999999")
    poslimitentry.grid(row=1, column=1, padx=10, pady=(0,10), sticky=N)

    currentposlabellabel = Label(body)
    currentposlabellabel.configure(text="Current Position:", bg="#333333", fg="#999999")
    currentposlabellabel.grid(row=3, column=0, padx=10, sticky=S)

    currentposlabel = Label(body)
    currentposlabel.configure(text="xxxxx.xxx", bg="#333333", fg="#999999")
    currentposlabel.grid(row=4, column=0, padx=10, sticky=N)

    setlimitsbtn = Button(body)
    setlimitsbtn.configure(width=btnx, text="Set Limits", bg="#999999", command=setlimits)
    setlimitsbtn.grid(row=0, column=2, rowspan=2, padx=10)

    setpositionlabel = Label(body)
    setpositionlabel.configure(text="Set Position:", bg="#333333", fg="#999999")
    setpositionlabel.grid(row=3, column=1, padx=10, sticky=S)

    setpositionentry = Entry(body)
    setpositionentry.configure(width=btnx, bg="#999999")
    setpositionentry.grid(row=4, column=1, padx=10, pady=(0,10), sticky=N)

    setpositionbtn = Button(body)
    setpositionbtn.configure(width=btnx, text="Set Position", bg="#999999", command=setposition)
    setpositionbtn.grid(row=3, column=2, rowspan=2, padx=10)

    insertlimits()

# Create Header
def drawheader():
    global header
    btnx = 10
    btny = 3

    header = Frame(root)
    header.configure(bg="#555555")
    header.grid(row=0,column=0,columnspan=3,sticky=N+E+W)
    header.grid_columnconfigure(100, weight=1)

    openclientbtn = Button(header)
    openclientbtn.configure(text="Connect\nClient", width=btnx, height=btny, command=openclient, bg="#999999")
    openclientbtn.grid(row=0, column=0, sticky=W, padx=10, pady=10)

    disconnectbtn = Button(header)
    disconnectbtn.configure(text="Disconnect\nClient", width=btnx, height=btny, command=disconnect, bg="#999999")
    disconnectbtn.grid(row=0, column=1, sticky=W, pady=10)

    clearerrbtn = Button(header)
    clearerrbtn.configure(text="Reset", width=btnx, height=btny, command=clearerr, bg="#999999")
    clearerrbtn.grid(row=0, column=100, sticky=E, padx=10, pady=10)

    global statusdisplay
    statusdisplay = Label(header, text="Disconnected", bg="#FF0000")
    statusdisplay.grid(row=0, column=2, padx=10)


# Create Footer
def drawfooter():
    global footer
    global AxisNumber
    global jogspd
    global jogacc
    btnx = 10
    btny = 4

    footer = Frame(root)
    footer.configure(bg="#555555")
    footer.grid(row=2,column=0,columnspan=3,sticky=S+E+W)

    try:
        AxisNumber
    except NameError:
        AxisNumber = None

    if AxisNumber == None:
        spdunit = "unit?"
        accunit = "unit?"
        fillspd = ""
        fillacc = ""
    else:
        (_, _, spdunit, accunit, maxspeed, maxaccel) = getaxisinfo()

        if (jogspd.get() == ""):
            fillspd = str(0.01 * maxspeed)
        else:
            fillspd = jogspd.get()

        if (jogacc.get() == ""):
            fillacc = str(0.01 * maxaccel)
        else:
            fillacc = jogacc.get()

    for child in footer.winfo_children():
        child.destroy()

    jogspd = Entry(footer)
    jogspd.configure(width=30, bg="#cccccc")
    jogspd.grid(row=0, column=0, padx=10, pady=10)
    jogspd.insert(0,fillspd)

    jogacc = Entry(footer)
    jogacc.configure(width=30, bg="#cccccc")
    jogacc.grid(row=1, column=0, padx=10, pady=10)
    jogacc.insert(0,fillacc)

    speedlabel= Label(footer)
    speedlabel.configure(text="Velocity (" + spdunit + ")", bg="#555555")
    speedlabel.grid(row=0, column=1, padx=10, pady=10)

    accellabel = Label(footer)
    accellabel.configure(text="Acceleration (" + accunit + ")", bg="#555555")
    accellabel.grid(row=1, column=1, padx=10, pady=10)


# Create Left Side
def drawleftside():
    global leftside
    btnx = 12
    btny = 2

    leftside = Frame(root)
    leftside.configure(bg="#999999")
    leftside.grid(row=1,column=0,sticky=W + N + S)

    body1Button = Button(leftside)
    body1Button.configure(text="Jog Controls", width=btnx, height=btny, command=body1, bg="#cccccc")
    body1Button.grid(row=0, column=0, padx=10, pady=10)

    body2Button = Button(leftside)
    body2Button.configure(text="Gear Axes", width=btnx, height=btny, command=body2, bg="#cccccc")
    body2Button.grid(row=1, column=0, padx=10)

    body3Button = Button(leftside)
    body3Button.configure(text="Set Limits", width=btnx, height=btny, command=body3, bg="#cccccc")
    body3Button.grid(row=2, column=0, padx=10, pady=10)


# Create Right Side
def drawrightside(AxisList):
    global rightside
    btnx = 10
    btny = 2

    rightside = Frame(root)
    rightside.configure(bg="#999999")
    rightside.grid(row=1, column=2, sticky=E + N + S)

    SelectAxisLabel = Label(rightside)
    SelectAxisLabel.configure(text="Select Axis:", bg="#999999")
    SelectAxisLabel.grid(row=0, column=0, sticky=W, padx=10, pady=10)

    SelectedAxis = StringVar()
    axismenu = OptionMenu(rightside, SelectedAxis, *AxisList, command=setaxisnumber)
    axismenu.configure(bg="#cccccc", highlightthickness=0)
    axismenu.grid(row=1, column=0)


# Create Body
def drawbody():
    global body
    body = Frame(root)
    body.configure(bg="#333333")
    body.grid(row=1, column=1)


# Draw Frames
drawheader()
drawfooter()
drawleftside()
drawrightside([""])
drawbody()


# Connect OPCUA Client
threading.Thread(target=openclient).start()


# Tkinter Main Loop
root.mainloop()
