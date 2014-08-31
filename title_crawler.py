from bs4 import BeautifulSoup
import urllib2

def get_file_content(file_name):
	file_content = open(file_name,'r')

	contents = ''
	for line in file_content:
		contents += line + '\n'
	file_content.close()

	return contents

def get_movie_titles(file_name,index_contents):
	soup = BeautifulSoup(index_contents)

	table = soup.find('table', {'class': 'movietitles'})

	rows = table.findAll('tr')

	file_content = open(file_name,'w')

	for tr in rows:
	    cols = tr.findAll('td')    
	    
	    for col in cols:
	    	link = col.find('a')
	    	if link is not None:
		    	url = link.get('href')
		    	title = link.getText()
		        file_content.write(title + "||" + url + '\n')
	file_content.close()

def main():

	contents = get_file_content('index_page.txt')			        
	get_movie_titles('titles.txt',contents)

if __name__ == '__main__':
	main()