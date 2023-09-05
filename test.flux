store i = 0;
store population = [,];
while(i<100){
    store person = [,];
    store age = randint(0 80);
    store sex = randint(0 1);
    setAV(person 0 age);
    append(person sex);
    if(i = 0){
        setAV(population 0 person);
    }
    if(i NOE 0){
        append(population person);
    }
    store i = i + 1;
}
print(population);