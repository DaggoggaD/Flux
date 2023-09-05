func abs(abs_x){
    if(abs_x GOE 0){
        return abs_x;
    }
    if(abs_x < 0){
        store res = 0-1;
        store res = res*abs_x;
        return res;
    }

}

func sqrt(sqrt_x){
    store delta = 0.001;
    store iteration_count = 0;
    store result = sqrt_x/2;

    store absval = result*result - sqrt_x;
    store absval = abs(absval);
    while(absval GOE delta){
        store result_sq = result*result;
        store result_sq = result_sq - sqrt_x;
        store result_sq = result_sq/2;
        store result = result - result_sq/result;

        store absval = result*result;
        store absval = absval - sqrt_x;
        store absval = abs(absval);
    }
    return result;
}

func pow(base power){
    store res = 1;
    store i = 0;
    if(power GOE 0){
        while(i<power){
            store res = res*base;
            store i = i + 1;
        }
    }
    if(power < 0){
        store normres = 1;
        while(i>power){
            store normres = normres*base;
            store i = i - 1;
        }
        store res = 1/normres;
    }
    return res;
}

func factorial(x){
    store i = 1;
    store res = 1;
    while(i LOE x){
        store res = res*i;
        store i = i + 1;
    }
    return res;
}

store arr = [1,2,3,4,5,];
store res = 2;
if(1>0){
    append(arr res);
    print(arr);
}