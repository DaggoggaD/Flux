class ClassName{
    store value = 3;
    store value_two = 4;
}


store ClassOBJ = Instantiate(ClassName);
store value = ClassOBJ $ value;
store value_two = ClassOBJ $ value_two;
print(value);
print(value_two);


setCV(ClassOBJ value 12);
store value = ClassOBJ $ value;
store value_two = ClassOBJ $ value_two;
print(value);
print(value_two);

setCV(ClassOBJ value_two 12);
store value = ClassOBJ $ value;
store value_two = ClassOBJ $ value_two;
print(value);
print(value_two);