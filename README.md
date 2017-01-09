# dependency_graph
##How to run
python HeurDep.py [input file] [output directory]

e.g.
python HeurDep.py sample/P04-1023.math out/

##Format of the Input File (in sample/*)
[MATH_ID]\t[Presentation MathML]

PS: \t represent a tab.

##Format of the Output File (in out/*)
[Math-ID-parent]\t[Math-ID-child-0] [Math-ID-child-1]...

The complex formula (Math-ID-parent) contains several math symbols (identifiers, numbers, or operators) that are denoted by Math-ID-child-i and separated by a space.
