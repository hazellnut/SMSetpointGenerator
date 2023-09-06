import sympy as sym



Xt = sym.Symbol('Xt')
Vt = sym.Symbol('Vt')
At = sym.Symbol('At',positive=True)
Dt = sym.Symbol('Dt',positive=True)
Jm = sym.Symbol('Jm',positive=True)

V0 = sym.Symbol('V0')
Ta = sym.Symbol('Ta',positive=True)
Tj = sym.Symbol('Tj',positive=True)
Tjd = sym.Symbol('Tjd',positive=True)
Td = sym.Symbol('Td',positive=True)

X1 = sym.Symbol('X1')
X2 = sym.Symbol('X2')
X3 = sym.Symbol('X3')
X4 = sym.Symbol('X4')
X5 = sym.Symbol('X5')
X6 = sym.Symbol('X6')

V1 = sym.Symbol('V1')
V2 = sym.Symbol('V2')
V3 = sym.Symbol('V3')
V4 = sym.Symbol('V4')
V5 = sym.Symbol('V5')
V6 = sym.Symbol('V6')

sq = sym.Symbol("SQ")

# Dt = At
Tj = At/Jm
Tjd = Dt/Jm

# case: We have a positive V0 and a positive Xt. Now we need to figure out out profile-
# there are 3 options for that we need to distinguish between- 
# 1. increase V0 to a Vt and then decrease to 0 to get to Xt i.e. +Jm, +Am, -Jm, 0, -Jm, -Am, +Jm
# 2. decrease V0 to a (still positive) Vt and then decrease to get to Xt i.e. -Jm, -Am,+jm,0,-Jm,-Am,+Jm
# 3. decrease V0 to a negative Vt and then increase to get to Xt i.e. -Jm, -Am, +Jm, 0, Jm, Am, -Jm

# we need to find conditions where these profiles have solutions for the input parameters. Additionally finding Am, Vm such that we always have a solution and a valid Ta
# first point of order is deciding- do we have enough Am for the current parameters to complete a fully jerk only move
# once this is established we need to find a Vm such that we can reach the target position. How do we do all of this with the constraints of the profile types? We can probably do some basic calculations to rule out 
# some scenarios.

#let's just start off by doing all the calculations and see where we find ourselves

#assumption 1: we have a vt of the same sign and an At of the same sign


s1 =1
s2 =1

# V0 = 0

Ta = -At/Jm - V0/At + Vt/At
Td = -Dt/Jm - Vt/Dt



V1 = V0 + s1*Jm*Tj**2/2
V2 = V1  +s1*At*Ta
V3 = V2 + s1*At*Tj - s1*Jm*Tj**2/2

V4 = Vt + s2*Jm*Tjd**2/2
V5 = V4 + s2*Dt*Td
V6 = V5 + s2*Dt*Tjd - s2*Jm*Tjd**2/2

# eq = sym.Eq(V3,Vt)
# print(sym.solve(eq,Ta))



X1 = V0*Tj +s1* Jm*Tj**3/6
X2 = X1 + V1*Ta +s1*At*Ta**2/2
X3 = X2 + V2*Tj +s1* At*Tj**2/2 -s1* Jm*Tj**3/6
X4 = X3 + Vt*Tjd + s2*Jm*Tjd**3/6
X5 = X4 + V4*Td + s2*Dt*Td**2/2
X6 = X5 + V5*Tjd + s2*Dt*Tjd**2/2 - s2*Jm*Tjd**3/6


print(sym.simplify(X6))

# SQ = Dt*(At + Dt)*(At**3*Dt + At**2*Dt**2 + 4*At**2*Jm*V0 - 8*At*Jm**2*Xt +4*Jm**2*V0**2)
                   
eq = sym.Eq(V3,Vt)
eq2 = sym.Eq(V6,0)
print(sym.solve(eq,Ta))
print(sym.solve(eq2,Td))


eq2 = sym.Eq(V6,0)
eq3 = sym.Eq(X6,Xt)
eq4 = sym.Eq(V3,Vt)
print(sym.solveset(eq3,Vt))


# eq5 = sym.Eq(SQ,0)
# print(sym.solve(eq5,Dt))

# print(sym.solveset(Dt*(At + Dt)*(At**3*Dt + At**2*Dt**2 + 4*At**2*Jm*V0 - 8*At*Jm**2*Xt +4*Jm**2*V0**2)> 0,Dt,sym.Reals))

# print(sym.solveset(At**4 - 16*At**2*Jm*V0 + 32*At*Jm**2*Xt - 16*Jm**2*V0**2>0,At,sym.Reals))

# print(sym.solve(At**3*Dt + At**2*Dt**2 + 4*At**2*Jm*V0 - 8*At*Jm**2*Xt + 4*Jm**2*V0**2 ,Dt))



# print(sym.factor(Dt*(At**4*Dt + 2*At**3*Dt**2 - 4*At**3*Jm*V0 + At**2*Dt**3 + 4*At**2*Dt*Jm*V0 + 8*At**2*Jm**2*Xt - 8*At*Dt*Jm**2*Xt - 4*At*Jm**2*V0**2 + 4*Dt*Jm**2*V0**2)))