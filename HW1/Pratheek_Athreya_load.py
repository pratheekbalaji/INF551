import pandas as pd
import json
import requests
import sys
import re

if __name__ == "__main__":
    if (len(sys.argv)!=2):# if user does not pass an input
        print ('Usage python filename csv_file_name')
        sys.exit(1)
    try:
        
        inv_index = dict() # dictionary to store the indexes of facility names
        url ='https://inf551-e666e.firebaseio.com/.json' # the url of firebase database
        data = pd.read_csv(sys.argv[1]) # reads csv file
        required_columns = ['facility_name','score','serial_number'] # list of columns we are interested in the dataframe
        data = data[required_columns] # extracting the required columns
        data.set_index ('serial_number',inplace = True) # indexing serial number
        data = data.to_json(orient = 'index') # converting to json format
        response = requests.put(url,data) # inserting values to the database
        data_dict = json.loads(data) # converting the data to a dictionary
        for key,val in data_dict.items() : #  getting individual key value pair
            temp_list=list(filter(None, re.split("[, \-!?:#$\./'\@&\()\,=\+]+", val['facility_name']))) # selecting whitespace and punctuation as delimiter
            temp_list = [x for x in temp_list if x!='s'] #in case of apostrophe removing 's' from list as apostorphe is a delimiter
            
            for value in temp_list:
                
                value =value.lower() #converting to lower case
                if value not in inv_index:
                    inv_index[value] = [key] # storing index values
                else:
                    inv_index[value].append(key) # adds to the existing values if keyword is already in dictionary
        inv_index = json.dumps(inv_index)

        requests.put('https://inf551-e666e.firebaseio.com/index.json',inv_index) # uploading inverted index to database
        resp = dict (requests.get('https://inf551-e666e.firebaseio.com/index.json').json()) # fetching inverted index from database
        print( json.dumps(resp,indent=2)) # printing in json format
       
    except:
        print('Error Occured')
        
        



