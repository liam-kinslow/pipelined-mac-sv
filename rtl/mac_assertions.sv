
module mac #(
    parameter WIDTH = 8  // input bit width, parameterised

)(
    input  logic                    clk,
    input  logic                    rst_n,    // active low reset
    input  logic                    en,       // enable accumulation
    input  logic signed [WIDTH-1:0] a, b,     // inputs
    output logic signed [2*WIDTH:0] result    // accumulator output
);

// Stage 1: inputs into registers
logic signed [WIDTH-1:0] a_reg, b_reg;
logic                       en_reg;

always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin                        // reset registers
        a_reg <= 0;
        b_reg <= 0;
        en_reg <= 0;
    end else begin                           // capture inputs
        a_reg <= a;
        b_reg <= b;
        en_reg <= en;
    end
end

// Stage 2: multiplication
logic signed [2*WIDTH-1:0] prod_reg;
logic                       en_reg2;

always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin                          // reset registers
        prod_reg <= 0;
        en_reg2 <= 0;
    end else begin                             // capture multiplication result
        prod_reg <= a_reg * b_reg;
        en_reg2 <= en_reg;                    // pass enable to next stage
    end
end

// Stage 3: accumulation 
logic signed [2*WIDTH:0] acc_reg;
always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin                          // reset registers
        acc_reg <= 0;
    end else if (en_reg2) begin                 // accumulate if enabled
        acc_reg <= acc_reg + prod_reg;
    end
end

// Output assignment 
assign result = acc_reg;

// Assertions to check correct behavior
    localparam MAX_VAL = (2**(2*WIDTH-1))-1;                  // maximum positive value for signed output
    localparam MIN_VAL = -(2**(2*WIDTH-1));                  // minimum negative value for signed output

assert property (@(posedge clk) $fell(rst_n) |=> (result == 0))     // Reset should clear the accumulator
    else $error("Reset did not clear the accumulator");

assert property (@(posedge clk) $fell(en) |-> ##4 $stable(result))  // When enable falls, result holds the accumulated value after 2 cycles
    else $error("Result did not hold the accumulated value when enable fell"); 

assert property (@(posedge clk) disable iff (!rst_n) $rose(en) |-> ##2 !$stable(result))  // When enable rises, result should change after 3 cycles
    else $error("Result did not change after enable rose");

assert property (@(posedge clk) 1 |-> (result <= MAX_VAL && result >= MIN_VAL))  // Check for overflow in accumulation
    else $error("Overflow detected in accumulation");

endmodule
