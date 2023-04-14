from Code.body_parts.subclasses.head import Head
from Code.body_parts.subclasses.neck import Neck
from Code.body_parts.subclasses.trunk import Trunk
from Code.body_parts.subclasses.arm import Arm
from Code.body_parts.subclasses.forearm import Forearm
from Code.body_parts.subclasses.hand import Hand
from Code.body_parts.subclasses.thigh import Thigh
from Code.body_parts.subclasses.leg import Leg
from Code.body_parts.subclasses.foot import Foot
from Code.overall_model.body_model import Body as body
from Code.constants import Constants as cst
import math
import scipy.optimize as opt
import numpy as np

body=body()
body.Tamb = body.TC(body.Tamb)
print(body.Tamb)
body.aggiorna_Tint()

print(body.TC(body.Tamb))


def error_function(x):
    res = 0
    i = 0  # 1 #2

    for part in body.body_parts:

        # part.eps = x[0]
        # part.delta = x[1]           #
        if not type(part) == Trunk:
            part.Tint = x[i]
            i = i + 1

    for part in body.body_parts:
        res += part.Udot() ** 2

    print(res)
    return res


import scipy.optimize as opt
import numpy as np

# 0.9,
res = opt.minimize(error_function, np.array([311.5, 310.5, 309, 308.5, 308, 309, 308.5, 308]))
print('\n')
print(res.x)

i = 0
for part in body.body_parts:
    if not type(part) == Trunk:
        part.Tint = res.x[i]
        i += 1
###1###


i = 0 #1  # 2
a=['head', 'neck', 'arm', 'forearm', 'hand', 'thigh', 'leg', 'foot']
print('\n')
for part in body.body_parts:
    if not type(part) == Trunk:
        print(part.Tint)
        print(a[i],'Tsk=', part.Tsk(), '[K]')
        print(a[i],'Qc=', part.Qc(), '[W]')
        print(a[i],'Qr=', part.Qr(), '[W]')
        print(a[i],'He=', part.He(), '[W]')
        print(a[i],'H_res=', part.H_res(), '[W]')
        print( a[i],'Tint=', part.Tint,'[K]')   #f'{type(part)} ='
        print (a[i],'Udot=', part.Udot(),'[W] ,')
        print('\n')
        i = i + 1

