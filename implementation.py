from wiki_crawler import wikipedia_network

url = r'https://en.wikipedia.org/wiki/George_Washington'
wikipedia_network(url, depth = 1,plot = True)
v= input('tt')
url = r'https://en.wikipedia.org/wiki/Harry_Potter_(character)'
wikipedia_network(url, depth = 2,plot = True)

url = r'https://en.wikipedia.org/wiki/Michelangelo'
wikipedia_network(url, depth = 2,plot = True)

url = r'https://en.wikipedia.org/wiki/Mark_Zuckerberg'
wikipedia_network(url, depth = 3)
