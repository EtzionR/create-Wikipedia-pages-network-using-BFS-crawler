from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
from time import sleep as wait
from queue import Queue
import networkx as nx
import pandas as pd
import requests

WIKI = r'https://en.wikipedia.org'
PREFIX = len(WIKI+'/wiki/')
UTF={'%21' : '!', '%22' : '"', '%24' : '$', '%25' : '%', '%26' : '&', '%27' : "'", '%2F' : '/',
     '%28' : '(', '%29' : ')', '%2A' : '*', '%2B' : '+', '%2C' : ',', '%2D' : '-', '%2E' : '.',
     '%3C' : '<', '%3D' : '=', '%3E' : '>', '%3F' : '?', '%40' : '@', '%5B' : '[', '%5D' : ']',
     '%5E' : '^', '%5F' : '_', '%60' : '`', '%7B' : '{', '%7C' : '|', '%7D' : '}', '%7E' : '~',
     '%C2%A1' : '¡', '%C2%A2' : '¢', '%C2%A3' : '£','%E2%80%93':'-',
     '%C2%A4' : '¤', '%C2%A5' : '¥', '%C2%A6' : '¦', '%C2%A7' : '§', '%C2%A8' : '¨',
     '%C2%A9' : '©', '%C2%AA' : 'ª', '%C2%AB' : '«', '%C2%AC' : '¬', '%C2%AD' : '­',
     '%C2%AE' : '®', '%C2%AF' : '¯', '%C2%B0' : '°', '%C2%B1' : '±', '%C2%B2' : '²',
     '%C2%B3' : '³', '%C2%B4' : '´', '%C2%B5' : 'µ', '%C2%B6' : '¶', '%C2%B7' : '·',
     '%C2%B8' : '¸', '%C2%B9' : '¹', '%C2%BA' : 'º', '%C2%BB' : '»', '%C2%BC' : '¼',
     '%C2%BD' : '½', '%C2%BE' : '¾', '%C2%BF' : '¿', '%C3%80' : 'À', '%C3%81' : 'Á',
     '%C3%82' : 'Â', '%C3%83' : 'Ã', '%C3%84' : 'Ä', '%C3%85' : 'Å', '%C3%86' : 'Æ',
     '%C3%87' : 'Ç', '%C3%88' : 'È', '%C3%89' : 'É', '%C3%8A' : 'Ê', '%C3%8B' : 'Ë',
     '%C3%8C' : 'Ì', '%C3%8D' : 'Í', '%C3%8E' : 'Î', '%C3%8F' : 'Ï', '%C3%90' : 'Ð',
     '%C3%91' : 'Ñ', '%C3%92' : 'Ò', '%C3%93' : 'Ó', '%C3%94' : 'Ô', '%C3%95' : 'Õ',
     '%C3%96' : 'Ö', '%C3%97' : '×', '%C3%98' : 'Ø', '%C3%99' : 'Ù', '%C3%9A' : 'Ú',
     '%C3%9B' : 'Û', '%C3%9C' : 'Ü', '%C3%9D' : 'Ý', '%C3%9E' : 'Þ', '%C3%9F' : 'ß',
     '%C3%A0' : 'à', '%C3%A1' : 'á', '%C3%A2' : 'â', '%C3%A3' : 'ã', '%C3%A4' : 'ä',
     '%C3%A5' : 'å', '%C3%A6' : 'æ', '%C3%A7' : 'ç', '%C3%A8' : 'è', '%C3%A9' : 'é',
     '%C3%AA' : 'ê', '%C3%AB' : 'ë', '%C3%AC' : 'ì', '%C3%AD' : 'í', '%C3%AE' : 'î',
     '%C3%AF' : 'ï', '%C3%B0' : 'ð', '%C3%B1' : 'ñ', '%C3%B2' : 'ò', '%C3%B3' : 'ó',
     '%C3%B4' : 'ô', '%C3%B5' : 'õ', '%C3%B6' : 'ö', '%C3%B7' : '÷', '%C3%B8' : 'ø',
     '%C3%B9' : 'ù', '%C3%BA' : 'ú', '%C3%BB' : 'û', '%C3%BC' : 'ü', '%C3%BD' : 'ý',
     '%C3%BE' : 'þ', '%C3%BF' : 'ÿ'}

class Link:
    def __init__(self,head,tail,level):
        self.head = head if '%' not in head else self.fix_utf(head)
        self.tail = tail if '%' not in tail else self.fix_utf(tail)
        self.level= level

    def get_tpl(self):
        return (self.head, self.tail,self.level)

    def fix_utf(self,string):
        for key in UTF:
            if key in string:
                string = string.replace(key, UTF[key])
        return string

def link_valid(seq):
    if seq==None:
        return False
    if ':' in seq or ';' in seq or '//' in seq or '#' in seq:
        return False
    if '/wiki/' in seq:
        return True

def page_parser(url):
    links= set()
    page = requests.get(url).text
    soup = bs(page[:page.find("<h2>")], 'html.parser')
    head = soup.find('div',{'class':'mw-parser-output'})
    for table in head.select('tbody'):
        table.decompose()
    for hyper in head.find_all('a'):
        link = hyper.get('href')
        if link_valid(link):
            links.add(WIKI+link)
    wait(1)
    return links

def bfs_crawler(url, depth):
    queue, links, memory = Queue(),[],{url}
    childs = page_parser(url)
    for child in childs: queue.put(Link(url,child,1))
    while queue.empty()==False:
        link = queue.get()
        links.append(link)
        if link.level>=depth:
            while queue.empty()==False: links.append(queue.get())
            break
        elif link.tail not in memory:
            childs = page_parser(link.tail)
            memory.add(link.tail)
            for child in childs:
                queue.put(Link(link.tail, child, link.level+1))
    return links

def links_to_df(links):
    return pd.DataFrame([link.get_tpl() for link in links],
                        columns=['head', 'tail', 'level'])

def calculate_hubs(graph):
    hubs = nx.hits(graph, tol=0.1)[0]
    h_avr= sum(hubs.values()) / len(hubs)
    h_sd =(sum([(h_vlu - h_avr)**2 for h_vlu in hubs.values()]) / len(hubs))**(0.5)
    return {key: key if hubs[key] > (h_avr + h_sd) else '' for key in hubs}

def create_network(data,depth,name):
    head = [h[PREFIX:] for h in data['head']]
    tail = [t[PREFIX:] for t in data['tail']]
    G = nx.Graph()
    for i in range(len(head)):
        G.add_edge(head[i], tail[i])
    hubs = calculate_hubs(G) if depth>1 else {key:key for key in G.nodes}
    pos_ = nx.spring_layout(G,k=2/len(G.nodes)**0.5)
    plt.figure(figsize=(15, 9))
    nx.draw_networkx(G, pos=pos_,with_labels=False,node_size=10,arrows =True,
                     node_color='blue',edge_color='lightskyblue')
    nx.draw_networkx_labels(G,pos=pos_, labels=hubs, font_size=8)
    plt.axis('off')
    plt.title(f"{name} network graph (for depth={depth})")
    plt.savefig(f"{name} network graph for depth={depth}.png")
    plt.show()

def wikipedia_network(url,depth=2, plot=False):
    name = url.split('/')[-1]

    links= bfs_crawler(url, depth)
    data = links_to_df(links)
    data.to_csv(f'{name} links for n={depth}.csv', encoding='utf-8', index=False)
    if plot: create_network(data,depth,name)
