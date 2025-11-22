import pandas as pd
import math as m 
from distance_cor import *
# Load the data from Excel files
file_path = 'OBSERVATIONS_ref.xlsx'
df = pd.read_excel(file_path)

file_path1 = 'int_CORD.xlsx'
INT_CORD = pd.read_excel(file_path1)

# Loop through each row in the df and match 'to' column with 'to' in INT_CORD
for i in range(len(df)):
    for j in range(len(INT_CORD)):
        if df.loc[i, 'TO'] == INT_CORD.loc[j, 'POINT']:  # Matching 'to' values
            df.loc[i, 'target_h'] = INT_CORD.loc[j, 'Z(m)']  # Assigning corresponding 'Z(m)' value to 'target_h'
            #print(df.loc[i, 'target_h'] )

h_bar = 2269.92048 # mean z in which all 2d distances are going to prject to 
for i in range(len(df)):
   df.loc[i,'proj_d(mean_z)'] = index(df, i, 'proj_d') * (6371000+h_bar)/(6371000+(index(df, i, 'target_h')+index(df, i, 'target_h'))/2)
   #print(index(df, i, 'proj_d(mean_z)'))

# +-+- Save to new Excel file +-+-+-+-+-+-+-
df.to_excel('obs_with_projected_d_to_mz.xlsx', index=False)
