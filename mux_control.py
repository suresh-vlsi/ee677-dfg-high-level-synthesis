def variable_to_source(variable, register_binding):

    # Intermediate variable stored in a register
    if variable in register_binding:
        return register_binding[variable]

    # Primary input
    return variable


def generate_mux_controls(
    dfg,
    schedule,
    fu_binding,
    register_binding
):

    controls = []

    for cycle in sorted(schedule):

        for node in schedule[cycle]:

            fu = fu_binding[node.node_id]

            input_a = variable_to_source(
                node.inputs[0],
                register_binding
            )

            input_b = variable_to_source(
                node.inputs[1],
                register_binding
            )

            control = {
                "cycle": cycle,
                "node": node.node_id,
                "functional_unit": fu,
                "input_a": input_a,
                "input_b": input_b,
                "output": node.output
            }

            controls.append(control)

    return controls

def display_mux_controls(controls):

    print(
        "\n========== MUX / CONTROL SIGNALS =========="
    )

    print(
        f"{'Cycle':<8}"
        f"{'Node':<8}"
        f"{'FU':<8}"
        f"{'Input A':<12}"
        f"{'Input B':<12}"
        f"{'Output':<10}"
    )

    print("-" * 58)

    for control in controls:

        print(
            f"{control['cycle']:<8}"
            f"{control['node']:<8}"
            f"{control['functional_unit']:<8}"
            f"{control['input_a']:<12}"
            f"{control['input_b']:<12}"
            f"{control['output']:<10}"
        )

    print("=" * 58)