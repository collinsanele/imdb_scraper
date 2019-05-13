import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import time
import io



url = "https://m.imdb.com/chart/moviemeter?ref_=m_nv_mpm"


Movie_Name = []
Imdb_Rating = []
Link = []
Poster_Image = []


def scrape_and_email(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	content = soup.find('section', {'id':'chart-content'})
	for item in content.findAll('h4'):
		mn = item.text.strip()
		Movie_Name.append(mn)		
		
	for item in content.findAll('p', {'class':'h4 unbold'}):
		imdb = item.text.strip()
		Imdb_Rating.append(imdb)
		
		
	for item in content.findAll('a'):
		link = 'http://imdb.com'+ item['href'].strip()
		Link.append(link)
		
		
	for item in content.findAll('img'):
		poster = item['src'].strip()
		Poster_Image.append(poster)
		

	df = pd.DataFrame({"Name":pd.Series(Movie_Name), "Imdb Rating":pd.Series(Imdb_Rating), "Link":pd.Series(Link), "Poster Image":pd.Series(Poster_Image)})
	df = df.loc[0:99, :]
	with io.BytesIO() as buffer:
		writer = pd.ExcelWriter(buffer)
		df.to_excel(writer)
		data =  buffer.getvalue()
		
	msg = MIMEMultipart()
	msg["Subject"] = "Imdb Best Movies"
	msg["From"] = "pycollins2019@gmail.com"
	msg["To"] = "collinsanele@gmail.com"
	msg["Date"] = formatdate(localtime=True)
	text = 'The best movies in imdb'
	msg.attach(MIMEText(text))
	
	part = MIMEBase('application', "octet-stream")
	part.set_payload(data)
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="imdb.xlsx"')
	msg.attach(part)
	
		
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login("pycollins2019@gmail.com", "call4807797")
		smtp.sendmail("pycollins2019@gmail.com", "collinsanele@gmail.com", msg.as_string())
	print("Sent!")
	

scrape_and_email(url)

				




