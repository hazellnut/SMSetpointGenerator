import time
from num_utils import *

from numerical_test import run_numerical_test

V0 =-100
At = 50
Dt = 200
Xt = -50
VtIn = -300
Jm = 100


start_time = time.perf_counter()
    
ta,td,Dx,Vt,At,Dt,case = run_numerical_test(V0,At,Dt,Xt,VtIn,Jm)

end_time = time.perf_counter()
diff =end_time - start_time
print(f"time taken: {diff} seconds")

assert(ta>0)
assert(td>0)


Tj = abs(At/Jm)
Tjd = abs(Dt/Jm)
Tv = (Xt - Dx)/Vt

X,V,A,J,T = generate_profile(Tj,Tjd,ta,td,Tv,At,Dt,Vt,Jm,case,V0)
print(X[-1])
print(V[-1])

plot_profile(X,V,A,J,T)