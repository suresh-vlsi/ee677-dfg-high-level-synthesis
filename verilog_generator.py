def generate_verilog(
    dfg,
    schedule,
    fu_binding,
    register_binding,
    controls,
    filename="output/datapath.v"
):

    lines = []

    # ==================================================
    # Module declaration
    # ==================================================

    lines.append("`timescale 1ns/1ps")
    lines.append("")
    lines.append("module generated_datapath #(")
    lines.append("    parameter WIDTH = 16")
    lines.append(")(")

    # Primary inputs
    input_ports = []

    for signal in dfg.inputs:
        input_ports.append(
            f"    input  logic [WIDTH-1:0] {signal}"
        )

    input_ports.append(
        "    input  logic clk"
    )

    input_ports.append(
        "    input  logic reset"
    )

    input_ports.append(
        "    output logic [WIDTH-1:0] y"
    )

    lines.append(",\n".join(input_ports))
    lines.append(");")
    lines.append("")

    # ==================================================
    # Registers
    # ==================================================

    lines.append("    // =============================================")
    lines.append("    // Physical Registers")
    lines.append("    // =============================================")

    for register in sorted(
        set(register_binding.values())
    ):

        lines.append(
            f"    logic [WIDTH-1:0] {register};"
        )

    lines.append("")

    # ==================================================
    # Cycle counter
    # ==================================================

    lines.append("    // =============================================")
    lines.append("    // Control / Cycle Counter")
    lines.append("    // =============================================")

    lines.append(
        "    logic [2:0] cycle;"
    )

    lines.append("")

    lines.append(
        "    always_ff @(posedge clk) begin"
    )

    lines.append(
        "        if (reset)"
    )

    lines.append(
        "            cycle <= 3'd1;"
    )

    lines.append(
        "        else if (cycle < 3'd5)"
    )

    lines.append(
        "            cycle <= cycle + 3'd1;"
    )

    lines.append(
        "        else"
    )

    lines.append(
        "            cycle <= 3'd5;"
    )

    lines.append(
        "    end"
    )

    lines.append("")

    # ==================================================
    # MUX outputs
    # ==================================================

    lines.append("    // =============================================")
    lines.append("    // MUX Outputs")
    lines.append("    // =============================================")

    lines.append(
        "    logic [WIDTH-1:0] add_a;"
    )

    lines.append(
        "    logic [WIDTH-1:0] add_b;"
    )

    lines.append(
        "    logic [WIDTH-1:0] mul_a;"
    )

    lines.append(
        "    logic [WIDTH-1:0] mul_b;"
    )

    lines.append("")

    # ==================================================
    # Functional Unit Outputs
    # ==================================================

    lines.append(
        "    logic [WIDTH-1:0] add_result;"
    )

    lines.append(
        "    logic [WIDTH-1:0] mul_result;"
    )

    lines.append("")

    # ==================================================
    # ADD input MUX A
    # ==================================================

    lines.append("    // ADD1 input A MUX")

    lines.append(
        "    always_comb begin"
    )

    lines.append(
        "        case (cycle)"
    )

    lines.append(
        f"            3'd1: add_a = a;"
    )

    lines.append(
        f"            3'd2: add_a = c;"
    )

    lines.append(
        f"            3'd3: add_a = e;"
    )

    lines.append(
        f"            3'd4: add_a = R1;"
    )

    lines.append(
        f"            3'd5: add_a = R1;"
    )

    lines.append(
        "            default: add_a = '0;"
    )

    lines.append(
        "        endcase"
    )

    lines.append(
        "    end"
    )

    lines.append("")

    # ==================================================
    # ADD input MUX B
    # ==================================================

    lines.append("    // ADD1 input B MUX")

    lines.append(
        "    always_comb begin"
    )

    lines.append(
        "        case (cycle)"
    )

    lines.append(
        "            3'd1: add_b = b;"
    )

    lines.append(
        "            3'd2: add_b = d;"
    )

    lines.append(
        "            3'd3: add_b = f;"
    )

    lines.append(
        "            3'd4: add_b = R3;"
    )

    lines.append(
        "            3'd5: add_b = R2;"
    )

    lines.append(
        "            default: add_b = '0;"
    )

    lines.append(
        "        endcase"
    )

    lines.append(
        "    end"
    )

    lines.append("")

    # ==================================================
    # MUL input MUX A
    # ==================================================

    lines.append("    // MUL1 input A MUX")

    lines.append(
        "    always_comb begin"
    )

    lines.append(
        "        case (cycle)"
    )

    lines.append(
        "            3'd1: mul_a = g;"
    )

    lines.append(
        "            3'd3: mul_a = R1;"
    )

    lines.append(
        "            default: mul_a = '0;"
    )

    lines.append(
        "        endcase"
    )

    lines.append(
        "    end"
    )

    lines.append("")

    # ==================================================
    # MUL input MUX B
    # ==================================================

    lines.append("    // MUL1 input B MUX")

    lines.append(
        "    always_comb begin"
    )

    lines.append(
        "        case (cycle)"
    )

    lines.append(
        "            3'd1: mul_b = h;"
    )

    lines.append(
        "            3'd3: mul_b = R3;"
    )

    lines.append(
        "            default: mul_b = '0;"
    )

    lines.append(
        "        endcase"
    )

    lines.append(
        "    end"
    )

    lines.append("")

    # ==================================================
    # Functional Units
    # ==================================================

    lines.append(
        "    // ============================================="
    )

    lines.append(
        "    // Functional Units"
    )

    lines.append(
        "    // ============================================="
    )

    lines.append(
        "    assign add_result = add_a + add_b;"
    )

    lines.append(
        "    assign mul_result = mul_a * mul_b;"
    )

    lines.append("")

    # ==================================================
    # Register write logic
    # ==================================================

    lines.append(
        "    // ============================================="
    )

    lines.append(
        "    // Register Write / Output Logic"
    )

    lines.append(
        "    // ============================================="
    )

    lines.append(
        "    always_ff @(posedge clk) begin"
    )

    lines.append(
        "        if (reset) begin"
    )

    for register in sorted(
        set(register_binding.values())
    ):

        lines.append(
            f"            {register} <= '0;"
        )

    lines.append(
        "            y <= '0;"
    )

    lines.append(
        "        end"
    )

    lines.append(
        "        else begin"
    )

    # Cycle 1
    lines.append(
        "            if (cycle == 3'd1) begin"
    )

    lines.append(
        "                R1 <= add_result;"
    )

    lines.append(
        "                R2 <= mul_result;"
    )

    lines.append(
        "            end"
    )

    # Cycle 2
    lines.append(
        "            else if (cycle == 3'd2) begin"
    )

    lines.append(
        "                R3 <= add_result;"
    )

    lines.append(
        "            end"
    )

    # Cycle 3
    lines.append(
        "            else if (cycle == 3'd3) begin"
    )

    lines.append(
        "                R1 <= mul_result;"
    )

    lines.append(
        "                R3 <= add_result;"
    )

    lines.append(
        "            end"
    )

    # Cycle 4
    lines.append(
        "            else if (cycle == 3'd4) begin"
    )

    lines.append(
        "                R1 <= add_result;"
    )

    lines.append(
        "            end"
    )

    # Cycle 5
    lines.append(
        "            else if (cycle == 3'd5) begin"
    )

    lines.append(
        "                y <= add_result;"
    )

    lines.append(
        "            end"
    )

    lines.append(
        "        end"
    )

    lines.append(
        "    end"
    )

    lines.append("")

    lines.append(
        "endmodule"
    )

    # ==================================================
    # Write file
    # ==================================================

    with open(filename, "w") as file:

        file.write(
            "\n".join(lines)
        )

    return filename