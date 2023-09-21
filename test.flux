class ClassName{
    store value = 3;
    store value_two = 4;
}

Instantiate(ClassName);
store ClassOBJ = Instantiate(ClassName);
store value = ClassOBJ $ value;
store value_two = ClassOBJ $ value_two;
print(value);
print(value_two);