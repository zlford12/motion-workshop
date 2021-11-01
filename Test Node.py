from opcua import Client, ua

def main():
    client = Client("opc.tcp://" + open("ip.txt", "r").read() + ":4840", timeout=3)
    client.connect()

    axis_node_list = client.get_node("ns=12;s=Motion.AxisSet.LocalControl").get_referenced_nodes()

    # Remove non-axis children
    for axis_node in axis_node_list:
        display_name = axis_node.get_display_name()
        print(display_name)

    client.disconnect()

if __name__ == "__main__":
    main()
