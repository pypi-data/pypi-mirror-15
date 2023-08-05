# include <math.h>

#ifdef _MSC_VER
#if _MSC_VER < 1800
double log1p(double x){
    if(fabs(x) > 1e-4){
        return log(1.0 + x);
    }
    return (-0.5 * x + 1.0) * x;
}
#endif
#endif
