"""
#This script retrieves data from the atla.avatarspirit index of transcripts
#and turns it into a python array. It's not that perfect, but at least, I could achieve lots of labour-saving.
"""
from requests import *
from bs4 import BeautifulSoup

def siblings(btag):
	"""
	HTML scout of one <b> tag siblings
	"""

	#Content next to <b> tag
	x = btag.next_sibling 
	
	#Looping till we run into next <br> tag
	arr = ''
	while (len(x) > 0):
		#If it's an <i> tag, only retrieve its content. 
		try:
			arr += str(x.text).strip()
		#Otherwise, keep it up
		except AttributeError:
			arr += str(x).strip() 
		x = x.next_sibling
	return arr

def getcontent(page, fptr):
	"""
	Transcripts parser and retriever
	"""
	blockq = page.find('blockquote')
	btags = blockq.find_all('b')

	#Retrieving contents next to <b> tags pairs
	for x in range(0, len(btags), 2):
		try:
			arr = ''
			arr += "\"" + btags[x].text + siblings(btags[x]) + "\\n\\n"
			if x == len(btags)-1:
				continue
			arr += btags[x+1].text + siblings(btags[x+1]) + "\\n\\n\",\n\n"
		except TypeError:
			continue
		fptr.write(arr)
	

def main():

	#Accesing relevant index webpage
	url = "http://atla.avatarspirit.net/transcripts.php"
	page = get(url)

	#Creating BeatifulSoup object
	soup = BeautifulSoup(page.content, 'html.parser')

	#Getting all the transcript links of each chapter
	content = soup.find(class_= 'content')
	links = content.find_all('a', href=True)

	#Slapping transcripts from each page to some python array
	with open("transcripts.py", "w") as tra:
		tra.write("transcripts = [")
		for k in range(40, len(links)-1):
			link_k = get(links[k]['href'])
			getcontent(BeautifulSoup(link_k.content, 'html.parser'), tra)
		tra.write("]")

if __name__ == '__main__':
	main()