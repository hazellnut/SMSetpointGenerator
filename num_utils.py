import math
from matplotlib import pyplot as plt
DEBUG = False

def case_2_velo(At,Dt,V0,Jm,Xt,VtIn):
    if At == Dt:
        Vtrestrict = -V0/2 + Jm*Xt/At - Jm*V0**2/(2*At**2)
    else:
        sqrt_term = Dt*(At**4*Dt + 2*At**3*Dt**2 - 4*At**3*Jm*V0 + At**2*Dt**3 + 4*At**2*Dt*Jm*V0 + 8*At**2*Jm**2*Xt - 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)
        if  sqrt_term< 0:
            if DEBUG:
                print("incorrect Vt calc")
            raise ValueError
        else:
            #Vt > 0
            Vtrestrict = (-At*Dt*(At + Dt) + math.sqrt(sqrt_term))/(2*Jm*(At - Dt))
    return Vtrestrict


def case_1_velo(At,Dt,V0,Jm,Xt,VtIn):
    if At == Dt:
        sqrt_term = (At**4 - 2*At**2*Jm*V0 + 4*At*Jm**2*Xt + 2*Jm**2*V0**2)
        if  sqrt_term< 0:
            if DEBUG:
                print("incorrect Vt calc")
            raise ValueError
        else:
            #the correct soln should be +ve, otherwise we go into negative time
            Vtrestrict = (-At**2 + math.sqrt(sqrt_term))/(2*Jm)
    else:
        sqrt_term = Dt*(At + Dt)*(At**3*Dt + At**2*Dt**2 - 4*At**2*Jm*V0 + 8*At*Jm**2*Xt + 4*Jm**2*V0**2)
        if sqrt_term < 0:
            if DEBUG:
                print("incorrect Vt calc")
            raise ValueError
        else:
            Vtrestrict = (-At*Dt*(At + Dt) + math.sqrt(sqrt_term))/(2*Jm*(At + Dt))

    return Vtrestrict


def case_3_velo(At,Dt,V0,Jm,Xt,VtIn):
    if At == Dt:
        sqrt_term = At**4 + 2*At**2*Jm*V0 - 4*At*Jm**2*Xt + 2*Jm**2*V0**2
        if  sqrt_term< 0:
            if DEBUG:
                print("incorrect Vt calc")
            raise ValueError
        else:
            Vtrestrict = (At**2 -math.sqrt(sqrt_term)/2)/(2*Jm)
    else:
        sqrt_term = Dt*(At + Dt)*(At**3*Dt + At**2*Dt**2 + 4*At**2*Jm*V0 - 8*At*Jm**2*Xt + 4*Jm**2*V0**2)
        if  sqrt_term< 0:
            if DEBUG:
                print("incorrect Vt calc")
            raise ValueError
        else:
            Vtrestrict = (At*Dt*(At + Dt) - math.sqrt(sqrt_term))/(2*Jm*(At + Dt))
            # print(Vtrestrict)
    return Vtrestrict


def case_4_velo(At,Dt,V0,Jm,Xt,VtIn):
    if At == Dt:
        Vtrestrict = -V0/2 + Jm*Xt/At + Jm*V0**2/(2*At**2)
    else:
        sqrt_term = Dt*(At**4*Dt + 2*At**3*Dt**2 + 4*At**3*Jm*V0 + At**2*Dt**3 - 4*At**2*Dt*Jm*V0 - 8*At**2*Jm**2*Xt + 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)
        if  sqrt_term< 0:
            if DEBUG:
                print("incorrect Vt calc")
            raise ValueError
        else:
            Vtrestrict = (At*Dt*(At + Dt) - math.sqrt(sqrt_term))/(2*Jm*(At - Dt))
            # print(Vtrestrict)
    return Vtrestrict

def case_1_dx():
    pass

def case_2_dx():
    pass
def case_3_dx():
    pass

def case_4_dx():
    pass


def generate_profile(Tj, Tjd, Ta, Td,Tv, At,Dt,Vt,Jm, move_case, V0,t_step = 0.0001):
    Xc = 0
    Vc = V0
    Ac =0
    X = []
    V = []
    A = []
    J = []
    T = []
    
    if move_case == 1:
        s1 = 1
        s2 = -1
    elif move_case ==2:
        s1 = -1
        s2 = -1
    elif move_case ==3:
        s1 = -1
        s2 = 1
    elif move_case == 4:
        s1 = 1
        s2 = 1

    Jc =0
    t=t_step

    T1 = Tj
    T2 = T1 + Ta
    T3 = T2 + Tj
    T4 = T3 + Tv
    T5 = T4 + Tjd
    T6 = T5 + Td
    T7 = T6 + Tjd
    Dx = 0
    Dx1 =0
    Dx2 =0
    Dx3=0
    Dx4=0
    Dx5 =0
    Dx6=0
    Dx7=0
    Ac_old = 0
    Vc_old = 0
    while t <= T7 + 0.5:
        if t < T1:
            Jc = s1*Jm
            Ac = s1*At*(t/(T1))
            #Ac = s1*Jm*t_step
        elif t < T2:
            Jc = (s1*At-Ac_old)/t_step
            Ac = s1*At
        elif t < T3:
            Jc = -s1*Jm
            Ac = s1*At*((T3-t)/(T3-T2))
        elif t< T4:
            Jc = (-Ac_old)/t_step
            Ac =0
            Vc = Vt
            #Xc += Vc*t_step
            #Dx2 += Vc*t_step
        elif t< T5:
            Jc = s2*Jm
            Ac = s2*Dt*(t-T4)/(T5-T4)
        elif t < T6:
            Jc = (s2*Dt-Ac_old)/t_step
            Ac = s2*Dt
        elif t < T7:
            Jc = -s2*Jm
            Ac = s2*Dt*((T7-t)/(T7-T6))
        else:
            Jc = (-Ac_old)/t_step
            Ac = 0
            Vc = 0

        Vc += Ac_old*t_step + 0.5*Jc*t_step**2
        dx = Vc_old*t_step + 0.5*Ac_old*t_step**2 + (1.0/6.0)*Jc*t_step**3
        Xc += dx

        if t > T1:
            Dx1 += dx
        elif t<T2:
            Dx2 += dx
        elif t<T3:
            Dx3 += dx
        elif t < T4:
            Dx4 +=dx
        elif t<T5:
            Dx5+=Dx
        elif t<T6:
            Dx6+=Dx
        elif t<T7:
            Dx7+=Dx

        
        
        Ac_old = Ac
        Vc_old = Vc
        
        X.append(Xc)
        V.append(Vc)
        A.append(Ac)
        J.append(Jc)
        t+= t_step
        T.append(t)
    print(f"Dx1, Dx2 : {Dx1}, {Dx2}")
    return (X,V,A,J,T)

def plot_profile(X,V,A,J,T, desc_string="test"):
    f = plt.figure(figsize=(10,8))
    f.suptitle(desc_string)
    #f.set_tight_layout('h_pad')

    sub = plt.subplot(4,1,1)
    sub.plot(T,X)
    sub.set_title("X")
    sub.set_ylabel("Position (mm)")
    sub.set_xlabel("Time (s)")

    f.add_axes(sub)

    sub = plt.subplot(4,1,2)
    sub.plot(T,V)
    sub.set_title("V")
    sub.set_ylabel("Velocity (mm/s)")
    sub.set_xlabel("Time (s)")


    f.add_axes(sub)
    sub = plt.subplot(4,1,3)
    sub.plot(T,A)
    sub.set_title("A")
    sub.set_ylabel("Acceleration (mm/s/s)")
    sub.set_xlabel("Time (s)")

    f.add_axes(sub)
    sub = plt.subplot(4,1,4)
    sub.plot(T,J)
    sub.set_title("J")
    sub.set_ylabel("Jerk (mm/s/s/s)")
    sub.set_xlabel("Time (s)")

    f.add_axes(sub)
    f.subplots_adjust(wspace=1,hspace=1)

    plt.show()