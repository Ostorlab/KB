Application should provide as little explanatory information as possible with the compiled code. Metadata such as
debugging information, line numbers, and descriptive function or method names makes the binary or byte-code
easier to reverse engineer.
  
These symbols can be saved in "Stabs" format, the DWARF format or in .symbols r .symbolsmap files. It is noteworthy
that most crash reporting tool support uploading symbols to perform stack trace symblication and don't require
symbols to be present in the application. 
