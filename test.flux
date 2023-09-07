func init_population(pop_len){
    store i = 0;
    store population = [,];
    while(i<pop_len){
        store person = [,];
        store age = randint(0 80);
        store sex = randint(0 1);
        setAV(person 0 age);
        append(person sex);
        append(person 0);
        append(person 1);
        if(i = 0){
            setAV(population 0 person);
        }
        if(i NOE 0){
            append(population person);
        }
        store i = i + 1;
    }
    return population;
}

func cycle(pop_num pop_arr food){
    store arr_pop_len = pop_num - 1;
    store i = 0;
    while(i<arr_pop_len){
        store currperson = getAV(pop_arr i);
        store age = getAV(currperson 0) + 1;
        store sex = getAV(currperson 1);
        store able = getAV(currperson 2);
        store alive = getAV(currperson 3);
        store newperson = 0;

        if(alive NOE 0){
            if(age>8){
                if(age<80){
                    store food = food + 1;
                    store randborn = randint(0 100);
                    if(sex = 1){
                        if(randborn>60){
                            store randsex = randint(0 1);
                            store randperson = [,];
                            setAV(randperson 0 0);
                            append(randperson randsex);
                            append(randperson 0);
                            append(randperson 1);
                            append(pop_arr randperson);
                            store pop_num = pop_num + 1;
                        }
                    }
                }
                if(age GOE 80){
                    store able = 0;
                    store randeath = randint(0 100);
                    if(randeath>40){
                        store alive = 0;
                        store pop_num = pop_num - 1;
                    }
                }
            }
        }
        store new_person = [,];
        setAV(new_person 0 age);
        append(new_person sex);
        append(new_person able);
        append(new_person alive);

        setAV(pop_arr i new_person);
        store i = i + 1;
    }
    store return_array = [,];
    setAV(return_array 0 pop_num);
    append(return_array pop_arr);
    append(return_array food);
    return return_array;
}

func main(){
    store curryear = 0;
    store years = 10;
    store population = init_population(100);
    store pop_num = 100;
    store food = 100;

    print(pop_num);
    print(food);
    print(population);

    while(curryear<years){
        store res = cycle(pop_num population food);
        store pop_num = getAV(res 0);
        store pop_arr = getAV(res 1);
        store food = getAV(res 2);
        print(curryear);
        store curryear = curryear + 1;
    }
    print(pop_num);
    print(food);
    print(population);
    return 0;
}

main();