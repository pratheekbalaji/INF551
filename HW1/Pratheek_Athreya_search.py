import requests
import json
import sys
import re
url ='https://inf551-e666e.firebaseio.com/.json' # url of FireBase keys
url_index ='https://inf551-e666e.firebaseio.com/index/' # url of inverted index

def search(lst):
    ''' Returns all matching resturants specified in the keyword'''
    response_json = dict(requests.get(url).json()) #fetching all the records from database
    result = [] # creating a list to store all the keys present in a particular keyword in inverted index
    output ={} # dictionary to store the output values
    for values in lst: # reading the keywords passed
        
        temp = requests.get(url_index+values+'/'+'.json').json() # fetching values of keyword from inverted index
        if temp is None:
            print ('Sorry No Matching Results Found') # the case when keyword is not present
            return
        for val in temp:
            result.append(val) # appending key values to a list
    result_unique = set(result)# removing duplicates
    

    for values in result_unique:
        output[values] = response_json[values] # fetching all the records having the particular key and storing it in a dictionary
    output = json.dumps(output,indent = 4) # concerting to json format
    print (output) # printing the values
    
  
   
if __name__ == '__main__':
    try:
        if (len (sys.argv) !=2): # if user does not pass an argument
            print ('Usage python File_Name searchparameter')
            sys.exit(1)
       
        
        lst =list(filter((None),re.split("[, \-!?:#$\./'\@&\()\,=\+]+", sys.argv[1]))) # removing punctuations
        lst = [x for x in lst if x!='s'] #in case of apostrophe removing 's' from list as apostorphe is a delimiter
            
        
        search(lst) # calling function to search for keywords
        
        
        
        
    except:
        print('Error occured')
        
    
    
