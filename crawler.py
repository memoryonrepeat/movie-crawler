from imdb import IMDb
from collections import Counter
import urllib2
import urllib
import json
import requests

def write_sorted_keywords(file_name,summary,movie_data,title,to_write):
	sorted_keywords_file = open(file_name,'a')

	counter = Counter()
	for key in movie_data['keywords']:
		if summary.count(key)>0:
			counter[key] = summary.count(key)

	title_keys = title.split(' ')
	for key in title_keys:
		key = key.lower()
		counter[key]=10

	for (key,value) in counter.most_common(20):		
		to_write +='(keyword (word \"'+str(key)+'\") (movieName \"'+title+'\") (number '+str(value)+'))\n'
	to_write += '\n'	
	sorted_keywords_file.write(to_write)
	sorted_keywords_file.close()

def get_pure_summary(file_name):
	file_content = open(file_name,'r')
	count=0
	summary=''
	for line in file_content:				
		if line.find('<p>')!=-1 and line.find('<p><')==-1:	
			line = line.replace('<p>','').replace('</p>','').replace('&quot;','').replace('&nbsp;','').replace('&amp;','').replace('&rsquo;','').replace('&ldquo;','').replace('&rdquo;','')
			summary += line			
			
	file_content.close()
	return summary

def write_to_file(file_name,to_write):
	file_content = open(file_name,'w')
	file_content.write(to_write)
	file_content.close()	

def main():

	i = IMDb('http')
	titles = open('titles.txt','r')
	
	wrong_files = open('wrong_files.txt','a')

	for line in titles:

		to_write = ''
		
		(title,url) = line.split('||')
		url=url.rstrip('\n')	

		parameters = {'t':title}	
		response_keywords = requests.get("http://www.omdbapi.com/?", params=parameters)
		
		if 'imdbID' not in response_keywords.json():
			wrong_files.write(title + '//Wrong title'+'\n')
			continue

		movie_id = response_keywords.json()['imdbID']	
		movie_data = i.get_movie(movie_id[2:], info='keywords')	
		
		if movie_data.get('keywords',None) is None:
			wrong_files.write(title + '//Keywords not exist'+'\n')
			continue

		print title
		
		to_write += '(movie (movieName \"'+title+'\"))\n'
		
		response = urllib2.urlopen("http://www.themoviespoiler.com/"+url)
		response_summary = response.read()		

		write_to_file('site_content.txt',response_summary)

		summary = get_pure_summary('site_content.txt')				
		
		write_sorted_keywords('sorted_keywords.txt',summary,movie_data,title,to_write)


if __name__ == '__main__':
	main()