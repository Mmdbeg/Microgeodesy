# +-+-+-+-+-+-+-+-+-+-+-+-+-+- this code , correct vertical angles refraction +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
from func_dep import *
# +-+- convert dms angles to decimal +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- 


# +-+-Load the Excel file +-+-+-+-+
file_path = 'OBSERVATIONS_ref.xlsx'
df = pd.read_excel(file_path)

for i in range(len(df)):

    df.loc[i,'V_decimal'] = dms_to_decimal(index(df,i,'V')) 
    df.loc[i,'V_corrected'] = v_corrector(index(df,i,'V_decimal'),index(df,i,'corrected_d'),0.13)
    #print(f"{abs(index(df,i,'V_decimal')-index(df,i,'V_corrected'))}" ,'\n')
    df.loc[i,'proj_d'] = proj(index(df,i,'V_corrected'),index(df,i,'corrected_d'))
    #print(index(df,i,'proj_d'))


# +-+- Save to new Excel file +-+-+-+-+-+-+-
df.to_excel('v&d_cor_and_proj.xlsx', index=False)
