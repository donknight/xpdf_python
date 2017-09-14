import os
import sys
import re
import subprocess



def countPages(filename):  
	''' Counts number of pages in PDF '''

	# NOTE: Currently does not work 100% of the time
	rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
	data = open(filename,"r", encoding = "ISO-8859-1").read()
	return len(rxcountpages.findall(data))

def to_text(file_loc, page_nums=True, options=()):
	''' Converts PDF to text

	Args
	- - - - - - -
		file_loc: path to pdf document, string
		page_nums: whether to insert page numbers into document, boolean
		options: allows the addition of any of the normal options accepted by pdftotext, tuple of strings
	
	Returns
	- - - - - - -
		text: extracted text from pdf document, string
		actual_count: estimated number of pages for pdf document, integer
	
	'''

	# Determines location of file
	if os.path.isabs(file_loc):
		full_file_loc = file_loc
	else:
		cd = os.getcwd()
		full_file_loc = os.path.join(cd, file_loc)

	path, file = os.path.split(full_file_loc)
	saved_file = os.path.join(path, os.path.splitext(file)[0] + '.txt')

	text = ''
	actual_count = 0

	# If page numbers are to be inserted
	if page_nums:
		num = countPages(full_file_loc)
		# Accounts for errors occuring in countPages function
		if num == 0:
			num = 100
	else:
		# accounts for not adding page numbers by allowing the loop to go just one bulk action
		num = 1
		actual_count = countPages(full_file_loc)  # try and provide a page estimate on bulk runs

	for i in range(num):
		actual = i + 1
		opt = options
		if page_nums:
			opt += ('-f', str(actual), '-l', str(actual))

		# Calls xpdf
		subprocess.call(['pdftotext', *opt, full_file_loc])

		# Opens file saved to disk, ensures it will always close when done
		with open(saved_file, 'r', encoding='ISO-8859-1') as file:
			t = file.read()
		# If the page is blank, it is not a real page
		if t == '':
			continue
		if page_nums:
			actual_count += 1
		# Add text and page count to existing string, or not it not page_nums
		if page_nums:
			text += '***Page {}*** {}'.format(actual, t)
		else:
			text = t

	# Remove file saved to disk
	os.remove(saved_file)

	return text, actual_count
	
def extract_images(file_loc):
	''' Extracts images from PDF document

	Args
	- - - - - - -
		file_loc: path to pdf document, string
	
	Returns
	- - - - - - -
		image_locs: location of saved images files, list
	
	'''
	# Determines location of file
	if os.path.isabs(file_loc):
		full_file_loc = file_loc
	else:
		cd = os.getcwd()
		full_file_loc = os.path.join(cd, file_loc)

	subprocess.call(['pdfimages'])
