// Board to act as the top-level entity of the physical circuit
module BOARD(input [9:0] SW,
            input [3:0] KEY,
            input CLOCK,
				output [9:0] LEDR,
				output [6:0] HEX0,
				output [6:0] HEX1,
				output [6:0] HEX2,
				output [6:0] HEX3,
				output [6:0] HEX4,
				output [6:0] HEX5);

	 // wire up the chips of your circuit here.

     // here an example chip outputs to one of the 7-seg displays
     // using example: `MyChipDesign chip(input button, output [3:0] chip_output);`
     wire [3:0] chip_output;
	 MyChipDesign chip(.button(KEY[0]), .chip_output(chip_output));
     SevenSegDisplay chipOut(.BINARY(chip_output), DISPLAY(HEX0));


	 // set everything to be off if you don't use it
	 assign LEDR = 10'b00_0000_0000;
//   assign HEX0 = 7'b1111111;      // used above
	 assign HEX1 = 7'b1111111;
	 assign HEX2 = 7'b1111111;
	 assign HEX3 = 7'b1111111;
	 assign HEX4 = 7'b1111111;
	 assign HEX5 = 7'b1111111;

endmodule

// Seven Segment Display Module
module SevenSegDisplay(input [3:0] BINARY, output reg [6:0] DISPLAY);
	always @(*)
		case (BINARY)
			4'b0000: DISPLAY = ~7'b0111111;
			4'b0001: DISPLAY = ~7'b0000110;
			4'b0010: DISPLAY = ~7'b1011011;
			4'b0011: DISPLAY = ~7'b1001111;
			4'b0100: DISPLAY = ~7'b1100110;
			4'b0101: DISPLAY = ~7'b1101101;
			4'b0110: DISPLAY = ~7'b1111101;
			4'b0111: DISPLAY = ~7'b0000111;
			4'b1000: DISPLAY = ~7'b1111111;
			4'b1001: DISPLAY = ~7'b1100111;
			4'b1010: DISPLAY = ~7'b1110111;
			4'b1011: DISPLAY = ~7'b1111100;
			4'b1100: DISPLAY = ~7'b0111001;
			4'b1101: DISPLAY = ~7'b1011110;
			4'b1110: DISPLAY = ~7'b1111001;
			4'b1111: DISPLAY = ~7'b1110001;
			default: DISPLAY = ~7'b0000000;
		endcase
endmodule


// Test bench to run your circuit

`timescale 1ns/1ps
module tb;

    // set up the inputs and outputs to the board
	reg [9:0] SW = 10'b00_0000_0000;                // 10 switches
	reg [3:0] KEY = 4'b1111;                        // 4 push buttons (active low)
	wire [9:0] LEDR;                                // 10 output LEDs
	wire [6:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;  // 6 seven-segment displays

    reg CLOCK = 0; // initialise clock to 0

    // wire up the board
    BOARD board(.SW(SW), .KEY(KEY), .CLOCK(CLOCK), .LEDR(LEDR), .HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2), .HEX3(HEX3), .HEX4(HEX4), .HEX5(HEX5));
    
	// simulate however you want the board to be interacted with here
	initial begin

		repeat (10) begin
			// example: let's press a button a few times
            KEY[0] = ~KEY[0];
			#8

            // outputs of the board state should look like this:
			$display("%b %b %b %b %b %b %b", HEX5, HEX4, HEX3, HEX2, HEX1, HEX0, LEDR);

            // example of a caption
			if (KEY[0] == 0) begin
				$display("@ key presssed");
			end 

		end
	end
endmodule 