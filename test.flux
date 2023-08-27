func sqrt(x){
    store res = "NONE";
	if(x=0){
		store res = x;
	}
	if(x=1){
		store res = x;
	}
	if(x NOE 0){
		if(x NOE 1){
			store start = 0;
			store end = x*1;
			store ans = 0;
			while(start LOE end){
				store mid = start + end;
				store mid = mid/2;
				if(mid*mid =x){
					store res = mid;
					store start = end + 1;
				}
				if(mid*mid < x){
					store start = mid + 1;
					store ans = mid*1;
				}
				if(mid*mid > x){
					store end = mid - 1;
				}

			}
			if(res NOE "NONE"){
			    if(ans NOE 0){
                    print(res);
                    store res = ans;
                }
			}
		}
	}
	return res;
}
store res = sqrt(5);
print(res);