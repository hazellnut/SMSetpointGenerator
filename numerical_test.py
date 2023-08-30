import math
from num_utils import *
V0 =-500
At = 200
Dt = 300
Xt = -100
VtIn = 400
Jm = 100


case = 1
# Ta = abs(abs(V0-Vt)/At - At/Jm)

# Tj = At/Jm
# Tjd = Dt/Jm
# Td = abs(Vt/Dt) - Tjd
# V1 = V0 + Jm*Tj**2/2
# V2 = V1 +At*Ta
# V3 = V2 + At*Tj + Jm*Tj**2/2

# V4 = V3 - Jm*Tjd**2/2
# V5 = V4 - Dt*Td
# V6 = V5 - Dt*Tjd - Jm*Tjd**2/2

# X1 = V0*Tj - Jm*Tj**3/6
# X2 = X1 + V1*Ta - At*Ta**2/2
# X3 = X2 + V2*Tj - At*Tj**2/2 + Jm*Tj**3/6
# X4 = V3*Tjd + Jm*Tjd**3/6
# X5 = V4*Td + Dt*Td**2/2
# X6 = V5*Tjd + Dt*Tjd**2/2 - Jm*Tjd**3/6



#case 1- Vt > V0,  Vt > 0- s1 = 1, s2 = -1
# if VtIn > 0 and VtIn > V0:

At = min(At,math.sqrt(Jm*abs(VtIn-V0)))
Dt = min(Dt, math.sqrt(Jm*abs(VtIn)))

if case == 1:

    try:
        Vtrestrict = calc_case_1(At,Dt,V0,Jm,Xt,VtIn)
        error = False
    except ValueError:
        case = 3
        error = True
        
    if not error:
        if Vtrestrict < (V0 + At**2/Jm) or Vtrestrict < Dt**2/Jm :
            print("need to change At")
            if Vtrestrict < (V0 + At**2/Jm):
                At = math.sqrt(Jm*abs(Vtrestrict-V0))

            if Vtrestrict < Dt**2/Jm:
                Dt = math.sqrt(Jm*abs(Vtrestrict))
            Vtrestrict = calc_case_1(At,Dt,V0,Jm,Xt,VtIn)
            
        if Vtrestrict < 0:
            case = 3
            VtIn = Vtrestrict
            print ("changed case to 3")
        elif Vtrestrict < V0:
            print("changed case to 2")
            case = 2
            VtIn = Vtrestrict

        if Vtrestrict < VtIn:
            Vt1 = Vtrestrict
        else:
            Vt1 = VtIn

        ta1 = -At/Jm - V0/At + Vt1/At
        td1= -Dt/Jm + Vt1/Dt
        Ta =ta1
        Td = td1
        Dx1 = At**3/Jm**2 + 3*At**2*Ta/(2*Jm) + At*Ta**2/2 + 2*At*V0/Jm - Dt**3/Jm**2 - 3*Dt**2*Td/(2*Jm) - Dt*Td**2/2 + 2*Dt*Vt1/Jm + Ta*V0 + Td*Vt1

#case 2- Vt < V0, Vt > 0 s1 = -1, s2=-1
# if VtIn > 0 and VtIn < V0:

if case == 2:

    Vtrestrict = calc_case_2(At,Dt,V0,Jm,Xt,VtIn)
    
    # if At == Dt:
    #     Vtrestrict = -V0/2 + Jm*Xt/At - Jm*V0**2/(2*At**2)
    # else:
    #     sqrt_term = Dt*(At**4*Dt + 2*At**3*Dt**2 - 4*At**3*Jm*V0 + At**2*Dt**3 + 4*At**2*Dt*Jm*V0 + 8*At**2*Jm**2*Xt - 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)
    #     if  sqrt_term< 0:
    #         print("incorrect Vt calc")
    #         Vtrestrict = VtIn
    #     else:
    #         #Vt > 0
    #         Vtrestrict = (-At*Dt*(At + Dt) + math.sqrt(sqrt_term))/(2*Jm*(At - Dt))

    if Vtrestrict > (V0 - At**2/Jm) or Vtrestrict < Dt**2/Jm:
        print("need to change At")
        if Vtrestrict > (V0 - At**2/Jm):
            At = math.sqrt(Jm*abs(Vtrestrict-V0))

        if Vtrestrict < Dt**2/Jm:
            Dt = math.sqrt(Jm*abs(Vtrestrict))
        Vtrestrict = calc_case_2(At,Dt,V0,Jm,Xt,VtIn)

    

    # if Vtrestrict > (V0 - At**2/Jm):
    #     print("need to change At")
    #     At = math.sqrt(Jm*abs(Vtrestrict-V0))
    #     print("changed to")
    #     print(At)
        
    # if Vtrestrict < Dt**2/Jm:
    #     print("need to change Dt")
    #     Dt = math.sqrt(Jm*abs(Vtrestrict))
    #     #need to recalc Vrestrict
        
    if Vtrestrict < 0:
        print("changed case to 3")
        case = 3
        VtIn = Vtrestrict







    Vt2 = Vtrestrict
    ta2 = -At/Jm + V0/At - Vt2/At
    td2 = -Dt/Jm + Vt2/Dt
    Ta =ta2
    Td = td2
    Dx2 = -At**3/Jm**2 - 3*At**2*Ta/(2*Jm) - At*Ta**2/2 + 2*At*V0/Jm - Dt**3/Jm**2 - 3*Dt**2*Td/(2*Jm) - Dt*Td**2/2 + 2*Dt*Vt2/Jm + Ta*V0 + Td*Vt2

if case == 3:
#case 3- Vt < V0, Vt < 0-- s1=-1 s2 = 1
# if VtIn < 0 and Vt < V0:
    # if At == Dt:
    #     sqrt_term = At**4 + 2*At**2*Jm*V0 - 4*At*Jm**2*Xt + 2*Jm**2*V0**2
    #     if  sqrt_term< 0:
    #         print("incorrect Vt calc")
    #         Vtrestrict = VtIn
    #     else:
    #         Vtrestrict = (At**2 -math.sqrt(sqrt_term)/2)/(2*Jm)
    # else:
    #     sqrt_term = Dt*(At + Dt)*(At**3*Dt + At**2*Dt**2 + 4*At**2*Jm*V0 - 8*At*Jm**2*Xt + 4*Jm**2*V0**2)
    #     if  sqrt_term< 0:
    #         print("incorrect Vt calc")
    #         Vtrestrict = VtIn
    #     else:
    #         Vtrestrict = (At*Dt*(At + Dt) - math.sqrt(sqrt_term))/(2*Jm*(At + Dt))
    #         # print(Vtrestrict)

    Vtrestrict = calc_case_3(At,Dt,V0,Jm,Xt,VtIn)

    if Vtrestrict > (V0 - At**2/Jm) or Vtrestrict > -Dt**2/Jm:
        print("need to change accels")
        if Vtrestrict > (V0 - At**2/Jm):
            At = math.sqrt(Jm*abs(Vtrestrict-V0))

        if Vtrestrict > -Dt**2/Jm:
            Dt = math.sqrt(Jm*abs(Vtrestrict))
        Vtrestrict = calc_case_2(At,Dt,V0,Jm,Xt,VtIn)
        #print ("stuck in here maybe")


    if Vtrestrict > V0:
        print("changed case to 4")
        case=4
        VtIn = Vtrestrict

    # if Vtrestrict > (V0 - At**2/Jm):
    #     print("need to change At")
    #     At = math.sqrt(Jm*abs(Vtrestrict-V0))
    #     print("changed to")
    #     print(At)

    #     pass
    # if Vtrestrict > -Dt**2/Jm:
    #     print("need to change Dt")
    #     Dt = math.sqrt(Jm*abs(Vtrestrict))
    #     pass


    Vt3 = Vtrestrict
    ta3 = -At/Jm + V0/At - Vt3/At
    td3 = -Dt/Jm - Vt3/Dt
    Ta =ta3
    Td = td3
    Dx3 = -At**3/Jm**2 - 3*At**2*Ta/(2*Jm) - At*Ta**2/2 + 2*At*V0/Jm + Dt**3/Jm**2 + 3*Dt**2*Td/(2*Jm) + Dt*Td**2/2 + 2*Dt*Vt3/Jm + Ta*V0 + Td*Vt3

#case 4- Vt > V0, Vt < 0 s1 = 1, s2 = 1
# if Vt > V0 and Vt < 0:
if case == 4:
    # if At == Dt:
    #     Vtrestrict = -V0/2 + Jm*Xt/At + Jm*V0**2/(2*At**2)
    # else:
    #     sqrt_term = Dt*(At**4*Dt + 2*At**3*Dt**2 + 4*At**3*Jm*V0 + At**2*Dt**3 - 4*At**2*Dt*Jm*V0 - 8*At**2*Jm**2*Xt + 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)
    #     if  sqrt_term< 0:
    #         print("incorrect Vt calc")
    #         Vtrestrict = VtIn
    #     else:
    #         Vtrestrict = (At*Dt*(At + Dt) - math.sqrt(sqrt_term))/(2*Jm*(At - Dt))
    #         # print(Vtrestrict)

    Vtrestrict = calc_case_4(At,Dt,V0,Jm,Xt,VtIn)

    Vt4 = Vtrestrict
    ta4 = -At/Jm - V0/At + Vt4/At
    td4 = -Dt/Jm - Vt4/Dt
    Ta =ta4
    Td = td4
    Dx4 = At**3/Jm**2 + 3*At**2*Ta/(2*Jm) + At*Ta**2/2 + 2*At*V0/Jm + Dt**3/Jm**2 + 3*Dt**2*Td/(2*Jm) + Dt*Td**2/2 + 2*Dt*Vt4/Jm + Ta*V0 + Td*Vt4


if (Vtrestrict >= 0):
    if Vtrestrict > V0:
        Dx = Dx1
        ta = ta1
        td = td1
        print("case 1\n")
        print("printing velo...")
        print(Vt1)
    else:
        Dx = Dx2
        ta = ta2
        td = td2
        print("case 2\n")
        print("printing velo...")
        print(Vt2)
else:
    if Vtrestrict > V0:
        Dx = Dx4
        ta = ta4
        td = td4
        print("case 4\n")
        print("printing velo...")
        print(Vt4)
    else:
        Dx = Dx3
        ta = ta3
        td = td3
        print("case 3\n")
        print("printing velo...")
        print(Vt3)



if ta < 0 or td < 0:
    At = math.sqrt(Jm*abs(VtIn-V0))
    
    print(At)


    
# print("DXes")
# print(Dx1)
# print(Dx2)
# print(Dx3)
# print(Dx4)

print(f"At:{At},Dt:{Dt}")
print("Dx:")
print(Dx)
print("ta,td:")
print(ta)
print(td)