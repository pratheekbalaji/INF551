import sys
import re
from lxml import etree

if __name__ == "__main__":
    if (len(sys.argv)!=3):# if user does not pass an input in desired format
        print ('Usage python filename xml_file_name_input xml_file_output ')
        sys.exit(1)
    
    with open(sys.argv[1]) as fobj:
        xml_book = fobj.read()
    root_book = etree.fromstring(xml_book) # getting element tree
    book_dict = {} # a dictionary to store all inverted indexes with their id and tag

    req_attr = ['author','title','genre','description']

    for book in root_book.getchildren():
        
        attribute = book.attrib
        
        for element in book.getchildren():
            if (element.tag) not in req_attr:
                continue
            lst =set(filter(None,re.split("[, \-!?:#$\.\@&\()\,=\+\n]+",element.text))) #removing punctuations and duplicate elements
            for val in lst:
                val = val.lower() # storing indexes in lower cases
                if val not in book_dict:
                    book_dict[val] = [(attribute['id'],element.tag)] # dicitonary keeping track of id and attribute that keyword came from
                else:

                    book_dict[val].append((attribute['id'],element.tag))
                    
    root_index = etree.Element('keywords') # etree for the result xml 
    for key in book_dict:
        child = etree.SubElement(root_index,'keyword',word = key)
        for book_id,attribute in book_dict[key]:
            etree.SubElement(child,'attribute',book_id=book_id).text = attribute
    doc = etree.ElementTree(root_index)
    doc.write(sys.argv[2],xml_declaration=True,encoding='utf-8',pretty_print=True) # writing to the output fi;e
    
    
    
   
        