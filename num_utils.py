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


def generate_profile(Tj, Tjd, Ta, Td,Tv, At,Dt,Vt,Jm, move_case, V0,t_step = 0.002):
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
        s1 = 1,
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
    while t <= T7:
        if t < T1:
            Jc = s1*Jm
            Ac = s1*At*(t/(T2-T1))
            #Ac = s1*Jm*t_step
        elif t < T2:
            Jc = 0
            Ac = s1*At
        elif t < T3:
            Jc = -s1*Jm
            Ac = s1*At*((t-T2)/(T3-T2))
        elif t< T4:
            Jc = 0
            Ac =0
            Vc = Vt
            #Xc += Vc*t_step
            Dx += Vc*t_step
        elif t< T5:
            Jc = s2*Jm
            Ac += s2*Jm*t_step
        elif t < T6:
            Jc =0
            Ac = s2*Dt
        elif t <= T7:
            Jc = -s2*Jm
            Ac += Jc*t_step
        else:
            Jc = 0
            Ac = 0
            Vc = 0

        Vc += Ac*t_step + 0.5*Jc*t_step**2
        Xc += Vc*t_step + 0.5*Ac*t_step**2 + (1.0/6.0)*Jc*t_step**3

        
        X.append(Xc)
        V.append(Vc)
        A.append(Ac)
        J.append(Jc)
        t+= t_step
        T.append(t)
    print(f"Dx = {Dx}")
    return (X,V,A,J,T)

def plot_profile(X,V,A,J,T):
    sub = plt.subplot(4,1,1)
    sub.plot(T,X)

    sub = plt.subplot(4,1,2)
    sub.plot(T,V)

    sub = plt.subplot(4,1,3)
    sub.plot(T,A)

    sub = plt.subplot(4,1,4)
    sub.plot(T,J)

    plt.show()