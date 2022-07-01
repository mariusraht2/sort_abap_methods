# Sort ABAP methods by alphabet

1. Use python to start the program
2. Input the path to a text file containing the source code of the class

The program generates a new text file '<filename>_sorted.<extension>' which contains the sorted source code.
The original file is only being read and not being written in any case!

The method definitions are being sorted by visibility section and name. The method implementations are being sorted by name only.
For an example please see 'lcl_test.abap'.
