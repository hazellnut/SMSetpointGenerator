import math

def calc_case_2(At,Dt,V0,Jm,Xt,VtIn):
    if At == Dt:
        Vtrestrict = -V0/2 + Jm*Xt/At - Jm*V0**2/(2*At**2)
    else:
        sqrt_term = Dt*(At**4*Dt + 2*At**3*Dt**2 - 4*At**3*Jm*V0 + At**2*Dt**3 + 4*At**2*Dt*Jm*V0 + 8*At**2*Jm**2*Xt - 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)
        if  sqrt_term< 0:
            print("incorrect Vt calc")
            raise ValueError
        else:
            #Vt > 0
            Vtrestrict = (-At*Dt*(At + Dt) + math.sqrt(sqrt_term))/(2*Jm*(At - Dt))
    return Vtrestrict


def calc_case_1(At,Dt,V0,Jm,Xt,VtIn):
    if At == Dt:
        sqrt_term = (At**4 - 2*At**2*Jm*V0 + 4*At*Jm**2*Xt + 2*Jm**2*V0**2)
        if  sqrt_term< 0:
            print("incorrect Vt calc")
            raise ValueError
        else:
            #the correct soln should be +ve, otherwise we go into negative time
            Vtrestrict = (-At**2 + math.sqrt(sqrt_term))/(2*Jm)
    else:
        sqrt_term = Dt*(At + Dt)*(At**3*Dt + At**2*Dt**2 - 4*At**2*Jm*V0 + 8*At*Jm**2*Xt + 4*Jm**2*V0**2)
        if sqrt_term < 0:
            print("incorrect Vt calc")
            raise ValueError
        else:
            Vtrestrict = (-At*Dt*(At + Dt) + math.sqrt(sqrt_term))/(2*Jm*(At + Dt))

    return Vtrestrict


def calc_case_3(At,Dt,V0,Jm,Xt,VtIn):
    if At == Dt:
        sqrt_term = At**4 + 2*At**2*Jm*V0 - 4*At*Jm**2*Xt + 2*Jm**2*V0**2
        if  sqrt_term< 0:
            print("incorrect Vt calc")
            raise ValueError
        else:
            Vtrestrict = (At**2 -math.sqrt(sqrt_term)/2)/(2*Jm)
    else:
        sqrt_term = Dt*(At + Dt)*(At**3*Dt + At**2*Dt**2 + 4*At**2*Jm*V0 - 8*At*Jm**2*Xt + 4*Jm**2*V0**2)
        if  sqrt_term< 0:
            print("incorrect Vt calc")
            raise ValueError
        else:
            Vtrestrict = (At*Dt*(At + Dt) - math.sqrt(sqrt_term))/(2*Jm*(At + Dt))
            # print(Vtrestrict)
    return Vtrestrict


def calc_case_4(At,Dt,V0,Jm,Xt,VtIn):
    if At == Dt:
        Vtrestrict = -V0/2 + Jm*Xt/At + Jm*V0**2/(2*At**2)
    else:
        sqrt_term = Dt*(At**4*Dt + 2*At**3*Dt**2 + 4*At**3*Jm*V0 + At**2*Dt**3 - 4*At**2*Dt*Jm*V0 - 8*At**2*Jm**2*Xt + 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)
        if  sqrt_term< 0:
            print("incorrect Vt calc")
            raise ValueError
        else:
            Vtrestrict = (At*Dt*(At + Dt) - math.sqrt(sqrt_term))/(2*Jm*(At - Dt))
            # print(Vtrestrict)
    return Vtrestrict
