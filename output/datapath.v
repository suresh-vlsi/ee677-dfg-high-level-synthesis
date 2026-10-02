`timescale 1ns/1ps

module generated_datapath #(
    parameter WIDTH = 16
)(
    input  logic [WIDTH-1:0] a,
    input  logic [WIDTH-1:0] b,
    input  logic [WIDTH-1:0] c,
    input  logic [WIDTH-1:0] d,
    input  logic [WIDTH-1:0] e,
    input  logic [WIDTH-1:0] f,
    input  logic [WIDTH-1:0] g,
    input  logic [WIDTH-1:0] h,
    input  logic clk,
    input  logic reset,
    output logic [WIDTH-1:0] y
);

    // =============================================
    // Physical Registers
    // =============================================
    logic [WIDTH-1:0] R1;
    logic [WIDTH-1:0] R2;
    logic [WIDTH-1:0] R3;

    // =============================================
    // Control / Cycle Counter
    // =============================================
    logic [2:0] cycle;

    always_ff @(posedge clk) begin
        if (reset)
            cycle <= 3'd1;
        else if (cycle < 3'd5)
            cycle <= cycle + 3'd1;
        else
            cycle <= 3'd5;
    end

    // =============================================
    // MUX Outputs
    // =============================================
    logic [WIDTH-1:0] add_a;
    logic [WIDTH-1:0] add_b;
    logic [WIDTH-1:0] mul_a;
    logic [WIDTH-1:0] mul_b;

    logic [WIDTH-1:0] add_result;
    logic [WIDTH-1:0] mul_result;

    // ADD1 input A MUX
    always_comb begin
        case (cycle)
            3'd1: add_a = a;
            3'd2: add_a = c;
            3'd3: add_a = e;
            3'd4: add_a = R1;
            3'd5: add_a = R1;
            default: add_a = '0;
        endcase
    end

    // ADD1 input B MUX
    always_comb begin
        case (cycle)
            3'd1: add_b = b;
            3'd2: add_b = d;
            3'd3: add_b = f;
            3'd4: add_b = R3;
            3'd5: add_b = R2;
            default: add_b = '0;
        endcase
    end

    // MUL1 input A MUX
    always_comb begin
        case (cycle)
            3'd1: mul_a = g;
            3'd3: mul_a = R1;
            default: mul_a = '0;
        endcase
    end

    // MUL1 input B MUX
    always_comb begin
        case (cycle)
            3'd1: mul_b = h;
            3'd3: mul_b = R3;
            default: mul_b = '0;
        endcase
    end

    // =============================================
    // Functional Units
    // =============================================
    assign add_result = add_a + add_b;
    assign mul_result = mul_a * mul_b;

    // =============================================
    // Register Write / Output Logic
    // =============================================
    always_ff @(posedge clk) begin
        if (reset) begin
            R1 <= '0;
            R2 <= '0;
            R3 <= '0;
            y <= '0;
        end
        else begin
            if (cycle == 3'd1) begin
                R1 <= add_result;
                R2 <= mul_result;
            end
            else if (cycle == 3'd2) begin
                R3 <= add_result;
            end
            else if (cycle == 3'd3) begin
                R1 <= mul_result;
                R3 <= add_result;
            end
            else if (cycle == 3'd4) begin
                R1 <= add_result;
            end
            else if (cycle == 3'd5) begin
                y <= add_result;
            end
        end
    end

endmodule