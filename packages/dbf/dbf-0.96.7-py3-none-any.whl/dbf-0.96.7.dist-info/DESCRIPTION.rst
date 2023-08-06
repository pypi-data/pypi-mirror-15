
Currently supports dBase III, Clipper, FoxPro, and Visual FoxPro tables. Text is returned as unicode, and codepage settings in tables are honored. Memos and Null fields are supported.  Documentation needs work, but author is very responsive to e-mails.

Not supported: index files (but can create tempory non-file indexes), auto-incrementing fields, and Varchar fields.

Installation:  `pip install dbf`

There may be messages about byte-compiling failures -- you can safely ignore them (this is a multi-version release, and 2 and 3 don't like some of each other's code).


