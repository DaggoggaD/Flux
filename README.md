# Flux v0.1
Interpreted (tree-walking) programming language Flux written in Python.
## Current state of progress
#### Early submission of flux. 

### Implemented features (grammar rules described later):
* Binary operations
* Variables (int, string, float, lists)
* Print statement
* While
* If
* Array set value
* Array get value

### WIP/planned features:

* Booleans
* Else
* Functions
* User input
* Errors
* Type conversion (int -> float, int -> string ... )
* Switch
* Break, Next, Try, Catch
* Classes
* Import
* Python modules accessibility (?)

## Issues
_parser.py and even more so _lexer.py are overcomplicated, junky and bad coded. _interpreter.py (and the small shell.py) is decently written, but the other 2 needs to be completely re-written. This will be done only after the key features are implemented (the first 8 in the WIP section).
_lexer.py can be splitted in multiple functions, as it should've been done since the beginning (i wasnt used to do so 2 years ago). _parser.py is better in this area, but some "alghoritms" used are poorly thought and written.
At the moment errors are poorly controlled and have no in-line info. A new system must be created handling errors in a more abstract manner.

## Language grammar
* binary operations:
  * Math operations: `+ - * /` are already implemented.
  * Power operation will be created inside the flux language as a function (`pow(VALUE POWER)`).
  * Sqrt operation will be implemented with `#` keyword.
  * `> < >= <= ==` becomes `> < GOE LOE =`.
* variables:
  * Variable declaration: variables are dinamically allocated, so they have no defined type and can change later. To declare one you use the "store" keyword: `store NAME = VALUE;`.
    To declare a variable you NEED to assign a value (None value will be added later) followed by a ";".
  * Variable value change: to change the value of a variable you still need to use the "store" keyword. This will NOT cause interferences with global/local variables.
    ```
    store NAME = "andrea";
    ...
    store NAME = "nautilus";
    ```
  * Array values: to create an array you initialize the variable, and than assign it an array: `store ARRAY = [VALUE, VALUE, VALUES...,] ;`. At the moment, due to a bug you need to end the line with a space and a comma, not only a comma `;` -> ` ;`. At the last index of the array, you must add a `,` like so: `store ARRAY = [1,[1.1,1.2,1.3,],2,3,] ;`.
      * Array get value: `getAV(NAME INDEX);`. **CAN be nested**
      * Array set value: `setAV(NAME INDEX VALUE);` **CAN'T BE NESTED**
  * `+= -= *= /= %=` are not supported and you'll need to use a "recursive" formula:
    ```
    store i = 0;
    store i = i + 1;
    ```
* print:
  * To print values to the user you use the "print" keyword: `print(VALUE);`.
  * You can print integers, floats, strings and arrays by passing it's value or identifier: `print(1);` or `print(2.2);` or `print(VALUE);` or `print(variable_name);`
* while:
  * #### For loops won't be implemented to keep the language simpler.
  * While loops are similar to it's C++ counterpart: `while(CONDITION){...}`
* if:
  * Again, if statements are similar to C++ grammar: `if(CONDITION){...}`

 # Other infos
All grammar infos will be updated as feature gets added or changed. The language is expected to be finished earlier than september 2024, as it will be used as a lyceum essay.
