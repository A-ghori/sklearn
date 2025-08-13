
import pandas as pd ;

# Sample Dataset Making 
data = {
    'buyer' : ['ali', 'noor', 'wajid' , 'karim'],
    'fruits' : ['apple','mango', 'orange' , 'banana'],
    'gender' : ['male','male','female','male'],
    'value': [2,3,4,4]
}

df = pd.DataFrame(data);
df.to_excel('ondata.xlsx', index=False)
print('Excel ready hai tera');

# read excel file 
df2 = pd.read_excel('ondata.xlsx')
print(df2)