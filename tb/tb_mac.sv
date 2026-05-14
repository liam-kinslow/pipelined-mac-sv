

module tb_mac;

                            // input bit width, parameterised
    parameter WIDTH = 8;  

                            // Clock and reset for the DUT
    logic clk;
    logic rst_n;
    logic en;

    // MAC inputs and output
    logic signed [WIDTH-1:0] a, b;
    logic signed [2*WIDTH:0] result;

                                    // Instantiate the MAC module
    mac dut (
        .clk(clk),
        .rst_n(rst_n),
        .en(en),
        .a(a),
        .b(b),
        .result(result)
    );

    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    // Test stimulus
    initial begin

        rst_n = 0;              // Start with reset active
        en = 1;
        a = 8'd0;
        b = 8'd0;
        #20;
        rst_n = 1;
                                // apply inputs for multiplication
        a = 8'd3;
        b = 8'd4;
        #60;
                                // enable set low to check accumulation result
        a = 8'd3;
        b = 8'd4;
        en = 0;              
        #20;

        #40;
        $finish;
    end

    always @(posedge clk) begin
                                        // Display the current time, enable signal, and result

        $display("Time=%0t en=%b reset=%b result=%0d", $time, en, rst_n, result);
    end

    endmodule