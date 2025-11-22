# +-+-+-+-+-+-+-+- 2d network adjustment  parametric model +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- 
from func_dep import * 
# +-+-Load the Excel file +-+-+-+-+  
obs_path= '4point_check.xlsx' 
init_coord_path = 'init_cord_out.xlsx' 
df = pd.read_excel(obs_path) 
int_cord = pd.read_excel(init_coord_path) 


# Define symbols (example for first few points; you should define all) +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
xBL1, yBL1, xBL2, yBL2, xBL3, yBL3, xBL4, yBL4, xBL5, yBL5 = sp.symbols("xBL1 yBL1 xBL2 yBL2 xBL3 yBL3 xBL4 yBL4 xBL5 yBL5")

xBR1, yBR1, xBR2, yBR2, xBR3, yBR3, xBR4, yBR4, xBR5, yBR5 = sp.symbols("xBR1 yBR1 xBR2 yBR2 xBR3 yBR3 xBR4 yBR4 xBR5 yBR5")

xBR6, yBR6, xBC3, yBC3, xCD1, yCD1, xCD2, yCD2, xCD4, yCD4 = sp.symbols("xBR6 yBR6 xBC3 yBC3 xCD1 yCD1 xCD2 yCD2 xCD4 yCD4")

# xCD5, yCD5, xCD6, yCD6, xCU1, yCU1, xCU2, yCU2, xCU3, yCU3 = sp.symbols("xCD5 yCD5 xCD6 yCD6 xCU1 yCU1 xCU2 yCU2 xCU3 yCU3")

# xCU4, yCU4, xCU5, yCU5, xCU6, yCU6, xD1, yD1, xD2, yD2 = sp.symbols("xCU4 yCU4 xCU5 yCU5 xCU6 yCU6 xD1 yD1 xD2 yD2")

# xD3, yD3, xD4, yD4 = sp.symbols("xD3 yD3 xD4 yD4")


# +-+-+-+-+-+-+-+-+-+-+-+-+-unknown vector +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

fixed_point = sp.Matrix([[xBC3],[yBC3]])
BL_points = sp.Matrix([[xBL2], [yBL2], [xBL3], [yBL3], [xBL4], [yBL4], [xBL5], [yBL5]])
BR_points = sp.Matrix([[xBR1], [yBR1], [xBR2], [yBR2], [xBR3], [yBR3], [xBR4], [yBR4], [xBR5], [yBR5], [xBR6], [yBR6]])
#BC_points = sp.Matrix([[xBC3], [yBC3]])

# CD_points = sp.Matrix([[xCD1], [yCD1], [xCD2], [yCD2], [xCD4], [yCD4], [xCD5], [yCD5], [xCD6], [yCD6]])
# CU_points = sp.Matrix([[xCU1], [yCU1], [xCU2], [yCU2], [xCU3], [yCU3], [xCU4], [yCU4], [xCU5], [yCU5], [xCU6], [yCU6]])
# D_points  = sp.Matrix([[xD1], [yD1], [xD2], [yD2], [xD3], [yD3], [xD4], [yD4]])


X_s = sp.Matrix.vstack( fixed_point,
                        BL_points,
                        BR_points)
                       # CD_points,
                       # CU_points, 
                       # D_points)

X_s_for_jacobian = sp.Matrix.vstack(BL_points,
                                    BR_points)
                                    # CD_points,
                                    # CU_points, 
                                    # D_points)


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# Your symbols

w0_BC3_to_BR1 = sp.symbols('w0_BC3_to_BR1')
w0_BL4_to_BL5 = sp.symbols('w0_BL4_to_BL5')
w0_BR5_to_BR4, w0_BR6_to_BL5= sp.symbols(' w0_BR5_to_BR4 w0_BR6_to_BL5')

w0_s = sp.Matrix([[w0_BC3_to_BR1], [w0_BL4_to_BL5] , [w0_BR5_to_BR4] ,[w0_BR6_to_BL5]])

w0_0 = sp.zeros(len(w0_s), 1)

# +-+-+-+-+-+- initial values for unknowns and observations+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

X0 = sp.zeros(len(int_cord)*2,1)

a=0 # a counter for coordinates 
for i in range(0,len(X0),2):
    X0[i] = index(int_cord,a,'X(m)')
    X0[i+1] = index(int_cord,a,'Y(m)')
    a=a+1


# +-+-+-+-+-+ 2d observation distances +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

dist_obs = defaultdict(list)

for i in range(len(df)):
    a = index(df, i, 'FROM')
    b = index(df, i, 'TO')
    key = frozenset([a, b])
    dist_value = index(df, i, 'proj_to_mz')
    dist_obs[key].append(dist_value)

l0_d = []
l_s_d = []
cl_d = []

for key, values in dist_obs.items():
    avg_value = sum(values) / len(values)
    points = sorted(list(key))
    l0_d.append(avg_value)
    l_s_d.append(f"{points[0]}_{points[1]}")

    
    if len(values) > 1:
        cl_val = (((0.001 + ( (avg_value)*(1e-6))) / sp.sqrt(2))**2).evalf()
    else:
        cl_val = (0.001 + (avg_value*(1e-6)))**2
    cl_d.append(cl_val)

l0_d = sp.Matrix(l0_d)
l_s_d = sp.Matrix(l_s_d)
cl_d_vector = sp.Matrix(cl_d)

# +-+-+-+-+-+ 2d observation hz angles +-+-+-+-+-+-+-
l_s_hz = sp.zeros(len(df),1)
cl_hz_vector = sp.zeros(len(df),1)
l0_hz = sp.zeros(len(df),1)


for i in range(len(df)):
    l0_hz[i] = ((index(df, i, 'HZ_decimal') * sp.pi/180).evalf())
    a = index(df,i,'FROM')
    b = index(df,i,'TO')
    l_s_hz[i] = f"{a}_to_{b}"
    cl_hz_vector[i] = (((0.7/3600)*sp.pi/180)**2).evalf()

# +-+-+-+-+-+- constraint +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
const_weight = sp.Matrix([[1]])
cl_values = sp.Matrix.vstack(cl_d_vector, cl_hz_vector, const_weight)
CL = sp.diag(*cl_values)
p = np.array(CL.inv(), dtype=float)


#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV    
l0_zero_for_az = sp.Matrix([[0]])
l0 = sp.Matrix.vstack(l0_d,l0_hz,l0_zero_for_az)
l0_s = sp.Matrix.vstack(l_s_d,l_s_hz)


print(p.shape)
# creating dictionary fot unknowns and observations

value_x = make_dict(X_s,X0)



# for i in range(len(w0_s)):
#     # Convert symbol to string and split
#     parts = str(w0_s[i]).split("_")
#     a = parts[1]
#     b = parts[3]

#     xi = sp.symbols(f"x{a}") 
#     yi = sp.symbols(f"y{a}") 
#     xj = sp.symbols(f"x{b}") 
#     yj = sp.symbols(f"y{b}") 

#     # Assign angle to matrix
#     w0_0[i] = ((mytan_sym_wrap(xi,xj,yi,yj).subs(value_x).evalf())*sp.pi/180).evalf()


# w0 = make_dict(w0_s, w0_0)

# #print(l0)

# all_value = value_x | w0
# all_unknown = sp.Matrix.vstack(X_s,w0_s)

# # # +-+-+-+-+-+- creating math model for distance obzervation +-+-+-+-+-+-+-+- 
# f = sp.zeros(len(l0_s),1)
# q = 0
# first_angle_processed = False  

# for i in range(len(l0_s)):
    
#     name = str(l0_s[i])
#     # angles hz
#     if "_to_" in name:
#         if first_angle_processed and float(l0[i]) == 0:
#             q =q+1 
     
#         first_angle_processed = True

#         pi, pj = name.split("_to_")
#         xi = yi = xj = yj = None

#         for finder in range(0, len(X_s), 2):
#             if str(X_s[finder]) == f"x{pi}":
#                 xi, yi = X_s[finder], X_s[finder+1]
#             if str(X_s[finder]) == f"x{pj}":
#                 xj, yj = X_s[finder], X_s[finder+1]

#         dir_obs = (mytan_sym_wrap(xi,xj,yi,yj).subs(value_x)*sp.pi/180).evalf()
#         zero_az = w0_0[q]

#         # compute angle using current q
#         if   dir_obs > zero_az : 

#             f[i] =((mytan_sym_wrap(xi,xj,yi,yj) *sp.pi/180)  - w0_s[q]) 

#         else: 

#             f[i] =((2*sp.pi)  -  ( w0_s[q] - (mytan_sym_wrap(xi,xj,yi,yj))*sp.pi/180  ) ) 

#         #print(f[i].subs(all_value).evalf() , "       ", zero_az,"    ",l0[i]) 
        

#     else:  # distances
#         pi, pj = name.split("_")
#         xi = yi = xj = yj = None
#         for finder in range(0, len(X_s), 2):
#             if str(X_s[finder]) == f"x{pi}":
#                 xi, yi = X_s[finder], X_s[finder+1]
#             if str(X_s[finder]) == f"x{pj}":
#                 xj, yj = X_s[finder], X_s[finder+1]
#         f[i] = sp.sqrt((xj - xi)**2 + (yj - yi)**2)


# azimoth_const = sp.Matrix([[mytan_sym_wrap(xBL1,xBL5,yBL1,yBL5)*(sp.pi/180)]])   # for bl1 => bl5
# f = sp.Matrix.vstack(f,azimoth_const)



# # evaluating A matrix values =-=-=-=-=-=-=--=-=--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--=
# A = f.jacobian(all_unknown).subs(all_value).evalf()

# A_numpy = np.array(A).astype(np.float64) # converting A to numpy
# #print(f'the model needs "{len(all_unknown)-np.linalg.matrix_rank(A_numpy)}"  constraint')  # = the number of constraint in need

# #-----------------------------------------------------------------------------------------------------------------
# # dividing model into 2 parts d and hz 

# f_d = sp.zeros(len(l0_d),1)
# f_hz = sp.zeros(len(l0_hz),1)
# f_calculated = f.subs(all_value).evalf() # evaluating   f(x0)

# for i in range(len(l0_d)): # extracting distances

#     f_d[i] = f_calculated[i]

# for i in range(len(l0_hz)):# extracting hz angles (mod 360)
     
#     f_hz[i]= f_calculated[len(l0_d)+i]
#     if f_hz[i]>6.28:
#         f_hz[i] = (f_hz[i] - sp.pi*2).evalf()

#     #print(f_hz[i])

# ini_val = sp.Matrix.vstack(X0,w0_0) # all initial values x0 + w0
# ini_val_numpy = np.array(ini_val).astype(np.float64) # converting init values into numpy

# ini_val_numpy_without_fixed_point = np.delete(ini_val_numpy, [0, 1], axis=0)


# #-----------------------------------------------------------------------------------------------------------------

# f_calculated_numeric = sp.Matrix.vstack(f_d,f_hz,l0_zero_for_az)
# f_numpy = np.array(f_calculated_numeric).astype(np.float64) # convert f into numpy array 

# #-----------------------------------------------------------------------------------------------------------------

# l_obs = np.array(l0).astype(np.float64) # converting observations to numpy vector 

# #-----------------------------------------------------------------------------------------------------------------

# dl =l_obs - f_numpy

# #-----------------------------------------------------------------------------------------------------------------

# p_numpy = np.array(p).astype(np.float64) # converting observations weigth to numpy vector 

# #-----------------------------------------------------------------------------------------------------------------

# A_numpy = np.delete(A_numpy, [0, 1], axis=1)  # cosider BL1 as fixed point =-=-=-=-=-=-=-=-
# #N = np.linalg.inv(A_numpy.T@p_numpy@A_numpy)

# #print(np.linalg.det(N))
# # print(N.shape)
# # print(p_numpy.shape)
# # print(dl.shape)

# dxcap = np.linalg.inv(A_numpy.T@p_numpy@A_numpy)@(A_numpy.T)@p_numpy@dl  

# xcap = ini_val_numpy_without_fixed_point + dxcap 



# x0i = sp.Matrix.vstack(sp.Matrix(X0[0:2]), sp.Matrix(xcap))

# all_value = dict(zip(all_unknown,x0i))

# # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- recalculate f +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# f_d = sp.zeros(len(l0_d),1)
# f_hz = sp.zeros(len(l0_hz),1)
# f_calculated = f.subs(all_value).evalf() # evaluating   f(x0)

# for i in range(len(l0_d)): # extracting distances

#     f_d[i] = f_calculated[i]

# for i in range(len(l0_hz)):# extracting hz angles (mod 360)
     
#     f_hz[i]= f_calculated[len(l0_d)+i]
#     if f_hz[i]>6.28:
#         f_hz[i] = (f_hz[i] - sp.pi*2).evalf()

#     #print(f_hz[i])

# f_calculated_numeric = sp.Matrix.vstack(f_d,f_hz,l0_zero_for_az)
# f_numpy = np.array(f_calculated_numeric).astype(np.float64) # convert f into numpy array 


# vcap = l_obs - f_numpy
# vcap_d = vcap[0:len(f_d)]
# vcap_hz = vcap[len(f_d),:]

# N = A_numpy@np.linalg.inv(A_numpy.T@p_numpy@A_numpy)@A_numpy.T@p_numpy
# R = np.eye(133 ,dtype=float) 
# df = np.trace(R-N)

# sigma0cap2 = (vcap_d.T@p_numpy[0:len(vcap_d),0:len(vcap_d)]@vcap_d) / df 

# np.set_printoptions(threshold=np.inf)  # نمایش همه عناصر ماتریس
# N = A_numpy.T@A_numpy

