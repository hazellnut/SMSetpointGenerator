import time
from num_utils import *
from statistics import mean,median

from numerical_test import run_numerical_test
import random

def sim_test(V0,At,Dt,Xt,VtIn,Jm,plot=False,debug=False):

    epsilon = 1e-6
    times = []
    diag_params = []

    # for i in range(tests):
    AtIn = At
    DtIn = Dt
    desc_str = (f"Xt={Xt},Vt={VtIn},At={At},Dt={Dt},Jt={Jm},V0={V0}")
    print(desc_str)



    start_time = time.perf_counter()
    ta,td,Dx,Vt,At,Dt,case = run_numerical_test(V0,At,Dt,Xt,VtIn,Jm)

    end_time = time.perf_counter()
    diff =end_time - start_time
    print(f"time taken: {diff} seconds")
    times.append(diff)
    # assert(ta>0)
    # assert(td>0)

    Tj = abs(At/Jm)
    Tjd = abs(Dt/Jm)
    Tv = (Xt - Dx)/Vt

    # plot = False
    # debug = True
    if debug:
        #debug_distances(Tj,Tjd,ta,td,Tv,At,Dt,Vt,Jm,case,V0)


        X,V,A,J,T = generate_profile(Tj,Tjd,ta,td,Tv,At,Dt,Vt,Jm,case,V0,t_step = 0.002)
        print(X[-1])
        print(V[-1])
        try:
            assert(abs((X[-1]-Xt)) < 0.1)
            assert (ta + epsilon > 0)
            assert (td + epsilon > 0)
            assert (abs(Vt) <= abs(VtIn))
            assert (abs(At) <= abs(AtIn))
            assert (abs(Dt) <= abs(DtIn))
        except AssertionError:
            diags = [Xt,VtIn,At,Dt,Jm,V0]
            diag_params.append(diags)
            print(diags)
            print("Assert Error")
    if plot:
        plot_profile(X,V,A,J,T,desc_str)

    # print(mean(times))
    # print(median(times))


def sim_stress_test():
    V0_range = [i for i in range(-1000,1000,30)]
    At_range = [i for i in range(1,5000,100)]
    Dt_range = [i for i in range(1,5000,100)]
    Xt_range = [i for i in range(-5000,6000,110)]
    Vt_range = [i for i in range(-5000,5000,150)]
    Jm_range = [i for i in range(20,10000,500)]
    tests= 100
#Xt=170,Vt=-2300,At=4901,Dt=2401,Jt=8520,V0=470
    #Xt=2480,Vt=-950,At=1,Dt=1301,Jt=5020,V0=950
    Xt=2480
    VtIn=-950
    At=1
    Dt=1301
    Jm=5020
    V0=950

    # At = min(At,math.sqrt(Jm*abs(VtIn-V0)))
    # Dt = min(Dt, math.sqrt(Jm*abs(VtIn)))

    #gen_and_plot_only(V0,At,Dt,Xt,-850,Jm,3)
    # for i in range(tests):
    #     V0 = V0_range[random.randint(0,len(V0_range)-1)]
    #     At = At_range[random.randint(0,len(At_range)-1)]
    #     Dt = Dt_range[random.randint(0,len(Dt_range)-1)]
    #     Xt = Xt_range[random.randint(0,len(Xt_range)-1)]
    #     VtIn = Vt_range[random.randint(0,len(Vt_range)-1)]
    #     Jm = Jm_range[random.randint(0,len(Jm_range)-1)]
        

    sim_test(V0,At,Dt,Xt,VtIn,Jm,plot=False,debug=True)


def gen_and_plot_only(V0,At,Dt,Xt,Vt,Jm,case):
    Tj = At/Jm
    Tjd = Dt/Jm
    if case == 1:
        ta= -At/Jm - V0/At + Vt/At
        td= -Dt/Jm + Vt/Dt
        Dx = At*V0/(2*Jm) + At*Vt/(2*Jm) + Dt*Vt/(2*Jm) + Vt**2/(2*Dt) - V0**2/(2*At) + Vt**2/(2*At)
    elif case == 2:
        ta = -At/Jm + V0/At - Vt/At
        td = -Dt/Jm + Vt/Dt
        Dx = At*V0/(2*Jm) + At*Vt/(2*Jm) + Dt*Vt/(2*Jm) + Vt**2/(2*Dt) + V0**2/(2*At) - Vt**2/(2*At)
    elif case == 3:
        ta = -At/Jm + V0/At - Vt/At
        td = -Dt/Jm - Vt/Dt
        Dx = At*V0/(2*Jm) + At*Vt/(2*Jm) + Dt*Vt/(2*Jm) - Vt**2/(2*Dt) + V0**2/(2*At) - Vt**2/(2*At)
    elif case ==4: 
        ta = -At/Jm - V0/At + Vt/At
        td = -Dt/Jm - Vt/Dt
        Dx = At*V0/(2*Jm) + At*Vt/(2*Jm) + Dt*Vt/(2*Jm) - Vt**2/(2*Dt) - V0**2/(2*At) + Vt**2/(2*At)
    
    Tv = (Xt - Dx)/Vt
    X,V,A,J,T = generate_profile(Tj,Tjd,ta,td,Tv,At,Dt,Vt,Jm,case,V0,t_step = 0.002)
    plot_profile(X,V,A,J,T,"")


if __name__ == "__main__":
    sim_stress_test()