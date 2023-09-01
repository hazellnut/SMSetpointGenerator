import math
from num_utils import *

DEBUG = True


def run_numerical_test(V0,At,Dt,Xt,VtIn,Jm):
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

            Dx1 = At1*V0/(2*Jm) + At1*VtIn/(2*Jm) + Dt1*VtIn/(2*Jm) + VtIn**2/(2*Dt1) - V0**2/(2*At1) + VtIn**2/(2*At1)
            if Dx1 < Xt and not Ta < 0 and not Td<0:
                Vt1 = VtIn
                resolved = True
                continue


            try:
                Vtrestrict = case_1_velo(At1,Dt1,V0,Jm,Xt,VtIn)
                error = False
            except ValueError:  
                case = 3
                error = True
                continue

            if not error:
                accelmodified = False
                if Vtrestrict < (V0 + At1**2/Jm) or Vtrestrict < Dt1**2/Jm :
                    if DEBUG:
                        print("need to change At")
                    accelmodified = True
                    if Vtrestrict < (V0 + At**2/Jm):
                        At1 = math.sqrt(Jm*abs(Vtrestrict-V0))

                    if Vtrestrict < Dt**2/Jm:
                        Dt1 = math.sqrt(Jm*abs(Vtrestrict))
                    try:
                        Vtrestrict = case_1_velo(At1,Dt1,V0,Jm,Xt,VtIn)
                    except ValueError:
                        case = 3
                        
                        continue
                    
                if Vtrestrict < 0:
                    case = 3
                    #VtIn = Vtrestrict
                    if DEBUG:
                        print ("changed case to 3")
                    continue
                elif Vtrestrict < V0:
                    if DEBUG:
                        print("changed case to 2")
                    case = 2
                    VtIn = min(Vtrestrict,VtIn)
                    At = min(At1,At)
                    Dt = min(Dt1,Dt)
                    continue

                if Vtrestrict < VtIn or accelmodified:
                    Vt1 = Vtrestrict
                else:
                    Vt1 = VtIn

                ta1 = -At1/Jm - V0/At1 + Vt1/At1
                td1= -Dt1/Jm + Vt1/Dt1
                Ta =ta1
                Td = td1
                Dx1 = At1*V0/(2*Jm) + At1*Vt1/(2*Jm) + Dt1*Vt1/(2*Jm) + Vt1**2/(2*Dt1) - V0**2/(2*At1) + Vt1**2/(2*At1)
            resolved = True
        #case 2- Vt < V0, Vt > 0 s1 = -1, s2=-1
        # if VtIn > 0 and VtIn < V0:

        if case == 2:
            VtIn = abs(VtIn)
            At2 = At
            Dt2 = Dt


            ta2 = -At2/Jm + V0/At2 - Vt2/At2
            td2 = -Dt2/Jm + Vt2/Dt
            Dx2 = At2*V0/(2*Jm) + At2*VtIn/(2*Jm) + Dt2*VtIn/(2*Jm) + VtIn**2/(2*Dt2) + V0**2/(2*At2) - VtIn**2/(2*At2)

            if Dx2 < Xt and not ta2 < 0 and not td2<0:
                Vt2 = VtIn
                resolved = True
                continue
            try:
                Vtrestrict = case_2_velo(At2,Dt2,V0,Jm,Xt,VtIn)
            except ValueError:
                case = 3
                if DEBUG:
                    print("changed to case 3")
                continue
            
            if Vtrestrict > (V0 - At2**2/Jm) or Vtrestrict < Dt2**2/Jm:
                if DEBUG:
                    print("need to change At")
                if Vtrestrict > (V0 - At2**2/Jm):
                    At2 = math.sqrt(Jm*abs(Vtrestrict-V0))

                if Vtrestrict < Dt2**2/Jm:
                    Dt2 = math.sqrt(Jm*abs(Vtrestrict))
                Vtrestrict = case_2_velo(At2,Dt2,V0,Jm,Xt,Vtrestrict)

                
            if Vtrestrict < 0:
                if DEBUG:
                    print("changed case to 3")
                case = 3
                VtIn = min(Vtrestrict,VtIn)
                At = min(At2,At)
                Dt = min(Dt2,Dt)
                continue


            Vt2 = Vtrestrict
            ta2 = -At2/Jm + V0/At2 - Vt2/At2
            td2 = -Dt2/Jm + Vt2/Dt
            Dx2 = At2*V0/(2*Jm) + At2*Vt2/(2*Jm) + Dt2*Vt2/(2*Jm) + Vt2**2/(2*Dt2) + V0**2/(2*At2) - Vt2**2/(2*At2)



            resolved = True
        if case == 3:
            VtIn = -abs(VtIn)

            At3 = At
            Dt3 = Dt
            ta3 = -At3/Jm + V0/At3 - VtIn/At3
            td3 = -Dt3/Jm - VtIn/Dt3
            Dx3 = At*V0/(2*Jm) + At*VtIn/(2*Jm) + Dt*VtIn/(2*Jm) - VtIn**2/(2*Dt) + V0**2/(2*At) - VtIn**2/(2*At)

            if Dx3 > Xt and not ta3 < 0 and not td3<0:
                if DEBUG:
                    print(ta3)
                    print(td3)
                Vt3 = VtIn
                resolved = True
                continue
            try:
                Vtrestrict = case_3_velo(At3,Dt3,V0,Jm,Xt,VtIn)
            except ValueError:
                case = 1
                continue

            if Vtrestrict > (V0 - At3**2/Jm) or Vtrestrict > -Dt3**2/Jm:
                if DEBUG:
                    print("need to change accels")
                if Vtrestrict > (V0 - At3**2/Jm):
                    At3 = math.sqrt(Jm*abs(Vtrestrict-V0))

                if Vtrestrict > -Dt3**2/Jm:
                    Dt3 = math.sqrt(Jm*abs(Vtrestrict))
                try:
                    Vtrestrict = case_3_velo(At3,Dt3,V0,Jm,Xt,Vtrestrict)
                except ValueError:
                    case = 1
                    
                    continue
                #print ("stuck in here maybe")

            if Vtrestrict > VtIn:
                Vt3 = Vtrestrict
            else:
                Vt3 = VtIn


            if Vt3 > V0:
                if Vt3 > 0:
                    if DEBUG:
                        print("changed case to 1")
                    case = 1
                    continue
                if DEBUG:
                    print("changed case to 4")
                VtIn = min(Vt3,VtIn)
                At = min(At3,At)
                Dt = min(Dt3,Dt)
                case=4
                # VtIn = Vt3
                continue
            
            ta3 = -At3/Jm + V0/At3 - Vt3/At3
            td3 = -Dt3/Jm - Vt3/Dt3

            Ta =ta3
            Td = td3
            Dx3 = At*V0/(2*Jm) + At*Vt3/(2*Jm) + Dt*Vt3/(2*Jm) - Vt3**2/(2*Dt) + V0**2/(2*At) - Vt3**2/(2*At)
            resolved = True
        #case 4- Vt > V0, Vt < 0 s1 = 1, s2 = 1
        # if Vt > V0 and Vt < 0:
        if case == 4:
            VtIn = -abs(VtIn)

            #initial calculations
            At4 = At
            Dt4 = Dt
            ta4 = -At4/Jm - V0/At4 + VtIn/At4
            td4 = -Dt4/Jm - VtIn/Dt4
            Ta =ta4
            Td = td4
            Dx4 = At4*V0/(2*Jm) + At4*VtIn/(2*Jm) + Dt4*VtIn/(2*Jm) - VtIn**2/(2*Dt4) - V0**2/(2*At4) + VtIn**2/(2*At4)
            Vtrestrict = VtIn

            if Dx4 >= Xt and not Ta<0 and not Td <0:
                resolved = True
                Vt4 = VtIn
                continue

            try:
                Vtrestrict = case_4_velo(At4,Dt4,V0,Jm,Xt,VtIn)
            except ValueError:
                case = 1
                
                continue


            if Vtrestrict < (V0 + At4**2/Jm) or Vtrestrict > -Dt4**2/Jm:
                if DEBUG:
                    print("need to change accels")
                if Vtrestrict < (V0 + At4**2/Jm):
                    At4 = math.sqrt(Jm*abs(Vtrestrict-V0))

                if Vtrestrict > -Dt4**2/Jm:
                    Dt4 = math.sqrt(Jm*abs(Vtrestrict))
                Vtrestrict = case_4_velo(At4,Dt4,V0,Jm,Xt,Vtrestrict)

            
            if Vtrestrict > 0:
                case = 1
                if DEBUG:
                    print("moved to case 1")
                VtIn = min(Vtrestrict,VtIn)
                At = min(At4,At)
                Dt = min(Dt4,Dt)
                continue

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



    if (case==1):
            Dx = Dx1
            ta = ta1
            td = td1
            if DEBUG:
                print("case 1\n")
                print("printing velo...")
                print(Vt1)
            At = At1
            Dt = Dt1
            Vt = Vt1
    elif (case==2):
            Dx = Dx2
            ta = ta2
            td = td2
            if DEBUG:
                print("case 2\n")
                print("printing velo...")
                print(Vt2)
            At = At2
            Dt = Dt2
            Vt = Vt2
    elif (case == 4):
            Dx = Dx4
            ta = ta4
            td = td4
            if DEBUG:
                print("case 4\n")
                print("printing velo...")
                print(Vt4)
            At = At4
            Dt = Dt4
            Vt = Vt4
    else:
            Dx = Dx3
            ta = ta3
            td = td3
            At = At3
            Dt = Dt3
            Vt = Vt3
            if DEBUG:
                print("case 3\n")
                print("printing velo...")
                print(Vt3)
    if DEBUG:
        print(f"Vt = {Vt}")

    # if ta < 0 or td < 0:
    #     At = math.sqrt(Jm*abs(VtIn-V0))
        
    #     print(At)


        
    # print("DXes")
    # print(Dx1)
    # print(Dx2)
    # print(Dx3)
    # print(Dx4)
    if DEBUG:
        print(f"At:{At},Dt:{Dt}")
        print("Dx:")
        print(Dx)
        print("ta,td:")
        print(ta)
        print(td)
        if (ta < 0 or td <0):
            print(f"Invalid: {ta}, {td}")

    return ta,td,Dx,Vt,At,Dt, case

if __name__ == "__main__":
    V0 =-100
    At = 50
    Dt = 200
    Xt = -50
    VtIn = -300
    Jm = 50
    run_numerical_test(V0,At,Dt,Xt,VtIn,Jm)