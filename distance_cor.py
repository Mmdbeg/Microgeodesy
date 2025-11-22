#-+-+-+-+-+-+-+-+-+-+-+-+ this program will add the atmospheric correction to distance observations -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
from func_dep import *

# +-+-Load the Excel file +-+-+-+-+
file_path = 'OBSERVATIONS_ref.xlsx'
df = pd.read_excel(file_path)

# +-+- updating data frame +-+-+-+-
for i in range(len(df)):
    T_iw = index(df, i, 'T.i(w)') # extracting ...
    P_i = index(df, i, 'P.i(mb)') # the dry/wet  - target/instrument ...
    T_td = index(df, i, 'T.t(d)') # pressure...
    T_tw = index(df, i, 'T.t(w)') # and ...
    T_id = index(df, i, 'T.i(d)') # temperture...
    P_t = index(df, i, 'P.t(mb)') # values...

    es_dry_i = 6.112 * exp((17.62 * T_id) / (243.12 + T_id)) # calculating ... 
    es_wet_i = 6.112 * exp((17.62 * T_iw) / (243.12 + T_iw)) # the dry/wet - target/instrument ...
    es_dry_t = 6.112 * exp((17.62 * T_td) / (243.12 + T_td)) # and es ...
    es_wet_t = 6.112 * exp((17.62 * T_tw) / (243.12 + T_tw)) # values ...


    df.loc[i, 'relative_H.i'] = rh(es_wet_i, es_dry_i, T_iw, T_id, P_i) # updating ...
    df.loc[i, 'relative_H.t'] = rh(es_wet_t, es_dry_t, T_tw, T_td, P_t) # data frame ...

    
    ti = (index(df,i,'T.i(d)') + index(df,i,'T.t(d)')) /2 # mean temperture
    pi = (index(df,i,'P.i(mb)') + index(df,i,'P.t(mb)')) /2 # mean pressure 
    rhi = (index(df,i,'relative_H.i') + index(df,i,'relative_H.t')) /2 # mean relative humidity 
    a = 1 / 273.15 # constante
    x =  ((7.5 * ti) / (237.3 + ti) ) + 0.7857 # defining variable

    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- adding data frame , new calculated values +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    df.loc[i,'delta_d(ppm)'] = 286.34 - ( ((0.29525*pi)/(1+a*ti)) - ((4.126*0.0001*rhi*10**x)/(1+a*ti))) # calculading distance correction 
    df.loc[i,'corrected_d'] = index(df,i,'D') + ((index(df,i,'delta_d(ppm)'))/(10**(6)))*index(df,i,'D') # corrected distance
    df.loc[i,'d_correction(mm)'] = ((index(df,i,'delta_d(ppm)'))/(10**(6)))*index(df,i,'D') # each distance correction  


# +-+- Save to new Excel file +-+-+-+-+-+-+-
df.to_excel('obs_with_rh.xlsx', index=False)






