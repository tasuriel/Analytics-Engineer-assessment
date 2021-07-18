import pandas as pd 
import numpy as np
import requests
import sys
import os



#Get working directory as input and set it
if len(sys.argv) == 2:
    working_dir = sys.argv[1]
if working_dir[-1]!="/":
    working_dir = working_dir + "/"
os.chdir(working_dir)



#Read files
vend1 = pd.read_csv("vendor1.csv")
vend2 = pd.read_json('vendor2.json', lines=True)
###Usually, with more time, for something pulled non-locally I would save a local version if one doesn't already exist in a way that pulls anew when there is a new version.
vend3 = requests.get('https://randomuser.me/api/?results=500&seed=0')
vend3 = vend3.json()
vend3 = vend3['results']
vend3 = pd.DataFrame(vend3)




# For vendor 3, expand nested json columns
def expandcol(inputframe, col):
    df = inputframe.copy()
    all_keys = []
    starting_index = df.columns.get_loc(col)+1
    for item in df[col]:
        if type(item) is dict:
            all_keys = all_keys + list(item.keys())
    all_keys = set(all_keys)
    for key in all_keys:
        key_values = []
        for item in df[col]:
            if type(item) is dict:
                if key in item.keys():
                    key_values.append(item[key])
                else:
                    key_values.append(np.nan)
            else:
                key_values.append(np.nan)
        if key not in df.columns:
            df.insert(starting_index, key, key_values)
        else:
            col_name = f"{key}_{col}"
            df.insert(starting_index, col_name, key_values)
    df.drop(col,axis=1,inplace=True)
    return df
###With more time I would first identify any column with items that are dictionaries and then I would have those automatically expanded and check for any more dictionary columns within them
for col in ['name', 'location', 'login', 'dob', 'registered', 'id', 'picture']:
    vend3 = expandcol(vend3, col)
for col in ['street', 'timezone', 'coordinates',]:
    vend3 = expandcol(vend3, col)
#By eyeballing I saw that the street address here is not combined into one column like the other files and the delivery schema. With more time I would put checks for some obvious things to look out for in terms of formatting suggesting that something is not an address, or a phone number, etc.
vend3['street'] = vend3.apply(lambda row: f"{row['number']} {row['name_street']}", axis=1)




#Make schemas of vendor files match
final_cols = ['id',
              'prefix', 'first_name', 'middle_name','last_name', 'suffix',
             'street', 'city', 'state', 'zip_code',
              'email', 'phone_number', 'date_of_birth', 'registration_date']

vend1 = vend1.rename({'vendor1_id':'id',
              'prefix':'prefix', 'first_name':'first_name', 'middle_name':'middle_name',
              'last_name':'last_name', 'suffix':'suffix',
             'addr':'street', 'city':'city', 'state':'state', 'zip':'zip_code',
              'email':'email', 'phone_num':'phone_number',
              'dob':'date_of_birth', 'date_registrated':'registration_date'}
             , axis=1)

vend2 = vend2.rename({'vendor2_id':'id',
              'firstName':'first_name', 'middleName':'middle_name',
              'lastName':'last_name', 'suffix':'suffix',
             'addressLine1':'street', 'city':'city', 'state':'state', 'zipCode':'zip_code',
              'email':'email', 'phoneNum':'phone_number',
              'birthDate':'date_of_birth', 'registrationDate':'registration_date'}
             , axis=1)

vend3 = vend3.rename({'uuid':'id',
              'title':'prefix', 'first':'first_name', 'last':'last_name',
             'street':'street', 'city':'city', 'state':'state', 'postcode':'zip_code',
              'email':'email', 'phone':'phone_number',
              'date':'date_of_birth', 'date_registered':'registration_date'}
             , axis=1)

def matchCols(df):
    for col in df.columns:
        if col not in final_cols:
            df.drop(col, axis=1, inplace=True)
    for col in final_cols:
        if col not in df.columns:
            df[col]=np.nan
    df = df[final_cols]
    return df

vend1 = matchCols(vend1)
vend2 = matchCols(vend2)
vend3 = matchCols(vend3)




#Put the final dataframe together an publish
all_users = pd.concat([vend1, vend2, vend3], ignore_index=True)
all_users.to_csv("all-user.csv", sep=',', index=False)