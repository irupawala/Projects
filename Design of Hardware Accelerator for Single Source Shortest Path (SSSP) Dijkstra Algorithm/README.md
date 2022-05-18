<h1 align="center">
Design of hardware accelerator for single source shortest path (SSSP) Dijkstra Algorithm
</h1>

<p align ="center">
<img src="https://i.pinimg.com/originals/cf/a6/e0/cfa6e0006734b0bd93431c754a8c42c4.gif"> 
</p>

* Designed a hardware accelerator using Synopsys Model Compiler for Dijkstra Algorithm used widely in the applications like segmentation of pixels, routing packets in network protocol and path planning of robots. 
* Optimized the design using architectural optimizations techniques like parallelism. A graph with 52 vertices can be fed into the circuit simultaneously and the outputs can be obtained almost at the same time. With the architectural optimizations applied the hardware accelerator was found to be almost 50 times faster than the software counterpart. 
* Mapped the design into Xilinx Virtex 7 XC7VX485T‐ 2FFG1761 FPGA and 28nm ASIC target and extracted area, power and timing reports.



**Languages:** C, MATLAB

**Tools Used:** Simulink, Synopsys Synplify Pro, Synopsys Design Compiler, Synopsys VCS, Synopsys Model Compiler, Synopsys High-Level Synthesis Token
