from bs4 import BeautifulSoup, Comment

fIn = open('globoSearch.xml','r')
soup = BeautifulSoup(fIn,"lxml")
print(len(soup.find_all('article')))

# el = soup.select('result_body')
# print(el[0].findChildren()[0])
