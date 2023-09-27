func spawnPerson(){
    class Person{
        store age = 0;
        store sex = 0;
        store able = FALSE;
        store alive = FALSE;
    }
    store set_age = randint(0 85);
    store set_sex = randint(0 1);
    if(set_age GOE 10){
        if(set_age LOE 80){
            store set_able = 1;
        }   
    }
    if(set_age < 10){
        store set_able = 0;   
    }
    if(set_age > 80){
        store set_able = 0;   
    }
    store set_alive = 1;
    store man = Instantiate(Person);
    setCV(man age set_age);
    setCV(man sex set_sex);
    setCV(man able set_able);
    setCV(man alive set_alive);
    return man;
}

func main(){
    class Person{
        store age = 0;
        store sex = 0;
        store able = FALSE;
        store alive = FALSE;
    }
    store population = [,];
    store starting_len = 10;
    store i = 0;
    store poplen = 10;
    store addedpop = 0;                                                                
    while(i<starting_len){
        store pers = spawnPerson();
        append(population pers);
        store i = i + 1;
    }
    store i = 0;
    while(i<poplen){
        store i = i + 1;
        store _infopers = getAV(population i);
        store _age = _infopers $ age;
        store _sex = _infopers $ sex;
        store _able = _infopers $ able;
        store _alive = _infopers $ alive;
        if(_alive = 1){
            if(_age GOE 10){
                if(_age LOE 45){
                    if(_sex = 1){
                        store randv = randint(0 10);
                        if(randv > 7){
                            store nman = spawnPerson();
                            append(population nman)
                            store addedpop = addedpop + 1;
                        }   
                    }
                }   
            }   
        }
        store poplen = poplen + addedpop;
    }
    store i = 0;
    while(i<poplen){
        store i = i + 1;
        store _infopers = getAV(population i);
        store _age = _infopers $ age;
        store _sex = _infopers $ sex;
        store _able = _infopers $ able;
        store _alive = _infopers $ alive;
        print(_age);
        print(_sex);
        print(_able);
        print(_alive);
        print("______");
    }
    
}

main();
