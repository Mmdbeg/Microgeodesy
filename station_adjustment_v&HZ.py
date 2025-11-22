from func_dep import * 
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# PLEASE SET 3 FIRST LATTER OF STATION OBSERVATION FILE NAME AS STATION ID {LIKE BL5}
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
file_name = 'bl5_kopl.xlsx'
df = pd.read_excel(file_name)
a = file_name[:3]



for i in range(len(df)):
    df.loc[i,'HZ_decimal'] = dms_to_decimal(index(df,i,'HZ'))
    df.loc[i,'V_decimal'] = dms_to_decimal(index(df,i,'V'))


v_hz = np.zeros((9,8)) # residual matrix  +-+-+-+-+-+ set number - observation number 
v_v = np.zeros((9,8)) 

# +-+-+-+-+ calculate each set angle +-+-+-+-+-+-+- 
for i in range(0,len(df)-1,2):
    df.loc[i, 'final_HZ'] = (index(df, i, 'HZ_decimal') + (val + 180 if (val := index(df, i+1, 'HZ_decimal')) < 180 else val - 180))/2
    df.loc[i, 'final_V'] = (index(df, i, 'V_decimal') + (val + 180 if (val := index(df, i+1, 'V_decimal')) < 180 else val - 180))/2
    #print(index(df,i,'final_HZ'))

final_HZ = df['final_HZ'].to_numpy()
final_V = df['final_V'].to_numpy()

final_HZ = final_HZ[~np.isnan(final_HZ)]
final_V = final_V[~np.isnan(final_V)]

# reshape 
final_HZ = final_HZ.reshape(9, 8, order='F')
final_V = final_V.reshape(9, 8, order='F')

np.set_printoptions(precision=6, suppress=True)  # suppress=True 

# +-+-+--++ calculate each set observation diffrence from whole set  +-+-+-++-
for i in range(9): # +-+-+-+- horizontal -+-+-+-+-+- 
    for j in range(8):
        v_hz[i,j] = final_HZ[i,j] - np.mean(final_HZ[:,j])

for i in range(9): # +-+-+-+-+-+ vertical +-+-+-+-+
    for j in range(8):
        v_v[i,j] = final_V[i,j] - np.mean(final_V[:,j])
# +--+-+++---+-+++---+-+++---+-+++---+-+++---+-+++---+-+++---+-+++---+-+++-
m = 9 # set
n = 8 # obs number 
sum_hz = 0
sum_v = 0
for i in range(9):
    sum_hz = sum_hz + (np.sum(v_hz[i,:]))**2
for i in range(9):
    sum_v = sum_v + (np.sum(v_v[i,:]))**2

# +-+-+-+-+- mean square error +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
MSN_hz = sqrt(  (   (  n*(np.sum(v_hz**2))  )   -    (sum_hz)    )     /  (n*m*(n-1)*(m-1)) )
MSN_v = sqrt(  (   (  n*(np.sum(v_v**2))  )   -    (sum_v)    )     /  (n*m*(n-1)*(m-1)) )


print(f"mean square error for {a} (HZ) : ",MSN_hz*3600)
print(f"mean square error for {a} (v) : ",MSN_v*3600)