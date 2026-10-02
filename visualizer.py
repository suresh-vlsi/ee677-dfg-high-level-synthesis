import os
import re
import subprocess
import sys


# ============================================================
# DFG PARSER
# ============================================================

def parse_dfg(filename):
    """
    Parse the HLS DFG file.

    Expected format:

        INPUTS: a,b,c,d,e,f,g,h

        NODE: N1 ADD a b x1
        NODE: N2 ADD c d x2
        NODE: N3 MUL x1 x2 x3
        NODE: N4 ADD e f x4
        NODE: N5 ADD x3 x4 x5
        NODE: N6 MUL g h x6
        NODE: N7 ADD x5 x6 y

        OUTPUTS: y
    """

    operations = []
    primary_inputs = []
    declared_outputs = []

    with open(filename, "r") as file:

        for raw_line in file:

            line = raw_line.strip()

            # ------------------------------------------------
            # Ignore empty lines
            # ------------------------------------------------

            if not line:
                continue

            # ------------------------------------------------
            # Ignore comments
            # ------------------------------------------------

            if line.startswith("#"):
                continue

            # ------------------------------------------------
            # Parse INPUTS
            # ------------------------------------------------

            if line.startswith("INPUTS:"):

                values = line.split(":", 1)[1]

                primary_inputs = [
                    x.strip()
                    for x in values.split(",")
                    if x.strip()
                ]

                continue

            # ------------------------------------------------
            # Parse OUTPUTS
            # ------------------------------------------------

            if line.startswith("OUTPUTS:"):

                values = line.split(":", 1)[1]

                declared_outputs = [
                    x.strip()
                    for x in values.split(",")
                    if x.strip()
                ]

                continue

            # ------------------------------------------------
            # Parse NODE
            # ------------------------------------------------

            if line.startswith("NODE:"):

                parts = line.split()

                # Expected:
                #
                # NODE: N1 ADD a b x1
                #
                # parts:
                # 0      1  2   3 4 5
                # NODE:  N1 ADD a b x1

                if len(parts) != 6:

                    print(
                        f"WARNING: Invalid NODE line:\n"
                        f"  {line}"
                    )

                    continue

                node = parts[1]
                operation = parts[2].upper()
                input_a = parts[3]
                input_b = parts[4]
                output = parts[5]

                operations.append({
                    "node": node,
                    "op": operation,
                    "inputs": [input_a, input_b],
                    "output": output
                })

    return operations, primary_inputs, declared_outputs


# ============================================================
# GRAPHVIZ NODE STYLE
# ============================================================

def get_operation_style(operation):

    operation = operation.upper()

    if operation == "ADD":

        return (
            "ADD",
            "lightblue"
        )

    if operation == "SUB":

        return (
            "SUB",
            "lightblue"
        )

    if operation == "MUL":

        return (
            "MUL",
            "lightgreen"
        )

    if operation == "DIV":

        return (
            "DIV",
            "lightyellow"
        )

    return (
        operation,
        "lightgray"
    )


# ============================================================
# GENERATE DOT
# ============================================================

def generate_dot(
    operations,
    primary_inputs,
    declared_outputs,
    dot_file
):

    lines = []

    # --------------------------------------------------------
    # Graph header
    # --------------------------------------------------------

    lines.append("digraph DFG {")
    lines.append("")
    lines.append("    rankdir=LR;")
    lines.append("    splines=ortho;")
    lines.append("    nodesep=0.7;")
    lines.append("    ranksep=1.0;")
    lines.append("")

    lines.append("    graph [")
    lines.append('        fontname="Arial",')
    lines.append(
        '        label="Data Flow Graph (DFG) — Automatic Visualization",'
    )
    lines.append("        labelloc=t,")
    lines.append("        fontsize=20,")
    lines.append("        pad=0.3")
    lines.append("    ];")
    lines.append("")

    lines.append("    node [")
    lines.append('        fontname="Arial",')
    lines.append("        fontsize=10")
    lines.append("    ];")
    lines.append("")

    lines.append("    edge [")
    lines.append('        fontname="Arial",')
    lines.append("        fontsize=9,")
    lines.append("        arrowsize=0.7")
    lines.append("    ];")
    lines.append("")

    # --------------------------------------------------------
    # Primary input nodes
    # --------------------------------------------------------

    for signal in primary_inputs:

        safe_name = re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            signal
        )

        lines.append(
            f'    IN_{safe_name} '
            f'[shape=circle, '
            f'label="{signal}", '
            f'fillcolor="white", '
            f'style="filled"];'
        )

    lines.append("")

    # --------------------------------------------------------
    # Operation nodes
    # --------------------------------------------------------

    for item in operations:

        node = item["node"]
        operation = item["op"]
        output = item["output"]

        operation_label, fill_color = get_operation_style(
            operation
        )

        label = (
            f"{node}\\n"
            f"{operation_label}\\n"
            f"{output}"
        )

        lines.append(
            f'    {node} ['
            f'shape=box, '
            f'style="rounded,filled", '
            f'label="{label}", '
            f'fillcolor="{fill_color}", '
            f'penwidth=1.5'
            f'];'
        )

    lines.append("")

    # --------------------------------------------------------
    # Determine outputs
    # --------------------------------------------------------

    produced_values = {
        item["output"]
        for item in operations
    }

    consumed_values = {
        signal
        for item in operations
        for signal in item["inputs"]
    }

    # Use explicitly declared outputs when available.
    if declared_outputs:

        final_outputs = declared_outputs

    else:

        final_outputs = sorted(
            produced_values - consumed_values
        )

    # --------------------------------------------------------
    # Output nodes
    # --------------------------------------------------------

    for signal in final_outputs:

        safe_name = re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            signal
        )

        lines.append(
            f'    OUT_{safe_name} '
            f'[shape=doublecircle, '
            f'label="{signal}", '
            f'fillcolor="lightcyan", '
            f'style="filled"];'
        )

    lines.append("")

    # --------------------------------------------------------
    # Map produced signal → generating node
    # --------------------------------------------------------

    producer = {
        item["output"]: item["node"]
        for item in operations
    }

    # --------------------------------------------------------
    # Create data-flow edges
    # --------------------------------------------------------

    for item in operations:

        destination_node = item["node"]

        for index, signal in enumerate(item["inputs"]):

            # ----------------------------------------------
            # Signal comes from another operation
            # ----------------------------------------------

            if signal in producer:

                source_node = producer[signal]

                lines.append(
                    f'    {source_node} -> {destination_node} '
                    f'[xlabel="{signal}"];'
                )

            # ----------------------------------------------
            # Signal is a primary input
            # ----------------------------------------------

            else:

                safe_name = re.sub(
                    r"[^A-Za-z0-9_]",
                    "_",
                    signal
                )

                lines.append(
                    f'    IN_{safe_name} -> {destination_node};'
                )

    lines.append("")

    # --------------------------------------------------------
    # Connect final outputs
    # --------------------------------------------------------

    for signal in final_outputs:

        if signal not in producer:
            continue

        source_node = producer[signal]

        safe_name = re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            signal
        )

        lines.append(
            f'    {source_node} -> OUT_{safe_name};'
        )

    lines.append("")

    # --------------------------------------------------------
    # Close graph
    # --------------------------------------------------------

    lines.append("}")

    with open(dot_file, "w") as file:

        file.write(
            "\n".join(lines)
        )


# ============================================================
# GENERATE PNG / SVG
# ============================================================

def generate_images(dot_file, output_directory):

    png_file = os.path.join(
        output_directory,
        "dfg_auto.png"
    )

    svg_file = os.path.join(
        output_directory,
        "dfg_auto.svg"
    )

    # --------------------------------------------------------
    # PNG
    # --------------------------------------------------------

    subprocess.run(
        [
            "dot",
            "-Tpng",
            dot_file,
            "-o",
            png_file
        ],
        check=True
    )

    # --------------------------------------------------------
    # SVG
    # --------------------------------------------------------

    subprocess.run(
        [
            "dot",
            "-Tsvg",
            dot_file,
            "-o",
            svg_file
        ],
        check=True
    )

    return png_file, svg_file


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Check command-line argument
    # --------------------------------------------------------

    if len(sys.argv) != 2:

        print()
        print(
            "Usage:"
        )
        print(
            "  python3 visualizer.py input/example.dfg"
        )
        print()

        sys.exit(1)

    dfg_file = sys.argv[1]

    # --------------------------------------------------------
    # Check DFG file
    # --------------------------------------------------------

    if not os.path.isfile(dfg_file):

        print()
        print(
            f"ERROR: DFG file not found:"
        )
        print(
            f"  {dfg_file}"
        )
        print()

        sys.exit(1)

    # --------------------------------------------------------
    # Create docs directory
    # --------------------------------------------------------

    docs_directory = "docs"

    os.makedirs(
        docs_directory,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Parse DFG
    # --------------------------------------------------------

    operations, primary_inputs, declared_outputs = parse_dfg(
        dfg_file
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if not operations:

        print()
        print(
            "ERROR: No DFG operations found."
        )
        print()
        print(
            "Expected format:"
        )
        print(
            "  NODE: N1 ADD a b x1"
        )
        print(
            "  NODE: N2 MUL x1 x2 x3"
        )
        print()

        sys.exit(1)

    # --------------------------------------------------------
    # Generate DOT
    # --------------------------------------------------------

    dot_file = os.path.join(
        docs_directory,
        "dfg_auto.dot"
    )

    generate_dot(
        operations,
        primary_inputs,
        declared_outputs,
        dot_file
    )

    # --------------------------------------------------------
    # Generate images
    # --------------------------------------------------------

    png_file, svg_file = generate_images(
        dot_file,
        docs_directory
    )

    # --------------------------------------------------------
    # Print summary
    # --------------------------------------------------------

    print()
    print("==============================================")
    print("          DFG VISUALIZATION")
    print("==============================================")
    print()
    print(f"Input file : {dfg_file}")
    print()
    print(f"Operations : {len(operations)}")
    print(
        f"Inputs     : {', '.join(primary_inputs)}"
    )
    print(
        f"Outputs    : {', '.join(declared_outputs)}"
    )
    print()
    print(f"DOT file   : {dot_file}")
    print(f"PNG file   : {png_file}")
    print(f"SVG file   : {svg_file}")
    print()
    print("==============================================")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()