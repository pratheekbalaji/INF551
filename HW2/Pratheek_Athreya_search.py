import sys
import re
from lxml import etree
def search (arg1,arg2,words):
    f_arg1 = open(arg1) # opening file1
    arg1 = etree.parse(f_arg1) # getting element tree
    f_arg2 = open(arg2) # opening file2
    arg2 = etree.parse(f_arg2) # getting element tree

    d = {} # dictionary to store ids and attributes
    res =set() # to print only the common keywords
  
    result_xml = etree.Element('results') # creating root for our result
    for word in words:
        word = word.lower()
        temp = arg2.xpath('//keyword[@word="{}"]'.format(word)) # using xpath to get the attribute i.e the keyword which is stored as attribute with tag='word' 
        if len(temp)!=0:
            temp =temp[0].attrib['word']
        
        lst = arg2.xpath('//keyword[@word="{}"]/attribute'.format(word)) # getting the children of the particular keyword (attributes containing keyword)
        for values in lst:
            if temp not in d:
                d[temp] = [(values.attrib['book_id'],values.text)] # to store the id and corresponding attribute 
            else:
                d[temp].append((values.attrib['book_id'],values.text)) # if the key is already present
    a =set(d) # set to get only the books having common keywords
    flag = 1
    for key in d:
        if flag:
            res =set(d[key])
            flag = 0
        else:
            res =res.intersection(set(d[key]))  # taking only the common keys i.e. to return attributes having common keywords
    e= {} # dictionary to group all keys with their corresponding attributes
    for k,v in res: # to ensure that all attributes of an id are under the same tag
        e.setdefault(k,[k]).append(v)
    lst = list(map(tuple, e.values())) # converting to a list
   
    
    for values in lst:
        
        child = etree.SubElement(result_xml,'book',id=values[0])
        for i in range (1,len(values)):
            result_xpath = arg1.xpath('//book[@id="{}"]/{}'.format(values[0],values[i]))
            for val in result_xpath:
                etree.SubElement(child,values[i]).text = val.text
    
    
    return result_xml
    
        
       
   
if __name__ == '__main__':
    if (len(sys.argv)<5):# if user does not pass an input
        print ('Usage python filename xml_file_name_input xml_file_output keyword ')
        sys.exit(1)
    lst =filter(None,re.split("[, \-!?:#$\.\@&\()\,=\+\n]+",sys.argv[3])) # removing all punctuations
    result =search(sys.argv[1],sys.argv[2],lst)
    doc = etree.ElementTree(result)
    doc.write(sys.argv[4],xml_declaration=True,encoding='utf-8',pretty_print=True) # writing result to output file
    
        