#!/usr/bin/env python3

from KafNafParserPy import *
import sys
import re

with open(sys.argv[1]) as f:
    content = f.readlines()
 
date_pattern='^\d{4}[-/]\d{2}[-/]\d{2}$'
my_parser = KafNafParser(None, type='NAF')  
raw = ''
outputdir = sys.argv[2]
outputfile = '%stest.naf' % outputdir
entity_counter = 0 
mycount=0
my_date=''
dct_found=False
for item in content:
	if len(item) < 2:
	#	print item.rstrip(), " ", len(item)
		continue
	if '-DOCSTART-' in item:
		if len(raw) > 2:
			# Create the raw text layer 
			rawlayer = my_parser.set_raw(raw)
			raw = ''
			offset = 0
			# print the NAF file
			my_parser.dump(outputfile)
	#	print "new document", item 
		parts = item.split(" ")
	#	print parts[1][1:]
		outputfile = '%s%s.naf' % (outputdir, parts[1][1:])
		
		# Init KafNafParserobject
		my_parser = KafNafParser(None, type='NAF')
		my_parser.root.set('{http://www.w3.org/XML/1998/namespace}lang','en')
		my_parser.root.set('version','v3')	
    
    	# Set the header
		header = my_parser.get_header()
		if header is None:
			#Create a new one
			header =  CHeader()
			my_parser.set_header(header)
		
		my_file_desc = header.get_fileDesc()
		if my_file_desc is None:
    		#Create a new one
			my_file_desc =  CfileDesc()
			header.set_fileDesc(my_file_desc)
        
			#Modify the attributes
			my_file_desc.set_title(parts[1][1:])
			my_file_desc.set_filename(parts[1][1:])
			my_file_desc.set_creationtime(my_date)
		dct_found=False
		my_public=header.node.find('public')
		#my_public=None
		if my_public is None:
                #Create a new one
			my_public = Cpublic()
			header.node.insert(0, my_public.get_node())

                        #Modify the attributes
			my_public.set_uri('http://example.com/aida/%s' % parts[1][1:])
			my_public.set_publicid(parts[1][1:])
	else:
		elements = item.split("\t")
		elements[0] = elements[0].rstrip()
		raw = raw + elements[0] + " " 
		if not dct_found and re.match(date_pattern, elements[0]):
			header = my_parser.get_header()
			my_file_desc =  header.get_fileDesc()
			my_file_desc.set_creationtime(elements[0])
			my_date=elements[0]
			dct_found=True
print(mycount)
print(entity_counter)
