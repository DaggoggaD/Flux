class Person{
    store age = 0;
    store sex = 0;
    store able = FALSE;
    store alive = FALSE;
}

store man = Instantiate(Person);
setCV(man age 18);
setCV(man sex 0);
setCV(man able TRUE);
setCV(man alive TRUE);
store age = man $ age;
store sex = man $ sex;
store able = man $ able;
store alive = man $ alive;
print(age);
print(sex);
print(able);
print(alive);