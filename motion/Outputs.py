from opcua import Client, ua


class Outputs:
    def __init__(self):
        self.output_list = {}

    def populate_outputs(self, client=Client("")):
        self.output_list = {}
        output_names = client.get_node("ns=2;s=Application.MNDT_Vars.arOutputNames").get_children()
        for i in range(len(output_names)):
            if output_names[i].get_value() != "" \
                    and output_names[i].get_data_type_as_variant_type() == ua.VariantType.String:
                self.output_list[output_names[i].get_value()] = i
