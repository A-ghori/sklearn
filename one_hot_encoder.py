import pandas as pd
df = pd.read_excel('ondata.xlsx')
df.info()

df2=pd.get_dummies(data=df, columns=['buyer','fruits','gender'],dtype=int)
print(df2)


# WITH SKLEARN oneHot Encoder 

# When sparse=True, the encoded output is returned as sparse matrix, while sparse = False return a dense matrix.

from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(dtype=int,sparse_output=False)
df_trans = ohe.fit_transform(df[['buyer','fruits','gender']])
print(df_trans)

cols=ohe.get_feature_names_out()
print(cols)

# print(df_trans)
df3=pd.DataFrame(data=df_trans,columns=cols)
print(df3)