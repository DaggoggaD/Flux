# Flux v0.3
Interpreted (tree-walking) programming language Flux written in Python.

* **New features: remAV, import, round.**

## Current state of progress
#### Early submission of flux. 

### Implemented features (grammar rules described later):
* Binary operations
* Variables (int, string, float, lists, booleans)
* Print statement
* While
* If
* Array set value
* Array get value
* Functions
* Append array
* Random values (int, float)
* Array remove value
* Import
* Round
* Math functions (root, log, pow)

### WIP/planned features:

* Type conversion (int -> float, int -> string ... )
* User input
* Else
* Errors
* Switch
* Break, Next, Try, Catch
* Classes
* Python modules accessibility (?)

## Issues
At the moment errors are poorly controlled and have no in-line info. A new system must be created handling errors more abstractly.

## Language grammar
* binary operations:
  * Math operations: `+ - * /` are already implemented.
  * Power operation will be created inside the flux language as a function (`pow(VALUE POWER)`).
  * Sqrt operation will be implemented with the `#` keyword.
  * `> < >= <= ==` becomes `> < GOE LOE =`.
* variables:
  * Variable declaration: Variables are dynamically allocated, so they have no defined type and can change later. To declare one, use the "store" keyword: `store NAME = VALUE;`.
    To declare a variable you NEED to assign a value (None value will be added later) followed by a ";".
  * Variable value change: To change the value of a variable you still need to use the "store" keyword. This will NOT cause interferences with global/local variables.
    ```
    store NAME = "andrea";
    ...
    store NAME = "nautilus";
    ```
  * Array values: to create an array you initialize the variable, and then assign it an array: `store ARRAY = [VALUE, VALUE, VALUES...,];`. At the last index of the array, you must add a `,` like so: `store ARRAY = [1,[1.1,1.2,1.3,],2,3,];`.
      * Array get value: `getAV(NAME INDEX);`. **CAN be nested**
      * Array set value: `setAV(NAME INDEX VALUE);` **CAN'T BE NESTED**
      * Array append value: `append(NAME VALUE):` **CAN'T BE NESTED**
      * Array remove value: `remAV(NAME INDEX);` **CAN'T BE NESTED**
  * `+= -= *= /= %=` are not supported and you'll need to use a "recursive" formula:
    ```
    store i = 0;
    store i = i + 1;
    ```
* print:
  * To print values to the user, use the "print" keyword: `print(VALUE);`.
  * You can print integers, floats, strings and arrays by passing their value or identifier: `print(1);` or `print(2.2);` or `print(VALUE);` or `print(variable_name);`
* while:
  * #### For loops won't be implemented to keep the language simpler.
  * While loops are similar to it's C++ counterpart: `while(CONDITION){...}`
* if:
  * Again, if statements are similar to C++ grammar: `if(CONDITION){...}`
* functions:
  * function declaration are structured as follows: ```func NAME(ARG ARG ...){EXPRESSIONS}```.
  * functions are completely separated parts of code, so they cannot see public variables outside of the ARGS passed. To pass variables you must use ARGS.
  * function calls can return a value into a variable or not dynamically:
    ```
    func sum(a b){
        store sum = a + b;
        return sum;
    }
    store res = sum(1 2);
    sum(1 2);
    ```
    Where the second sum doesn't show in the console
* random values:
  * random float: `random();` -> returns float between 0 and 1.
  * random int: `randint(START END);` -> returns int between START and END.
* import:
  * import a file: `import FILENAME;` with all variables and functions.
* round:
  * round value: `round(VALUE);` -> FLOAT -> INT; INT->INT.
* math functions:
  * power: `Mpow(BASE POWER);`
  * root: `Mroot(EXPONENT VALUE);`
  * log: `Mlog(BASE VALUE);`
 # Other Infos
All grammar info will be updated as features gets added or changed. The language is expected to be finished earlier than September 2024, as it will be used as a lyceum essay.
