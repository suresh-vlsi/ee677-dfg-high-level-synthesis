def generate_netlist(
    dfg,
    schedule,
    fu_binding,
    register_binding,
    controls
):

    netlist = {
        "inputs": list(dfg.inputs),
        "outputs": list(dfg.outputs),
        "registers": sorted(
            set(register_binding.values())
        ),
        "functional_units": sorted(
            set(fu_binding.values())
        ),
        "muxes": [],
        "connections": [],
        "operations": []
    }

    # --------------------------------
    # Generate MUXes
    # --------------------------------

    fu_inputs = {}

    for control in controls:

        fu = control["functional_unit"]

        if fu not in fu_inputs:
            fu_inputs[fu] = {
                "A": set(),
                "B": set()
            }

        fu_inputs[fu]["A"].add(
            control["input_a"]
        )

        fu_inputs[fu]["B"].add(
            control["input_b"]
        )

    for fu in sorted(fu_inputs):

        netlist["muxes"].append({
            "name": f"{fu}_A_MUX",
            "functional_unit": fu,
            "port": "A",
            "inputs": sorted(
                fu_inputs[fu]["A"]
            )
        })

        netlist["muxes"].append({
            "name": f"{fu}_B_MUX",
            "functional_unit": fu,
            "port": "B",
            "inputs": sorted(
                fu_inputs[fu]["B"]
            )
        })

    # --------------------------------
    # Generate operation connections
    # --------------------------------

    for control in controls:

        operation = {
            "cycle": control["cycle"],
            "node": control["node"],
            "functional_unit":
                control["functional_unit"],
            "input_a": control["input_a"],
            "input_b": control["input_b"],
            "output": control["output"]
        }

        # Determine destination
        output = control["output"]

        if output in register_binding:

            operation["destination"] = (
                register_binding[output]
            )

        else:

            operation["destination"] = (
                "OUTPUT"
            )

        netlist["operations"].append(
            operation
        )

    return netlist

def display_netlist(netlist):

    print(
        "\n========== GENERATED NETLIST =========="
    )

    print("\nPRIMARY INPUTS:")

    for signal in netlist["inputs"]:

        print(
            f"  INPUT {signal}"
        )

    print("\nREGISTERS:")

    for register in netlist["registers"]:

        print(
            f"  REGISTER {register}"
        )

    print("\nFUNCTIONAL UNITS:")

    for unit in netlist["functional_units"]:

        print(
            f"  {unit}"
        )

    print("\nMULTIPLEXERS:")

    for mux in netlist["muxes"]:

        inputs = ", ".join(
            mux["inputs"]
        )

        print(
            f"  {mux['name']}: "
            f"{inputs}"
        )

    print("\nOPERATIONS / CONNECTIONS:")

    print(
        f"{'Cycle':<7}"
        f"{'Node':<7}"
        f"{'FU':<7}"
        f"{'A':<8}"
        f"{'B':<8}"
        f"{'DEST':<10}"
    )

    print("-" * 57)

    for operation in netlist["operations"]:

        print(
            f"{operation['cycle']:<7}"
            f"{operation['node']:<7}"
            f"{operation['functional_unit']:<7}"
            f"{operation['input_a']:<8}"
            f"{operation['input_b']:<8}"
            f"{operation['destination']:<10}"
        )

    print(
        "\nOUTPUTS:"
    )

    for output in netlist["outputs"]:

        print(
            f"  OUTPUT {output}"
        )

    print(
        "=======================================\n"
    )