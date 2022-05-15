# SUDOKU Helper Using MiniSAT Solver

<p align ="center">
<img src="https://thumbs.gfycat.com/MiserlyDisfiguredAgouti-size_restricted.gif"/> 
</p>


**Goal**: Fill in with digits the partially completed 9 × 9 grid so that each row, each column, and each of the nine 3 × 3 subgrids contains all the digits from 1 to 9.

```
puzzle=["5***1***4",
        "***2*6***",
        "**8*9*6**",
        "*4*****1*",
        "7*1*8*4*6",
        "*5*****3*",
        "**6*4*1**",
        "***5*2***",
        "2***6***8"]
 ```
where blank spaces are represented by a *

* Sudoku Problem is represented in terms of Formula F in 3-CNF (a collection of clauses each having at most three literals).
* An easy way to solve such a combinatorial problem is to reduce problem to SAT and use SAT-Solver (MiniSAT here) which can solve instances with thousands of variables.
* In this problem there will be there will be 9 × 9 × 9 = 729 Booleanvariables: for 1 ≤ i , j , k ≤ 9, xijk = 1, if and only if the cell [i,j] contains the digit k.
* Following Constraints have been used to create the list of clauses which are then converted to CNF (Conjunctive Normal Form) and fed to MiniSAT Solver.
  * Cell [i,j] contains exactly one digit: ExactlyOneOf(xij1, xij2, . . . , xij9) 
  * k appears exactly once in row i: ExactlyOneOf(xi1k, xi2k, . . . , xi9k)
  * k appears exactly once in column j : ExactlyOneOf(x1jk, x2jk, . . . , x9jk)
  * k appears exactly once in a 3 × 3 block: ExactlyOneOf(x11k, x12k, . . . , x33k)
  * [i,j] already contains k : (xijk)
* State-of-the-art SAT-solvers find a satisfying assignment for the resulting formula in blink of an eye, though the corresponding search space has size about 2^729 ≈ 10^220
