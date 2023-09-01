import time
from num_utils import *

from numerical_test import run_numerical_test
import random


V0_range = [-1000,-200,-10,0,10,200,1000]
At_range = [1,5,20,50,100,500,2000]
Dt_range = [1,5,20,50,100,500,2000]
Xt_range = [-5000,-100,-1,1,100,5000]
Vt_range = [-5000,-100,100,5000]
Jm_range = [1,5,100,2000]

V0 = V0_range[random.randint(0,6)]
At = At_range[random.randint(0,6)]
Dt = Dt_range[random.randint(0,6)]
Xt = Xt_range[random.randint(0,5)]
VtIn = Vt_range[random.randint(0,3)]
Jm = Jm_range[random.randint(0,3)]


Xt=-1
VtIn=-100
At=2000
Dt=500
Jm=100
V0=10

# V0 =-100
# At = 50
# Dt = 200
# Xt = 5000
# VtIn = -300
# Jm = 1000
desc_str = (f"Xt={Xt},Vt={VtIn},At={At},Dt={Dt},Jt={Jm},V0={V0}")
print(desc_str)



start_time = time.perf_counter()



ta,td,Dx,Vt,At,Dt,case = run_numerical_test(V0,At,Dt,Xt,VtIn,Jm)

end_time = time.perf_counter()
diff =end_time - start_time
print(f"time taken: {diff} seconds")

# assert(ta>0)
# assert(td>0)


Tj = abs(At/Jm)
Tjd = abs(Dt/Jm)
Tv = (Xt - Dx)/Vt

X,V,A,J,T = generate_profile(Tj,Tjd,ta,td,Tv,At,Dt,Vt,Jm,case,V0,t_step = 0.002)
print(X[-1])
print(V[-1])

plot_profile(X,V,A,J,T,desc_str)