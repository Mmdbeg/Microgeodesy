import pandas as pd
from math import *
from func_dep import *
import itertools

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-this code will check misclusure error for out network points+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

file_path = 'triangle_check.xlsx'
df = pd.read_excel(file_path)

# +-+-+-+-+-+- make angles decimal +-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
for i in range (len(df)):
    df.loc[i,'hz_decimal'] = dms_to_decimal(index(df,i,'HZ'))
    #print(df.loc[i,'hz_decimal'])

azimuths = {(row['FROM'], row['TO']): row['hz_decimal'] for _, row in df.iterrows()}


# +-+- this function checks if 3 combinations of observationsa create a triangle or not +-+-+-+-+-+
def triangle_angles(p1, p2, p3):
    try:
        a1 = angle_between(azimuths[(p1,p2)], azimuths[(p1,p3)])
        a2 = angle_between(azimuths[(p2,p3)], azimuths[(p2,p1)])
        a3 = angle_between(azimuths[(p3,p1)], azimuths[(p3,p2)])
        return a1, a2, a3
    except KeyError:
        return None  #  does not make a triangle 
    

triangles = []

# +-+-+-+-+- calculate misclosure error for triangles +-+-+-+-+-+-+-+-+- 
for combo in itertools.combinations(set(df['FROM']) | set(df['TO']), 3):
    angles = triangle_angles(*combo)
    if angles:
        total = sum(angles)
        misclose = total - 180
        triangles.append({
            "Triangle": combo,
            "Angles": angles,
            "Sum": total,
            "Misclose": (misclose*3600)
        })
a=0
for t in triangles:
    if abs(t['Misclose']) <= 2.5:  
        #print(t,'\n')
        a=a+1 
r=0
for t in triangles:
    if abs(t['Misclose']) > 2.5:  
        print(t,'\n')
        r=r+1 

print(f'{a} triangles out of {len(triangles)} are accepted ')
print(f'{r} triangles out of {len(triangles)} are rejected')
