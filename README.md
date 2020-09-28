## create-Wikipedia-pages-network-using-BFS-crawler
Gets a Wikipedia page URL and creates a network of all pages that link to it at a certain distance.


## introduction
A Wikipedia page consists many links between the various pages on the site. These links can also be viewed as a graph: where the pages are used as **nodes** and the links as **edges**.

When we want to examine the graph to a certain depth, we can use the adapted **BFS** algorithm which is designed to search the graph. Using this algorithm we can reach any of the nodes at a certain distance from the original page. The distance is determined by the **"depth"** parameter, which sets the distance to search for pages from the original page.

In order to identify the links of each page on the web, we must perform a **crawling** process on each of them. In this process we can locate the links the page contains to other Wikipedia pages. In order to get the most relevant links, the algorithm filters only the introduction section of each page. This section of the page is filtered using **BeautifulSoup** to get only the correct links. In order to avoid blocking by the site, between each search there is a wait of one second.

Each link is saved under a python object (**"Link"** class), so it will be easy to retrieve and organize the information about it. Also, the Object handles UTF conversion errors: for example, the page "Bayes's law", display as "Bayes%27s law". source for conversions dictionary from: [utf8-chartable](https://www.utf8-chartable.de/). The code exports all of these links to a single CSV file so that it is convenient to explore and use afterwards.

Also, the code allows the creation of a **networkx graph**, based on the links we found. The graph adds its name to each central node so that the dominant pages on the network can be discerned. In order to find the main nodes we will use the networkx **HITS** algorithm. Then, we will attach its name to each Node only if it indeed relatively central in the network (its hub score will be larger than average + standard deviation). output example:

![example](https://github.com/EtzionData/create-Wikipedia-pages-network-using-BFS-crawler/blob/master/Output/Michelangelo%20network%20graph%20for%20depth%3D2.png)

**Note:** Due to the delay of the crawling process, for **depth** greater than 3, the runtime of the code may be extremely long

## libraries
The code uses the following libraries in Python:

**BeautifulSoup** (bs4)

**requests**

**networkx**

**matplotlib**

**pandas**

Also, **time** & **queue** libraries 


## application
An application of the code is attached to this page under the name: 

**"implementation.py"** 
the examples outputs are also attached here.


## example for using the code
To use this code, you just need to import it as follows:
``` sh
# import
from wiki_crawler import wikipedia_network

# define variables
url = r'https://en.wikipedia.org/wiki/something'  # original page
depth = 2	                                        # search distance from the original page
plot = True	                                      # bool (default: False)

# application
wikipedia_network(url, depth, plot)
```

When the variables displayed are:

**url:** url string of the base Wikipedia page

**bin:** search distance to pages, from the original page

**name:** string which represents the filename of the plot you want to save

## License
MIT © [Etzion Harari](https://github.com/EtzionData)


