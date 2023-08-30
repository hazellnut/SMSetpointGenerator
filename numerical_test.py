import math
from num_utils import *

V0 =0
At = 700
Dt = 200
Xt = -100
VtIn = 200
Jm = 1000


if VtIn < 0:
    if V0 < VtIn:
        case = 4
    else:
        case = 3
else:
    if V0 > VtIn:
        case = 2
    else:
        case=1

#some notes for implementation-

#if accel is modified we HAVE to take a modified velo value too otherwise the numbers don't add up (at the very least modifed before the accel/decel values are)
#process- are our accel values within reason for the current velo?
Vtrestrict = 0


At = min(At,math.sqrt(Jm*abs(VtIn-V0)))
Dt = min(Dt, math.sqrt(Jm*abs(VtIn)))

resolved = False
while(not resolved):
    if case == 1:
        VtIn = abs(VtIn)
        Dt1 = Dt
        At1 = At
        ta1 = -At1/Jm - V0/At1 + VtIn/At1
        td1= -Dt1/Jm + VtIn/Dt1
        Ta =ta1
        Td = td1

        Dx1 = At1**3/Jm**2 + 3*At1**2*Ta/(2*Jm) + At1*Ta**2/2 + 2*At1*V0/Jm - Dt1**3/Jm**2 - 3*Dt1**2*Td/(2*Jm) - Dt1*Td**2/2 + 2*Dt1*VtIn/Jm + Ta*V0 + Td*VtIn
        if Dx1 < Xt and not Ta < 0 and not Td<0:
            Vt1 = VtIn
            resolved = True
            continue


        try:
            Vtrestrict = calc_case_1(At1,Dt1,V0,Jm,Xt,VtIn)
            error = False
        except ValueError:  
            case = 3
            error = True
            continue

        if not error:
            accelmodified = False
            if Vtrestrict < (V0 + At1**2/Jm) or Vtrestrict < Dt1**2/Jm :
                print("need to change At")
                accelmodified = True
                if Vtrestrict < (V0 + At**2/Jm):
                    At1 = math.sqrt(Jm*abs(Vtrestrict-V0))

                if Vtrestrict < Dt**2/Jm:
                    Dt1 = math.sqrt(Jm*abs(Vtrestrict))
                Vtrestrict = calc_case_1(At1,Dt1,V0,Jm,Xt,VtIn)
                
            if Vtrestrict < 0:
                case = 3
                VtIn = Vtrestrict
                print ("changed case to 3")
                continue
            elif Vtrestrict < V0:
                print("changed case to 2")
                case = 2
                VtIn = Vtrestrict
                continue

            if Vtrestrict < VtIn or accelmodified:
                Vt1 = Vtrestrict
            else:
                Vt1 = VtIn

            ta1 = -At1/Jm - V0/At1 + Vt1/At1
            td1= -Dt1/Jm + Vt1/Dt1
            Ta =ta1
            Td = td1
            Dx1 = At1**3/Jm**2 + 3*At1**2*Ta/(2*Jm) + At1*Ta**2/2 + 2*At1*V0/Jm - Dt**3/Jm**2 - 3*Dt1**2*Td/(2*Jm) - Dt1*Td**2/2 + 2*Dt1*Vt1/Jm + Ta*V0 + Td*Vt1
        resolved = True
    #case 2- Vt < V0, Vt > 0 s1 = -1, s2=-1
    # if VtIn > 0 and VtIn < V0:

    if case == 2:
        VtIn = abs(VtIn)
        At2 = At
        Dt2 = Dt
        try:
            Vtrestrict = calc_case_2(At2,Dt2,V0,Jm,Xt,VtIn)
        except ValueError:
            case = 3
            print("changed to case 3")
            continue
        
        if Vtrestrict > (V0 - At2**2/Jm) or Vtrestrict < Dt2**2/Jm:
            print("need to change At")
            if Vtrestrict > (V0 - At2**2/Jm):
                At2 = math.sqrt(Jm*abs(Vtrestrict-V0))

            if Vtrestrict < Dt2**2/Jm:
                Dt2 = math.sqrt(Jm*abs(Vtrestrict))
            Vtrestrict = calc_case_2(At2,Dt2,V0,Jm,Xt,VtIn)

            
        if Vtrestrict < 0:
            print("changed case to 3")
            case = 3
            VtIn = Vtrestrict
            continue







        Vt2 = Vtrestrict
        ta2 = -At2/Jm + V0/At2 - Vt2/At2
        td2 = -Dt2/Jm + Vt2/Dt
        Ta =ta2
        Td = td2
        Dx2 = -At2**3/Jm**2 - 3*At2**2*Ta/(2*Jm) - At2*Ta**2/2 + 2*At2*V0/Jm - Dt2**3/Jm**2 - 3*Dt2**2*Td/(2*Jm) - Dt2*Td**2/2 + 2*Dt2*Vt2/Jm + Ta*V0 + Td*Vt2



        resolved = True
    if case == 3:
        VtIn = -abs(VtIn)
        #make input velo negative
        #VtIn = -abs(VtIn)
    #case 3- Vt < V0, Vt < 0-- s1=-1 s2 = 1
        #1: do pre calculation of Dx

        #2: if Dx is exceeded in the direction required OR ta or td are negative, recalculate Vtrestrict

        #3: cycle through until 
        At3 = At
        Dt3 = Dt
        ta3 = -At3/Jm + V0/At3 - VtIn/At3
        td3 = -Dt3/Jm - VtIn/Dt3
        Ta =ta3
        Td = td3
        Dx3 = -At3**3/Jm**2 - 3*At3**2*Ta/(2*Jm) - At3*Ta**2/2 + 2*At3*V0/Jm + Dt3**3/Jm**2 + 3*Dt3**2*Td/(2*Jm) + Dt3*Td**2/2 + 2*Dt3*VtIn/Jm + Ta*V0 + Td*VtIn

        if Dx3 > Xt and not Ta < 0 and not Td<0:
            print(Td)
            Vt3 = VtIn
            resolved = True
            continue

        Vtrestrict = calc_case_3(At3,Dt3,V0,Jm,Xt,VtIn)

        if Vtrestrict > (V0 - At3**2/Jm) or Vtrestrict > -Dt3**2/Jm:
            print("need to change accels")
            if Vtrestrict > (V0 - At3**2/Jm):
                At3 = math.sqrt(Jm*abs(Vtrestrict-V0))

            if Vtrestrict > -Dt3**2/Jm:
                Dt3 = math.sqrt(Jm*abs(Vtrestrict))
            Vtrestrict = calc_case_3(At3,Dt3,V0,Jm,Xt,VtIn)
            #print ("stuck in here maybe")





        if Vtrestrict > VtIn:
            Vt3 = Vtrestrict
        else:
            Vt3 = VtIn


        if Vt3 > V0:
            print("changed case to 4")
            case=4
            VtIn = Vt3
            continue


        
        ta3 = -At3/Jm + V0/At3 - Vt3/At3
        td3 = -Dt3/Jm - Vt3/Dt3

        Ta =ta3
        Td = td3
        Dx3 = -At3**3/Jm**2 - 3*At3**2*Ta/(2*Jm) - At3*Ta**2/2 + 2*At3*V0/Jm + Dt3**3/Jm**2 + 3*Dt3**2*Td/(2*Jm) + Dt3*Td**2/2 + 2*Dt3*Vt3/Jm + Ta*V0 + Td*Vt3
        resolved = True
    #case 4- Vt > V0, Vt < 0 s1 = 1, s2 = 1
    # if Vt > V0 and Vt < 0:
    if case == 4:
        VtIn = -abs(VtIn)
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
        At4 = At
        Dt4 = Dt
        ta4 = -At4/Jm - V0/At4 + VtIn/At4
        td4 = -Dt4/Jm - VtIn/Dt4
        Ta =ta4
        Td = td4
        Dx4 = At4*V0/(2*Jm) + At4*VtIn/(2*Jm) + Dt4*VtIn/(2*Jm) - VtIn**2/(2*Dt4) - V0**2/(2*At4) + VtIn**2/(2*At4)
        Vtrestrict = VtIn
        if Dx4 < Xt:
            Vtrestrict = calc_case_4(At4,Dt4,V0,Jm,Xt,VtIn)
            if Vtrestrict > 0:
                case = 1
                print("moved to case 1")
                continue

            if Vtrestrict < (V0 + At4**2/Jm) or Vtrestrict > -Dt4**2/Jm:
                print("need to change accels")
                if Vtrestrict < (V0 + At4**2/Jm):
                    At4 = math.sqrt(Jm*abs(Vtrestrict-V0))

                if Vtrestrict > -Dt4**2/Jm:
                    Dt4 = math.sqrt(Jm*abs(Vtrestrict))
                Vtrestrict = calc_case_4(At4,Dt4,V0,Jm,Xt,VtIn)

            #
            if Vtrestrict > VtIn:
                Vt4 = Vtrestrict
            else:
                Vt4 = VtIn

        # Vt4 = Vtrestrict
            ta4 = -At4/Jm - V0/At4 + Vt4/At4
            td4 = -Dt4/Jm - Vt4/Dt4
            Ta =ta4
            Td = td4
            Dx4 = At4*V0/(2*Jm) + At4*Vt4/(2*Jm) + Dt4*Vt4/(2*Jm) - Vt4**2/(2*Dt4) - V0**2/(2*At4) + Vt4**2/(2*At4)
            resolved = True

print(f"Vt = {Vtrestrict}")

if (case==1):
        Dx = Dx1
        ta = ta1
        td = td1
        print("case 1\n")
        print("printing velo...")
        print(Vt1)
        At = At1
        Dt = Dt1
elif (case==2):
        Dx = Dx2
        ta = ta2
        td = td2
        print("case 2\n")
        print("printing velo...")
        print(Vt2)
        At = At2
        Dt = Dt2
elif (case == 4):
        Dx = Dx4
        ta = ta4
        td = td4
        print("case 4\n")
        print("printing velo...")
        # print(Vt4)
        At = At4
        Dt = Dt4
else:
        Dx = Dx3
        ta = ta3
        td = td3
        At = At3
        Dt = Dt3
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