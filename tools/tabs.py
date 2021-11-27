#Extract arrays from c headers
#Attempting to preserve comments

def tables(header):
	"""Find the start of the c array, declared with [].
	Expects one parameter, a string containing the content of the file to read."""
	ct = header.count('[]') #How many tables.
	if ct == 0: return #Woops, nothing to do. 
	idx = 0 #start from the first letter.
	while ct > 0:
		idx = header.index('[]', idx)
		yield idx #start-ish of the table declaration.
		idx += 1 #get ready for next search.
		ct -= 1 #We found 1.

def getTabName(header, index):
	"""Get the name of the table at index from above tables generator.
	Expects the header string and the index of the table."""
	name = header.rindex(' ', 0, index) #start of the name.
	return header[name + 1: index] #the name of the table.

def getTabData(header, index):
	"""Get the table data at index from above tables generator.
	Expects the header string and the index of the table."""
	tabStart = header.index('{', index) + 1 #start of the table, first letter after {.
	tabEnd = header.index('}', tabStart) #last of the array.
	return header[tabStart:tabEnd]

def getComments(header, index):
	"""Get any comments before this table.
	Expects the header string and the index of the table."""
	cend = header.rindex('\n', 0, index) #the start of line.
	cstart = cend
	tmp = cend
	while True: #find start of a comment.
		tmp = header.rindex('\n', 0, cstart - 1)
		if '//' in header[tmp:cstart]:
			cstart = tmp #this is a line with a comment.
		else:
			return header[cstart:cend]

def allTabs(filePath):
	"""return {table name: (comments, data)} for all tables.
	Expects the filename of the header to read."""
	#Its a q&d tool, I should catch exceptions, but this is not for use in production.
	header = filePath.read_text() #see pathlib.Path.
	r = {} #result of this function.
	for i in tables(header):
		r[getTabName(header, i)] = (getComments(header, i), getTabData(header, i))
	return r

