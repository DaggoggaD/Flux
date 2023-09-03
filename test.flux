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
        print(result);
        print(absval);
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

store sqrt_res = sqrt(16);
print(sqrt_res);