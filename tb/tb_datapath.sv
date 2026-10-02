`timescale 1ns/1ps

module tb_datapath;

    parameter WIDTH = 16;

    logic clk;
    logic reset;

    logic [WIDTH-1:0] a;
    logic [WIDTH-1:0] b;
    logic [WIDTH-1:0] c;
    logic [WIDTH-1:0] d;
    logic [WIDTH-1:0] e;
    logic [WIDTH-1:0] f;
    logic [WIDTH-1:0] g;
    logic [WIDTH-1:0] h;

    logic [WIDTH-1:0] y;


    // ==========================================
    // DUT
    // ==========================================

    generated_datapath #(
        .WIDTH(WIDTH)
    ) dut (

        .clk(clk),
        .reset(reset),

        .a(a),
        .b(b),
        .c(c),
        .d(d),
        .e(e),
        .f(f),
        .g(g),
        .h(h),

        .y(y)
    );


    // ==========================================
    // Clock generation
    // ==========================================

    initial begin
        clk = 1'b0;

        forever #5 clk = ~clk;
    end


    // ==========================================
    // Test
    // ==========================================

    initial begin

        // --------------------------------------
        // Input values
        // --------------------------------------

        a = 16'd1;
        b = 16'd2;

        c = 16'd3;
        d = 16'd4;

        e = 16'd5;
        f = 16'd6;

        g = 16'd7;
        h = 16'd8;


        // --------------------------------------
        // Reset
        // --------------------------------------

        reset = 1'b1;

        #12;

        reset = 1'b0;


        // --------------------------------------
        // Wait for 5-cycle schedule
        // --------------------------------------

        #60;


        // --------------------------------------
        // Display result
        // --------------------------------------

        $display("");
        $display("======================================");
        $display("          HLS DATAPATH TEST");
        $display("======================================");

        $display("a = %0d", a);
        $display("b = %0d", b);
        $display("c = %0d", c);
        $display("d = %0d", d);
        $display("e = %0d", e);
        $display("f = %0d", f);
        $display("g = %0d", g);
        $display("h = %0d", h);

        $display("--------------------------------------");

        $display(
            "Expected y = %0d",
            ((a + b) * (c + d)) + (e + f) + (g * h)
        );

        $display(
            "Actual y   = %0d",
            y
        );

        $display("--------------------------------------");


        if (
            y ==
            ((a + b) * (c + d))
            + (e + f)
            + (g * h)
        ) begin

            $display("RESULT: PASS");

        end
        else begin

            $display("RESULT: FAIL");

        end


        $display("======================================");

        $finish;

    end


    // ==========================================
    // Waveform
    // ==========================================

    initial begin

        $dumpfile("output/datapath.vcd");

        $dumpvars(0, tb_datapath);

    end

endmodule