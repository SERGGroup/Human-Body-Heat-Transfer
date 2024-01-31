# %%
from main_code.body_parts.subclasses.trunk import Trunk
from main_code.overall_model.body_model import Body
import scipy.optimize as opt
import numpy as np
import math

body = Body()
print(body.TC(body.Tamb))


# %%

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

    # print(res)
    return res


res = opt.minimize(error_function, np.array([311.5, 310.5, 309, 308.5, 308, 309, 308.5, 308]))
print('\n')
print(res.x)

i = 0
for part in body.body_parts:
    if not type(part) == Trunk:
        part.Tint = res.x[i]
        i += 1


