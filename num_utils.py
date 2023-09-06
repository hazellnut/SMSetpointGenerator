import math
from matplotlib import pyplot as plt
DEBUG = False

EPSILON = 1e-4

def case_2_velo(At,Dt,V0,Jm,Xt,VtIn,recurse=0):
    if recurse > 5:
        raise ValueError
    
    if VtIn > (V0 - At**2/Jm):
        At = math.sqrt(Jm*abs(VtIn-V0))


    if VtIn < Dt**2/Jm:
        Dt = math.sqrt(Jm*abs(VtIn))

    Vtrestrict = VtIn
    if At == Dt:
        Vtrestrict = -V0/2 + Jm*Xt/At - Jm*V0**2/(2*At**2)
    else:
        sqrt_term = Dt*(At**4*Dt + 2*At**3*Dt**2 - 4*At**3*Jm*V0 + At**2*Dt**3 + 4*At**2*Dt*Jm*V0 + 8*At**2*Jm**2*Xt - 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)
        if  sqrt_term< 0:
            D1 = solve_cubic(At**2,2*(At**3),At**4 + 4*At**2*Jm*V0 - 8*At*Jm**2*Xt + 4*Jm**2*V0**2,-4*At**3*Jm*V0+8*At**2*Jm**2*Xt-4*At*Jm**2*V0**2)
            if DEBUG:
                print("incorrect Vt calc")
            if D1 < 0:
                raise ValueError
            else:
                sqrt_term = D1*(At**4*D1 + 2*At**3*D1**2 - 4*At**3*Jm*V0 + At**2*D1**3 + 4*At**2*D1*Jm*V0 + 8*At**2*Jm**2*Xt - 8*At*D1*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*D1*Jm**2*V0**2)

        else:
            #Vt > 0
            Vtrestrict = (-At*Dt*(At + Dt) + math.sqrt(sqrt_term))/(2*Jm*(At - Dt))
    Vt = min(Vtrestrict,VtIn)
    if Vt > (V0 - At**2/Jm) + EPSILON or Vt < Dt**2/Jm - EPSILON:
        if Vt > (V0 - At**2/Jm) + EPSILON:
            At = math.sqrt(Jm*abs(Vt-V0))
        if Vt < Dt**2/Jm - EPSILON:
            Dt = math.sqrt(Jm*abs(Vt))
        Vt,At,Dt = case_2_velo(At,Dt,V0,Jm,Xt,Vt,recurse+1)

    if DEBUG:
        print(recurse) 
    return Vt,At,Dt


def case_1_velo(At,Dt,V0,Jm,Xt,VtIn,recurse=0):
    if recurse > 5:
        raise ValueError
    
    if VtIn < (V0 + At**2/Jm):
        At = math.sqrt(Jm*abs(VtIn-V0))
    if VtIn < Dt**2/Jm:
        Dt = math.sqrt(Jm*abs(VtIn))

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
            D1,D2 = solve_poly_inequality(At**2,At**3, 8*At*Jm**2*Xt- 4*At**2*Jm*V0 + 4*Jm**2*V0**2)
            if DEBUG:
                print("incorrect Vt calc")
            if D1 < 0:
                raise ValueError
            Dt = D1
        Vtrestrict = (-At*Dt*(At + Dt) + math.sqrt(sqrt_term))/(2*Jm*(At + Dt))
    Vt = min(Vtrestrict,VtIn)
    if Vt < V0:
        raise V0Error(Vt,At,Dt)
    if Vt < (V0 + At**2/Jm) - EPSILON or Vt < Dt**2/Jm - EPSILON:
        if Vt < (V0 + At**2/Jm):
            At = math.sqrt(Jm*abs(Vt-V0))
        if Vt < Dt**2/Jm:
            Dt = math.sqrt(Jm*abs(Vt))
    
        Vt,At,Dt = case_1_velo(At,Dt,V0,Jm,Xt,Vt,recurse+1)

    if DEBUG:
        print(recurse)
    return Vt,At,Dt


def case_3_velo(At,Dt,V0,Jm,Xt,VtIn,recurse=0):
    if recurse > 5:
        raise ValueError
    # if Xt > 0 and V0 < 0:
    #     raise ValueError
    
    if VtIn > (V0 - At**2/Jm):
        At = min(math.sqrt(Jm*abs(VtIn-V0)),At)

    if VtIn > -Dt**2/Jm:
        Dt = min(math.sqrt(Jm*abs(VtIn)),Dt)

    #inequality test
    # DtTest = (-At**2 - math.sqrt(At**4 - 16*At**2*Jm*V0 + 32*At*Jm**2*Xt - 16*Jm**2*V0**2))/(2*At)
    # DtTest2 = (-At**2 + math.sqrt(At**4 - 16*At**2*Jm*V0 + 32*At*Jm**2*Xt - 16*Jm**2*V0**2))/(2*At)

    

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
        #we could adjust Dt ST we have a solution here
        
        if  sqrt_term< 0:
            D1,D2 = solve_poly_inequality(At**2,(At**3),4*At**2*Jm*V0 - 8*At*Jm**2*Xt + 4*Jm**2*V0**2)
            
            if DEBUG:
                print("incorrect Vt calc")
            if D1 < 0:
                AccelVal = min(At,Dt)
                Vtrestrict,At,Dt = case_3_velo(AccelVal,AccelVal,V0,Jm,Xt,VtIn,recurse+1)
                if Vt <= (V0 - At**2/Jm) and Vt <= -Dt**2/Jm:
                    return Vtrestrict, At,Dt
                raise ValueError
            else:
                sqrt_term = D1*(At + D1)*(At**3*D1 + At**2*D1**2 + 4*At**2*Jm*V0 - 8*At*Jm**2*Xt + 4*Jm**2*V0**2)
        
        Vtrestrict = (At*Dt*(At + Dt) - math.sqrt(sqrt_term))/(2*Jm*(At + Dt))
            # print(Vtrestrict)
    if Vtrestrict >0:
        At = Dt
    if Vtrestrict < VtIn and not VtIn > 0:
        Vt = VtIn
    else:
        Vt = Vtrestrict

    if Vt > V0:
        raise V0Error(Vt,At,Dt)
    

    if Vt > (V0 - At**2/Jm) + EPSILON or Vt > -Dt**2/Jm + EPSILON:  #little floating point artefacts fucking it up and causing recursion issues
        if Vt > (V0 - At**2/Jm):
            At = math.sqrt(Jm*abs(Vt-V0))

        if Vt > -Dt**2/Jm:
            Dt = math.sqrt(Jm*abs(Vt))

        Vt,At,Dt = case_3_velo(At,Dt,V0,Jm,Xt,Vt,recurse=recurse+1)

    if DEBUG:
        print(recurse)
    return Vt,At,Dt


def case_4_velo(At,Dt,V0,Jm,Xt,VtIn,recurse=0):
    if recurse> 5:
        raise ValueError
    
    if VtIn < (V0 + At**2/Jm):
        At = math.sqrt(Jm*abs(VtIn-V0))

    if VtIn > -Dt**2/Jm:
        Dt = math.sqrt(Jm*abs(VtIn))

    if abs(At-  Dt) < EPSILON:
        Vtrestrict = -V0/2 + Jm*Xt/At + Jm*V0**2/(2*At**2)
    else:
        sqrt_term = Dt*(At**4*Dt + 2*At**3*Dt**2 + 4*At**3*Jm*V0 + At**2*Dt**3 - 4*At**2*Dt*Jm*V0 - 8*At**2*Jm**2*Xt + 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)
        if  sqrt_term< 0:

            D1 = solve_cubic(At**2,2*(At**3),At**4 + 4*At**2*Jm*V0 + 8*At*Jm**2*Xt + 4*Jm**2*V0**2,4*At**3*Jm*V0-8*At**2*Jm**2*Xt+4*At*Jm**2*V0**2)
            if DEBUG:
                print("incorrect Vt calc")
            if D1 < 0: #at this point this implies we cannot find a Dt to work with At within the constraints- does NOT necessarily mean params don't exist
                #raise ValueError
                AccelVal = min(At,Dt)
                Vtrestrict,At,Dt = case_4_velo(AccelVal,AccelVal,V0,Jm,Xt,VtIn,recurse+1)
                if Vtrestrict >= (V0 + At**2/Jm) and Vtrestrict <= -Dt**2/Jm:
                    return Vtrestrict,At,Dt
                raise ValueError
            Dt = D1
            sqrt_term = Dt*(At**4*Dt + 2*At**3*Dt**2 + 4*At**3*Jm*V0 + At**2*Dt**3 - 4*At**2*Dt*Jm*V0 - 8*At**2*Jm**2*Xt + 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)
        
        Vtrestrict = (At*Dt*(At + Dt) - math.sqrt(sqrt_term))/(2*Jm*(At - Dt))
            # print(Vtrestrict)
    Vt = max(VtIn,Vtrestrict)
    if Vt > 0:
        raise ValueError
    if Vt < (V0 + At**2/Jm)- EPSILON or Vt > -Dt**2/Jm + EPSILON:
        if Vt < (V0 + At**2/Jm):
            At = math.sqrt(Jm*abs(Vt-V0))

        if Vt > -Dt**2/Jm:
            Dt = math.sqrt(Jm*abs(Vt))
            
        Vt,At,Dt = case_4_velo(At,Dt,V0,Jm,Xt,Vt,recurse+1)
    
    if DEBUG:
        print(recurse)
    return Vt,At,Dt


def check_valid_velocity(Vt,At,Dt,Jm,V0,Xt):
    sqrt_term1 = Dt*(At + Dt)*(At**3*Dt + At**2*Dt**2 - 4*At**2*Jm*V0 + 8*At*Jm**2*Xt + 4*Jm**2*V0**2)

    sqrt_term4 = Dt*(At**4*Dt + 2*At**3*Dt**2 + 4*At**3*Jm*V0 + At**2*Dt**3 - 4*At**2*Dt*Jm*V0 - 8*At**2*Jm**2*Xt + 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)

    sqrt_term3 = Dt*(At + Dt)*(At**3*Dt + At**2*Dt**2 + 4*At**2*Jm*V0 - 8*At*Jm**2*Xt + 4*Jm**2*V0**2)



    sqrt_term2 = Dt*(At**4*Dt + 2*At**3*Dt**2 - 4*At**3*Jm*V0 + At**2*Dt**3 + 4*At**2*Dt*Jm*V0 + 8*At**2*Jm**2*Xt - 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)

    if sqrt_term1 > 0:
        return 1
    if sqrt_term2 > 0:
        return 2
    if sqrt_term3 > 0:
        return 3
    if sqrt_term4 > 0:
        return 4
    

def solve_poly_inequality(a,b,c,gt=True): #gt implies >0, False <0
    test_term = (b**2 - 4*a*c)
    if test_term < 0:
        D1 = -b/(2*a)
        D2 = 0
             #invalid calculation i.e. there exists no Dt for this At s.t. we get a valid velocity
    else:
        D1 = (-b + math.sqrt(test_term))/(2*a)
        D2 = (-b - math.sqrt(test_term))/(2*a)
    return [D1,D2]

def solve_cubic(a,b,c,d):
    
    t1 = (-b**3)/(27*(a**3)) +  b*c/(6*a**2) - d/(2*a)
    t2 = c/(3*a) - b**2/(9*a**2)
    test_term = t1**2 +t2**3
    if test_term < 0:
        return -1
    D1 = (t1 + math.sqrt(test_term))**(1/3) + (t1 - math.sqrt(test_term))**(1/3) - b/(3*a)
    D1 = abs(D1)
    return D1

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
    Vc_old = V0
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

        if t < T1:
            Dx1 += dx
        elif t<T2:
            Dx2 += dx
        elif t<T3:
            Dx3 += dx
        elif t < T4:
            Dx4 +=dx
        elif t<T5:
            Dx5+=dx
        elif t<T6:
            Dx6+=dx
        elif t<T7:
            Dx7+=dx

        
        
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


def debug_distances(Tj,Tjd,ta,td,Tv,At,Dt,Vt,Jm,move_case,V0):

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


    V1 = V0 + s1*Jm*Tj**2/2
    V2 = V1  +s1*At*ta
    V3 = V2 + s1*At*Tj - s1*Jm*Tj**2/2

    V4 = Vt + s2*Jm*Tjd**2/2
    V5 = V4 + s2*Dt*td
    V6 = V5 + s2*Dt*Tjd - s2*Jm*Tjd**2/2

    X1 = V0*Tj +s1* Jm*Tj**3/6
    X2 = V1*ta +s1*At*ta**2/2
    X3 =  V2*Tj +s1* At*Tj**2/2 -s1* Jm*Tj**3/6
    X4 = Vt*Tjd + s2*Jm*Tjd**3/6
    X5 =V4*td + s2*Dt*td**2/2
    X6 = V5*Tjd + s2*Dt*Tjd**2/2 - s2*Jm*Tjd**3/6

    print(f"X1:{X1}\nX2:{X2}\nX3:{X3}\nX4:{X4}\nX5:{X5}\nX6:{X6}")

class V0Error(Exception):
    def __init__(self,Vt=0,At=0,Dt=0):
        self.Vt= Vt
        self.At = At
        self.Dt = Dt