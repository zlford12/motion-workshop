from tkinter import *
from tkinter import messagebox, Entry
from opcua import Client, ua
import threading
import time


class ConnectionManagement:
    def __init__(self):
        self.connection_monitor_thread = threading.Thread(target=self.is_connected)
        self.connection_desired = False
        self.connection_okay = False
        self.close_requested = False

    def start_connection_monitor_thread(self):
        self.connection_monitor_thread.start()

    def is_connected(self):
        while not self.close_requested:
            try:
                client.get_node("i=2253")
                self.connection_okay = True
            except:
                self.connection_okay = False

            user_interface.update_status_display()

            time.sleep(0.5)

    def open_client(self):
        try:
            if not self.connection_desired:
                self.connection_desired = True
                client.connect()
        except:
            self.connection_desired = False
            messagebox.showerror(title="OPC Error", message="Failure Connecting\nto OPC UA Server")
            return
        motion_control.get_axes()

    def disconnect(self):

        try:
            if self.connection_desired:
                client.disconnect()
                self.connection_desired = False
        except:
            messagebox.showerror(title="OPC Error", message="Failed to\nDisconnect")

        for child in user_interface.right_side.winfo_children():
            child.destroy()

        user_interface.draw_right_side([""])


class MotionControl:
    def __init__(self):
        self.axis_list = [""]
        self.axis_number = None
        self.master1 = None
        self.master2 = None
        self.slave1 = None
        self.slave2 = None

    @staticmethod
    def clear_error():
        try:
            client.get_node("ns=2;s=Application.IO_Names.command").set_value(2, ua.VariantType.Int16)
        except:
            messagebox.showerror(title="OPC Error", message="Failure Writing Data\nto OPC UA Server")

    def get_axes(self):

        user_interface.draw_right_side(self.axis_list)

        # global right_side
        # global AxisList
        # AxisList = [""]
        # try:
        #     AxisString = client.get_node("ns=2;s=Application.CommissioningVar.sRealAxes").get_value()
        #     AxisList = AxisString.split(",")
        # except:
        #     messagebox.showerror(title="OPC Error", message="Failure Reading Data\from OPC UA Server")
        #
        # for child in right_side.winfo_children():
        #     child.destroy()
        #
        # draw_right_side(AxisList)

    def set_axis_number(self, axis_name):

        if axis_name != "":
            self.axis_number = self.axis_list.index(axis_name) + 1
            axis_positioning.insert_limits()

        user_interface.draw_footer()

    def get_axis_info(self):

        positive_limit = client.get_node(
            nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                   + str(self.axis_number)
                   + ".Limits.PositionLimitPositive"
        ).get_value()

        negative_limit = client.get_node(
            nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                   + str(self.axis_number)
                   + ".Limits.PositionLimitNegative"
        ).get_value()

        speed_unit = client.get_node(
            nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                   + str(self.axis_number)
                   + ".Units.Velocity"
        ).get_value()

        accel_unit = client.get_node(
            nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                   + str(self.axis_number)
                   + ".Units.Acceleration"
        ).get_value()

        max_speed = client.get_node(
            nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                   + str(self.axis_number)
                   + ".Limits.VelocityLimitBipolar"
        ).get_value()

        max_accel = client.get_node(
            nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                   + str(self.axis_number)
                   + ".Limits.AccelerationLimitBipolar"
        ).get_value()

        return positive_limit, negative_limit, speed_unit, accel_unit, max_speed, max_accel

    def get_position(self):

        try:
            self.axis_number
        except NameError:
            self.axis_number = None

        if self.axis_number is None:
            return
        else:
            current_position = str(
                client.get_node(
                    nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                           + str(self.axis_number)
                           + ".ActualValues.ActualPosition"
                ).get_value()
            )

            try:
                user_interface.current_position_label.configure(text=current_position)
            except:
                return

    def jog_positive(self):
        (positive_limit, _, _, _, max_speed, max_accel) = self.get_axis_info()

        speed = float(user_interface.jog_speed_entry.get())
        if speed > max_speed:
            speed = max_speed

        accel = float(user_interface.jog_accel_entry.get())
        if accel > max_accel:
            accel = max_accel

        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Position").set_value((positive_limit - 10), ua.VariantType.Float)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Velocity").set_value(speed, ua.VariantType.Float)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Accel").set_value(accel, ua.VariantType.Float)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissionJog_AxisNo").set_value(self.axis_number, ua.VariantType.Int16)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(True)

    def jog_negative(self):
        (_, negative_limit, _, _, max_speed, max_accel) = self.get_axis_info()

        speed = float(user_interface.jog_speed_entry.get())
        if speed > max_speed:
            speed = max_speed

        accel = float(user_interface.jog_accel_entry.get())
        if accel > max_accel:
            accel = max_accel

        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Position").set_value((negative_limit + 10), ua.VariantType.Float)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Velocity").set_value(speed, ua.VariantType.Float)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Accel").set_value(accel, ua.VariantType.Float)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissionJog_AxisNo").set_value(self.axis_number, ua.VariantType.Int16)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(True)

    def stop_jog(self):

        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissionJog_AxisNo").set_value(self.axis_number, ua.VariantType.Int16)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(True)

    def go_to_position(self):
        (positive_limit, negative_limit, _, _, max_speed, max_accel) = self.get_axis_info()

        go_to_position = float(user_interface.go_to_entry.get())
        if go_to_position > (positive_limit - 10):
            go_to_position = positive_limit
        if go_to_position < (negative_limit + 10):
            go_to_position = negative_limit

        speed = float(user_interface.jog_speed_entry.get())
        if speed > max_speed:
            speed = max_speed

        accel = float(user_interface.jog_accel_entry.get())
        if accel > max_accel:
            accel = max_accel

        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Stop").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Position").set_value(go_to_position, ua.VariantType.Float)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Velocity").set_value(speed, ua.VariantType.Float)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.rCommissionJog_Accel").set_value(accel, ua.VariantType.Float)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissionJog_AxisNo").set_value(self.axis_number, ua.VariantType.Int16)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissionJog_Enable").set_value(True)

    def gear_in_master1(self, master):

        self.master1 = master
        master_number = self.axis_list.index(master) + 1

        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissioningGearInMaster_1").set_value(master_number, ua.VariantType.Int16)

    def gear_in_master2(self, master):

        self.master2 = master
        master_number = self.axis_list.index(master) + 1

        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissioningGearInMaster_2").set_value(master_number, ua.VariantType.Int16)

    def gear_in_slave1(self, slave):

        self.slave1 = slave
        slave_number = self.axis_list.index(slave) + 1

        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissioningGearInSlave_1").set_value(slave_number, ua.VariantType.Int16)

    def gear_in_slave2(self, slave):

        self.slave2 = slave
        slave_number = self.axis_list.index(slave) + 1

        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.iCommissioningGearInSlave_2").set_value(slave_number, ua.VariantType.Int16)

    @staticmethod
    def gear_in1():

        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_1").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(True)

    @staticmethod
    def gear_in2():
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_2").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(True)

    @staticmethod
    def gear_out1():
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_1").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_1").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_1").set_value(True)

    @staticmethod
    def gear_out2():
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningGearIn_2").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_2").set_value(False)
        client.get_node(nodeid="ns=2;s=Application.CommissioningVar.bCommissioningStopGearIn_2").set_value(True)


class AxisPositioning:

    @staticmethod
    def insert_limits():
        """Position And Limits"""
        global negative_limit_entry
        global positive_limit_entry
        global set_position_entry

        try:
            negative_limit_entry.delete(0, 100)
            neglimit = str(client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                                                  + str(AxisNumber)
                                                  + ".Limits.PositionLimitNegative").get_value())
            negative_limit_entry.insert(0, neglimit)

            positive_limit_entry.delete(0, 100)
            poslimit = str(client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                                                  + str(AxisNumber)
                                                  + ".Limits.PositionLimitPositive").get_value())
            positive_limit_entry.insert(0, poslimit)

            set_position_entry.delete(0, 100)
        except:
            return

    @staticmethod
    def setlimits():
        global negative_limit_entry
        global positive_limit_entry

        neglimit = ua.DataValue(ua.Variant(float(negative_limit_entry.get()), ua.VariantType.Double))
        poslimit = ua.DataValue(ua.Variant(float(positive_limit_entry.get()), ua.VariantType.Double))
        client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                               + str(AxisNumber)
                               + ".Limits.PositionLimitNegative").set_attribute(ua.AttributeIds.Value, neglimit)
        client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                               + str(AxisNumber)
                               + ".Limits.PositionLimitPositive").set_attribute(ua.AttributeIds.Value, poslimit)

    @staticmethod
    def setposition():
        global AxisNumber
        global set_position_entry

        node = client.get_node(nodeid="ns=12;s=Motion.AxisSet.LocalControl.Axis"
                                      + str(AxisNumber)).get_referenced_nodes()

        for child in node:
            if str(child).find("s=Physical") > -1:
                drivenode = str(child)
                client.get_node(nodeid=drivenode + '.ParameterSet."S-0-0052"').set_value(int(set_position_entry.get()) * 10000, ua.VariantType.Int32)
                client.get_node(nodeid=drivenode + '.ParameterSet."S-0-0447"').set_value(3, ua.VariantType.Int16)
                client.get_node(nodeid=drivenode + '.ParameterSet."S-0-0447"').set_value(0, ua.VariantType.Int16)


class UserInterface:
    def __init__(self):
        self.root = Tk()
        self.body = Frame(self.root)
        self.header = Frame(self.root)
        self.footer = Frame(self.root)
        self.left_side = Frame(self.root)
        self.right_side = Frame(self.root)

        # Body 1 Elements
        self.go_to_entry = None

        # Body 3 Elements
        self.negative_limit_entry = None
        self.positive_limit_entry = None
        self.current_position_label = None
        self.set_position_entry = None

        # Header Elements
        self.status_display = None

        # Footer Elements
        self.jog_speed_entry = None
        self.jog_accel_entry = None


    def body1(self):
        btnx = 10
        btny = 4

        for child in self.body.winfo_children():
            child.destroy()

        jogposbtn = Button(self.body)
        jogposbtn.configure(text="Jog\nPositive", width=btnx, height=btny, command=motion_control.jog_positive, bg="#999999")
        jogposbtn.grid(row=0, column=0, padx=10, pady=10)

        jognegbtn = Button(self.body)
        jognegbtn.configure(text="Jog\nNegative", width=btnx, height=btny, command=motion_control.jog_negative, bg="#999999")
        jognegbtn.grid(row=0, column=1, padx=10, pady=10)

        stopjogbtn = Button(self.body)
        stopjogbtn.configure(text="Stop\nJog", width=btnx, height=btny, command=motion_control.stop_jog, bg="#999999")
        stopjogbtn.grid(row=0, column=2, padx=10, pady=10)

        gotobtn = Button(self.body)
        gotobtn.configure(text="GoTo\nPosition", width=btnx, height=btny, command=motion_control.go_to_position, bg="#999999")
        gotobtn.grid(row=1, column=0, rowspan=2, padx=10, pady=10)

        gotolabel = Label(self.body)
        gotolabel.configure(text="GoTo Position:", bg="#333333", fg="#999999")
        gotolabel.grid(row=1, column=1, padx=10, pady=10, sticky=S)

        self.go_to_entry = Entry(self.body)
        self.go_to_entry.configure(width=btnx, bg="#999999")
        self.go_to_entry.grid(row=2, column=1, padx=10, sticky=N)

        currentposlabellabel = Label(self.body)
        currentposlabellabel.configure(text="Current Position:", bg="#333333", fg="#999999")
        currentposlabellabel.grid(row=1, column=2, padx=10, pady=10, sticky=S)

        self.currentposlabel = Label(self.body)
        self.currentposlabel.configure(text="xxxxx.xxx", bg="#333333", fg="#999999")
        self.currentposlabel.grid(row=2, column=2, padx=10, sticky=N)

    def body2(self):
        global Master1
        global Master2
        global Slave1
        global Slave2

        for child in self.body.winfo_children():
            child.destroy()

        selected_master1 = StringVar()
        selected_master2 = StringVar()
        selected_slave1 = StringVar()
        selected_slave2 = StringVar()

        try:
            selected_master1.set(Master1)
        except:
            Master1 = ""

        try:
            selected_master2.set(Master2)
        except:
            Master2 = ""

        try:
            selected_slave1.set(Slave1)
        except:
            Slave1 = ""

        try:
            selected_slave2.set(Slave2)
        except:
            Slave2 = ""

        mastermenu1 = OptionMenu(self.body, selected_master1, *motion_control.axis_list, command=motion_control.gear_in_master1)
        mastermenu1.configure(bg="#999999", highlightthickness=0)
        mastermenu1.grid(row=2, column=1, padx=10, pady=10)

        mastermenu2 = OptionMenu(self.body, selected_master2, *motion_control.axis_list, command=motion_control.gear_in_master2)
        mastermenu2.configure(bg="#999999", highlightthickness=0)
        mastermenu2.grid(row=5, column=1, padx=10, pady=10)

        slavemenu1 = OptionMenu(self.body, selected_slave1, *motion_control.axis_list, command=motion_control.gear_in_slave1)
        slavemenu1.configure(bg="#999999", highlightthickness=0)
        slavemenu1.grid(row=2, column=2, padx=10, pady=10)

        slavemenu2 = OptionMenu(self.body, selected_slave2, *motion_control.axis_list, command=motion_control.gear_in_slave2)
        slavemenu2.configure(bg="#999999", highlightthickness=0)
        slavemenu2.grid(row=5, column=2, padx=10, pady=10)

        gearinbutton1 = Button(self.body)
        gearinbutton1.configure(text="Gear In", bg="#999999", command=motion_control.gear_in1)
        gearinbutton1.grid(row=2, column=3, padx=10, pady=10)

        gearoutbutton1 = Button(self.body)
        gearoutbutton1.configure(text="Gear Out", bg="#999999", command=motion_control.gear_out1)
        gearoutbutton1.grid(row=2, column=4, padx=10, pady=10)

        gearinbutton2 = Button(self.body)
        gearinbutton2.configure(text="Gear In", bg="#999999", command=motion_control.gear_in2)
        gearinbutton2.grid(row=5, column=3, padx=10, pady=10)

        gearoutbutton2 = Button(self.body)
        gearoutbutton2.configure(text="Gear Out", bg="#999999", command=motion_control.gear_out2)
        gearoutbutton2.grid(row=5, column=4, padx=10, pady=10)

        Label(self.body, text="Gear 1", bg="#333333", fg="#999999").grid(row=2, column=0)
        Label(self.body, text="Gear 2", bg="#333333", fg="#999999").grid(row=5, column=0)
        Label(self.body, text="Master", bg="#333333", fg="#999999").grid(row=0, column=1)
        Label(self.body, text="Slave", bg="#333333", fg="#999999").grid(row=0, column=2)

    def body3(self):
        btnx = 10

        for child in self.body.winfo_children():
            child.destroy()

        neglimitlabel = Label(self.body)
        neglimitlabel.configure(text="Negative Limit:", bg="#333333", fg="#999999")
        neglimitlabel.grid(row=0, column=0, padx=10, sticky=S)

        self.negative_limit_entry = Entry(self.body)
        self.negative_limit_entry.configure(width=btnx, bg="#999999")
        self.negative_limit_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky=N)

        poslimitlabel = Label(self.body)
        poslimitlabel.configure(text="Positive Limit:", bg="#333333", fg="#999999")
        poslimitlabel.grid(row=0, column=1, padx=10, sticky=S)

        self.positive_limit_entry = Entry(self.body)
        self.positive_limit_entry.configure(width=btnx, bg="#999999")
        self.positive_limit_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky=N)

        currentposlabellabel = Label(self.body)
        currentposlabellabel.configure(text="Current Position:", bg="#333333", fg="#999999")
        currentposlabellabel.grid(row=3, column=0, padx=10, sticky=S)

        self.current_position_label = Label(self.body)
        self.current_position_label.configure(text="xxxxx.xxx", bg="#333333", fg="#999999")
        self.current_position_label.grid(row=4, column=0, padx=10, sticky=N)

        setlimitsbtn = Button(self.body)
        setlimitsbtn.configure(width=btnx, text="Set Limits", bg="#999999", command=axis_positioning.setlimits)
        setlimitsbtn.grid(row=0, column=2, rowspan=2, padx=10)

        setpositionlabel = Label(self.body)
        setpositionlabel.configure(text="Set Position:", bg="#333333", fg="#999999")
        setpositionlabel.grid(row=3, column=1, padx=10, sticky=S)

        self.set_position_entry = Entry(self.body)
        self.set_position_entry.configure(width=btnx, bg="#999999")
        self.set_position_entry.grid(row=4, column=1, padx=10, pady=(0, 10), sticky=N)

        setpositionbtn = Button(self.body)
        setpositionbtn.configure(width=btnx, text="Set Position", bg="#999999", command=axis_positioning.setposition)
        setpositionbtn.grid(row=3, column=2, rowspan=2, padx=10)

        axis_positioning.insert_limits()

    def draw_header(self):
        btnx = 10
        btny = 3

        self.header.configure(bg="#555555")
        self.header.grid(row=0, column=0, columnspan=3, sticky=N+E+W)
        self.header.grid_columnconfigure(100, weight=1)

        openclientbtn = Button(self.header)
        openclientbtn.configure(text="Connect\nClient", width=btnx, height=btny, command=connection_management.open_client, bg="#999999")
        openclientbtn.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        disconnectbtn = Button(self.header)
        disconnectbtn.configure(text="Disconnect\nClient", width=btnx, height=btny, command=connection_management.disconnect, bg="#999999")
        disconnectbtn.grid(row=0, column=1, sticky=W, pady=10)

        clearerrbtn = Button(self.header)
        clearerrbtn.configure(text="Reset", width=btnx, height=btny, command=MotionControl.clear_error, bg="#999999")
        clearerrbtn.grid(row=0, column=100, sticky=E, padx=10, pady=10)

        self.status_display = Label(self.header)
        self.status_display.configure(text = "Disconnected", bg = "#FF0000")
        self.status_display.grid(row=0, column=2, padx=10)

    def draw_footer(self):
        global AxisNumber

        self.footer.configure(bg="#555555")
        self.footer.grid(row=2, column=0, columnspan=3, sticky=S+E+W)

        try:
            AxisNumber
        except NameError:
            AxisNumber = None

        if AxisNumber is None:
            speed_unit = "unit?"
            accel_unit = "unit?"
            fillspd = ""
            fillacc = ""
        else:
            (_, _, speed_unit, accel_unit, max_speed, max_accel) = motion_control.get_axis_info()

            if user_interface.jog_speed_entry.get() == "":
                fillspd = str(0.01 * max_speed)
            else:
                fillspd = user_interface.jog_speed_entry.get()

            if user_interface.jog_accel_entry.get() == "":
                fillacc = str(0.01 * max_accel)
            else:
                fillacc = user_interface.jog_accel_entry.get()

        for child in self.footer.winfo_children():
            child.destroy()

        self.jog_speed_entry = Entry(self.footer)
        self.jog_speed_entry.configure(width=30, bg="#cccccc")
        self.jog_speed_entry.grid(row=0, column=0, padx=10, pady=10)
        self.jog_speed_entry.insert(0, fillspd)

        self.jog_accel_entry = Entry(self.footer)
        self.jog_accel_entry.configure(width=30, bg="#cccccc")
        self.jog_accel_entry.grid(row=1, column=0, padx=10, pady=10)
        self.jog_accel_entry.insert(0, fillacc)

        speed_label = Label(self.footer)
        speed_label.configure(text="Velocity (" + speed_unit + ")", bg="#555555")
        speed_label.grid(row=0, column=1, padx=10, pady=10)

        accel_label = Label(self.footer)
        accel_label.configure(text="Acceleration (" + accel_unit + ")", bg="#555555")
        accel_label.grid(row=1, column=1, padx=10, pady=10)

    def draw_left_side(self):
        """Create Left Side"""
        btnx = 12
        btny = 2

        self.left_side.configure(bg="#999999")
        self.left_side.grid(row=1, column=0, sticky=W + N + S)

        body1_button = Button(self.left_side)
        body1_button.configure(text="Jog Controls", width=btnx, height=btny, command=user_interface.body1, bg="#cccccc")
        body1_button.grid(row=0, column=0, padx=10, pady=10)

        body2_button = Button(self.left_side)
        body2_button.configure(text="Gear Axes", width=btnx, height=btny, command=user_interface.body2, bg="#cccccc")
        body2_button.grid(row=1, column=0, padx=10)

        body3_button = Button(self.left_side)
        body3_button.configure(text="Set Limits", width=btnx, height=btny, command=user_interface.body3, bg="#cccccc")
        body3_button.grid(row=2, column=0, padx=10, pady=10)

    def draw_right_side(self, AxisList):

        self.right_side.configure(bg="#999999")
        self.right_side.grid(row=1, column=2, sticky=E + N + S)

        select_axis_label = Label(self.right_side)
        select_axis_label.configure(text="Select Axis:", bg="#999999")
        select_axis_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        selected_axis = StringVar()
        axis_menu = OptionMenu(self.right_side, selected_axis, *AxisList, command=motion_control.set_axis_number)
        axis_menu.configure(bg="#cccccc", highlightthickness=0)
        axis_menu.grid(row=1, column=0)

    def draw_body(self):
        self.body.configure(bg="#333333")
        self.body.grid(row=1, column=1)

    def update_status_display(self):
        if connection_management.connection_desired and connection_management.connection_okay:
            self.status_display.configure(text="Connected", bg="#00FF00")
        else:
            self.status_display.configure(text="Disconnected", bg="#FF0000")

    def cleanup(self):
        connection_management.close_requested = True
        connection_management.connection_monitor_thread.join(2)
        while connection_management.connection_monitor_thread.is_alive():
            print("Thread Still Running")
            time.sleep(0.5)
        print("Thread Finished")
        user_interface.root.update()
        user_interface.root.destroy()
        exit()


def main():
    # Initialize Tkinter
    user_interface.root.protocol("WM_DELETE_WINDOW", user_interface.cleanup)
    user_interface.root.title("Bosch Rexroth Commissioning Tool")
    user_interface.root.geometry("640x480")
    user_interface.root.resizable(width=False, height=False)
    user_interface.root.configure(bg="#333333")
    user_interface.root.grid_columnconfigure(1, weight=1)
    user_interface.root.grid_rowconfigure(1, weight=1)

    # Draw Frames
    user_interface.draw_header()
    user_interface.draw_footer()
    user_interface.draw_left_side()
    user_interface.draw_right_side([""])
    user_interface.draw_body()

    # Connect OPCUA Client
    connection_management.open_client()
    connection_management.start_connection_monitor_thread()

    # Tkinter Main Loop
    user_interface.root.mainloop()


if __name__ == "__main__":
    # Create Global Instances of Class Objects
    connection_management = ConnectionManagement()
    motion_control = MotionControl()
    axis_positioning = AxisPositioning()
    user_interface = UserInterface()
    client = Client("opc.tcp://" + open("ip.txt", "r").read() + ":4840", timeout=3)

    main()
