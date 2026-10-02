def generate_datapath(
    dfg,
    schedule,
    fu_binding,
    register_binding
):

    datapath = {
        "inputs": list(dfg.inputs),
        "outputs": list(dfg.outputs),
        "functional_units": sorted(
            set(fu_binding.values())
        ),
        "registers": sorted(
            set(register_binding.values())
        ),
        "operations": [],
        "connections": []
    }

    # --------------------------------
    # Generate operation information
    # --------------------------------

    for cycle in sorted(schedule):

        for node in schedule[cycle]:

            operation = {
                "cycle": cycle,
                "node": node.node_id,
                "operation": node.operation,
                "functional_unit":
                    fu_binding[node.node_id],
                "inputs": list(node.inputs),
                "output": node.output
            }

            # Register receiving the result
            if node.output in register_binding:

                operation["destination_register"] = (
                    register_binding[node.output]
                )

            else:

                operation["destination_register"] = (
                    "OUTPUT"
                )

            datapath["operations"].append(
                operation
            )

    return datapath

def display_datapath(datapath):

    print(
        "\n========== DATAPATH =========="
    )

    print("\nInputs:")

    print(
        "  "
        + ", ".join(datapath["inputs"])
    )

    print("\nFunctional Units:")

    for unit in datapath["functional_units"]:

        print(
            f"  {unit}"
        )

    print("\nRegisters:")

    for register in datapath["registers"]:

        print(
            f"  {register}"
        )

    print("\nOperations:")

    print(
        f"{'Cycle':<8}"
        f"{'Node':<8}"
        f"{'Operation':<10}"
        f"{'FU':<8}"
        f"{'Inputs':<20}"
        f"{'Destination':<12}"
    )

    print("-" * 66)

    for operation in datapath["operations"]:

        inputs = ", ".join(
            operation["inputs"]
        )

        print(
            f"{operation['cycle']:<8}"
            f"{operation['node']:<8}"
            f"{operation['operation']:<10}"
            f"{operation['functional_unit']:<8}"
            f"{inputs:<20}"
            f"{operation['destination_register']:<12}"
        )

    print(
        "=" * 66
    )