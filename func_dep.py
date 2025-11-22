#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- IN NEEDED LIBRARIES +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
import pandas as pd 
from math import *
import numpy as np
import sympy as sp 
import time
from collections import defaultdict

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- IN NEED FUNCTIONS +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


# +-+- this function could be used to access data frame element +-+-+
def index(data_frame, row_no, col_name):
    return data_frame.loc[row_no, col_name]

# +-+- this function could be used to calculate relative humidity +-+-+
def rh(es_wet, es_dry, t_wet, t_dry, pressure):
    RH = 100 * (es_wet - 0.00066 * pressure * (t_dry - t_wet)) / es_dry
    return RH

# +-+- convert dms angles to decimal +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- 
def dms_to_decimal(dms_str: str) -> float:
    """
    Converts a DMS string (e.g. "103° 08' 51.0\"") to decimal degrees.
    Also supports:
      - Degrees only (e.g. "103°")
      - Degrees + minutes (e.g. "103° 08'")
      - Seconds only (e.g. "45\"")
    Returns a float with full precision.
    """
    # Normalize the string
    dms_str = dms_str.strip().replace("°", " ").replace("'", " ").replace('"', " ")
    parts = dms_str.split()

    # Initialize values
    degrees, minutes, seconds = 0.0, 0.0, 0.0

    # Parse based on how many parts exist
    if len(parts) == 1:
        # Could be degrees, minutes, or seconds
        if "°" in dms_str:
            degrees = float(parts[0])
        elif "'" in dms_str:
            minutes = float(parts[0])
        else:  # assume seconds
            seconds = float(parts[0])
    elif len(parts) == 2:
        degrees = float(parts[0])
        minutes = float(parts[1])
    elif len(parts) == 3:
        degrees = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
    else:
        raise ValueError(f"Unrecognized DMS format: {dms_str}")

    # Convert to decimal degrees
    decimal = degrees + minutes / 60 + seconds / 3600
    return decimal

# +-+- male correction to vertical angles +-+-+-+
def v_corrector(V,S,K):
    r = 6371000
    Z_bar = V + (S*K)/(2*r)
    return Z_bar

# +-+- distance project +-+-+- 
def proj(V,D):
    V = V*pi/180
    proj_d = D * sin(V-(D/(2*6371000)))
    return proj_d

# +-+-+-+ calculate the angles between 2 horizontal distance +-+-+-+-+-+-+
def angle_between(a, b):
    """angle diff 0-360"""
    d = (b - a) % 360
    if (d>=180):
        d=360-d
    return d 


# +-+- this function checks if 3 combinations of observationsa create a triangle or not +-+-+-+-+-+

#azimuths = {(row['FROM'], row['TO']): row['hz_decimal'] for _, row in df.iterrows()}

# def triangle_angles(p1, p2, p3):
#     try:
#         a1 = angle_between(azimuths[(p1,p2)], azimuths[(p1,p3)])
#         a2 = angle_between(azimuths[(p2,p3)], azimuths[(p2,p1)])
#         a3 = angle_between(azimuths[(p3,p1)], azimuths[(p3,p2)])
#         return a1, a2, a3
#     except KeyError:
#         return None  # +-+-+-+-+-+-+-+-+ no triangle


# def mytan(xi,xj,yi,yj,ref_dict=None):

#     dx1 = ref_dict[xj]-ref_dict[xi]
#     dy1 = ref_dict[yj]-ref_dict[yi]

#     if dx1>0 and dy1>0 :
#         a = sp.atan(abs(xj-xi)/abs(yj-yi))*180/sp.pi     
#     if dx1<0 and dy1<0 :
#         a = sp.atan(abs(xj-xi)/abs(yj-yi))*180/sp.pi +180
#     if dx1>0 and dy1<0 :
#         a = 180 - sp.atan(abs(xj-xi)/abs(yj-yi))*180/sp.pi
#     if dx1<0 and dy1>0 :
#         a = 360 - sp.atan(abs(xj-xi)/abs(yj-yi))*180/sp.pi

#     return(a)
def mytan_sym_wrap(xi, xj, yi, yj):
    dx = xj - xi
    dy = yj - yi
    angle_deg = sp.atan2(dx, dy) * 180 / sp.pi

    # بازه 0-360 با Piecewise
    angle_wrapped = sp.Piecewise(
        (angle_deg + 360, angle_deg < 0),
        (angle_deg, angle_deg >= 0)
    )
    return angle_wrapped

# dx,dy=sp.symbols('dx dy')
# sym = sp.Matrix([[dx,dy]])
# val = sp.Matrix([[-1,-1]])
# values = dict(zip(sym,val)) 

# a = mytan(dx,dy,values).subs(values).evalf()
# print(a)



def make_dict(a,b):
    c = dict(zip(a,b))
    return c