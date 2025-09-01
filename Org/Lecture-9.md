---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.17.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
## Dashboards

In our previous lecture (lecture 8), we have seen how to add some interactivity to your table and your plots. Now, imagine that you are working on your project, and that you already have some preliminary results that you want to share with a team of colleagues working on the same project, or with an institution/an organisation supporting your project, or even to address non-technical readers. For this, you can use a simple dashboard in which you sum up the essential results of your preliminary work. 

In order to deploy such a dashboard, you will need to install the following utilities: 

  1. a jupyter lab server, which is serving notebooks (like this one) on your own workspace: 
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}}
#pip3 install jupyterlab
```

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
  2. an application for your dashboard -- in this example, we are using the simple _voila_ dashboard utility because it is simple to setup and it offers basic dashboard functionalities:
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}}
#pip3 install voila
```

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
  3. in order to have a better layout for our voila-dashboard, we install also the gridstack and the voila-vuetify templates like this:
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}}
#pip3 install voila-gridstack voila-vuetify
```

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
  4. finally, to enable conversions of your dashboard into other formats (like PDF f.ex.), you can also install the nbconvert utility like this: 
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}}
#pip3 install nbconvert
```

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
  5. troubleshooting possible old packages -- as _voila_ develop at quick pace, it is possible that you encounter errors by installing it, coming from dependencies that are too old. In order to update voila and its dependencies, you can run the following: 
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}}
#pip3 install jupyter-book myst-nb nbclient voila nbinteract nbformat --upgrade
```

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
Now, you can run jupyter lab as a standalone server on your computer by typing:
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}}
#jupyter lab
```

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
in a terminal or a windows cmd window. Your Internet-browser will be opened at the start page of jupyter lab, and you will have the possibility to create an ipynb notebook file which will be your dashboard. Let us create an example dashboard from the data that we have used in our lecture 8: 

  1. go to 'File', 'New' and select 'Notebook'
  2. at the pop-up window, be sure to select python3
  3. an 'Untitled.ipynb' notebook file is created -- in our example, we rename it to 'Dash9.ipynb'. 
  
While opening your new notebook in jupyter lab, you will see a taskbar with on the left an icon to save your work, then a plus isgn, etc., and on the extreme right of the taskbar a square icon with darkgrey squares in it -- this is the gridstack editor which we will use to create our dashboard. You can click on it in your notebook, and we will place some of the information taken from our lecture 8 in order to construct our dashboard (see our example 'Dash9.ipynb').
<!-- #endregion -->

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
### First import the libraries

First, we import into our dashboard the libraries that we need to construct our tables and plots. We import the libraries for the static plots and tables, and also the one needed to implement some interactivity. In 'Dash9.ipynb', we make two cells in order to render the differences between these libraries, but you could paste them into one cell, too. 

The second step is to customize our file 'Dominant_Topics_ENG_2.csv', in order to have a table with more explicit content and appropriate sort keys. Run all cells in your notebook in order to be sure that you have the appropriate table. Now, we have everything needed to make our dashboard.
<!-- #endregion -->

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
### Table -- Show your dataframe

The first element we would like to show in our dashboard is our dataframe, and we would like to enable the audience to sort it by the value of the topics. In our lecture 8, we have some code for that presentation, so let us take it into our dashboard. This were the following lines of code: 
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}}
# Widget to filter table by topic value
#@interact
#def show_articles(column=['Topic_0', 'Topic_1', 'Topic_2', 'Topic_3', 'Topic_4'], value=(0, 1, 0.05)):
#    return df_eng.loc[df_eng[column] > value]
```

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
Let us paste them into our 'Dash9.ipynb' file -- take the cell with the mouse, and drag-drop it to the gridstack editor. Write a title in another (Markdown) cell, and paste it above your table. Now you see a title and after that, your table with the interactive properties that we have coded in our lecture 8. You as well as the audience using your dashboard will be able to change the topic or / and the value of them to filter your dataset. Let us do the same with a plot. 
<!-- #endregion -->

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
### Plot -- Show first results

We want to show a plot in which the values are aggregated, letting the audience see the multiple factors of our dataset, and letting it interact with them. For this, we use the code or our cell 11 in our lecture 8, to which we add the following line from our cell 10 in order to display the years correctly, and we add it just after the call to the plotly express library (see our file 'Dash9.ipynb'):
<!-- #endregion -->

```python extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}}
#df_eng2["Year"] = df_eng2["Year"].astype(int)
```

<!-- #region extensions={"jupyter_dashboards": {"activeView": "grid_default", "views": {"grid_default": {"col": null, "height": 2, "hidden": true, "row": null, "width": 2}}}} -->
We now can drag and drop this cell to our dashboard. We first write a title for this plot in a cell, drag-drop this title to the dashboard, then drag-drop the cell with the code of our plot. 
<!-- #endregion -->

### Troubles with voila and gridstack

Depending on the version of the widgets, you can quickly get into troubles using the voila gridstack template, f.ex. at the time of writing, plotly plots won't be shown at all in the dashboard. A workaround is to use the voila rendering without the gridstack template, by clicking on the blue-yellow circle icon which is the on the right of the drop-down menu where you can select the formatting of your cells (Markdown, Code or Raw). 


### Web-app

Another solution to avoid hunting bugs in the interplay between jupyter lab, the voila application and the widgets and jupyter extensions, you simply could use a free public service like f.ex. mybinder.org which target the notebook in which you have written your presentation.

For that, you first need to edit a file called 'requirements.txt' -- you can find mine in this repository. In this file, you have to list down all the libraries that your notebook is needed in order to be properly reconstructed by binder. If you look at mine, I have the name of the library, two equal signs, and finally the version of my library. In order to find your installed libraries in python with the version number, you can type in a terminal window (cmd window in windows) the following: 

```python
#pip3 list
```

This code output all packages installed in your python with their version number. You have to read the list and pick up the libraries and its version numbers corresponding to the ones which you are using in your dashboard.

Another requirement is to have a github, a gitlab or another account in relation to mybinder in order for binder to scan the files in this account -- or optionally one of the file (your dashboard in our example) in this account. Then, you just have to make your account 'public' (and not 'private'), for example just for the time you want to share your dashboard, making it 'private' again after this time.

Having all these elements, you can go to mybinder.org, input the path to your online account and give the name of your dashboard, and it will be published online, for other people to see what you have achieved. You will be given an URL of your dashboard online that you can distribute to others.

Such web-apps are also an interesting way to turn your dashboard into a presentation, f.ex. if you have to give a talk at a conference and don't want to carry everything with you. 

#### Web-app -- Streamlit as alternative to voila

Another interesting way to build a Web-app is to use the python library streamlit. You can install this library -- here for python3 -- using the following command:

```python
#pip3 install streamlit
```

Streamlit is an easy way to display nice boards at low cost as an application. I have saved my demos of a streamlit basic app (capp.py) and a streamlit multipage app (mcapp.py) with comments in order for you to understand the basics -- how to layout your app, and how to display several elements such as the table of your data, different graphical representation of the data as well as some comments (all in German -- don't be afraid, I shall translate the content of the app for you in our course). 

Combine with the cloud service of streamlit and your own github repository, you can link streamlit to your repository in order to publish your app (even if your repository on github is a private one) to the world. You will get an Internet link that you can distribute to others in order to show your first results. Don't forget the requirements text file that streamlit needs in order to build your container with your app -- this is exactly the same file that you need for binder, so you don't have to write several files for your app if you just want to publish a voila notebook on mybinder or if you want to publish a streamlit app. 

Streamlit has a lot of possibilities, from single page apps to multipage apps, and it can be used not only for apps, but also f.ex. to turn tutorials into apps and distribute them on the streamlit cloud. It could be a good replacement for notebooks for example, adding interactivity to your projects. 

To run one of the two apps with streamlit on your computer, just type the following in a terminal window on the command line:

```python
#streamlit run capp.py
```

capp.py will be opened in your favorite browser and you can see the result of this tiny demo as it were online.

**Your turn***: if you run capp.py, you will see a problem -- what is the problem in question and how would you solve it?


## Network of topics

To make a useful presentation of your topic analysis, you can also opt for a network graph, introducing to the relationships between your topics and your case. Let us come back to our data 'Dominant_Topics_ENG_2.csv', and to our table in the form of a pandas dataframe 'df_eng2'.

```python
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = [10, 6]
# Set up with a higher resolution screen (useful on Mac)
%config InlineBackend.figure_format = 'retina'
import pandas as pd
df_eng = pd.read_csv('Dominant_Topics_ENG_2.csv')
# First step -- rename columns
df_eng.rename(columns={ df_eng.columns[0]: "Articles" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
# Second step -- drop the column of the dominant topics
df_eng.drop('Dominant_Topic_NMF', axis=1, inplace=True)
# Third step -- create separate columns for title of newspapers and year of publication
df_eng['Year'] = df_eng['Articles']
df_eng['Newspaper'] = df_eng['Articles']
# Fourth step -- set years of publication as int variables
df_eng['Year']= df_eng['Year'].map(lambda x: str(x)[0:4])
df_eng['Year'].astype(int)
# Fifth step -- shorten the newspapers' names in the newspaper column
df_eng['Newspaper']= df_eng['Newspaper'].map(lambda x: str(x)[11:14])
# Sixth step -- sort years 
df_eng2 = df_eng.sort_values(by='Year',ascending=True)
# Display our reworked table
df_eng2.head()
```

We can take this data as a base for our network graph. A network graph is basically a graph of the relationships (or edges) between entities (or nodes). In our example, we want to understand the relationships between: 

  1. newspapers' articles and topics
  3. newspapers' articles
  
We can then rework our 'df_eng2' data in order to get the needed data for the network graph, and because we shall use two software in order to plot our data, we will create files that we can use with both of them. Let us first tailor our 'df_eng2' data with the needed information for our network graph. Here, we will: 

  1. fusion our columns 'Newspaper' and 'Year' into a new column 'News' to have short names of cases 
  2. drop the columns 'Year' and 'Newspaper' that we added in the frame of our lecture 8, in order to have more keys to sort our data
  3. drop the column 'Articles' which will be replaced by the column 'News'
  4. shift the column 'News' to the first column
  5. save the result to a . csv file (here a file called 'gephi-data.csv', because we will use it with the gephi software afterwards)

```python
df_eng2["News"] = df_eng2["Year"].astype(str) + '-' + df_eng2["Newspaper"]
df_eng2 = df_eng2.drop('Articles', 1)
df_eng2 = df_eng2.drop('Year', 1)
df_eng2 = df_eng2.drop('Newspaper', 1)
first_column = df_eng2.pop('News')
df_eng2.insert(0, 'News', first_column)
df_eng2.head()
df_eng2.to_csv('gephi-data.csv', index=False)
```

### Parsing the 'gephi-data.csv' file

We parse the 'gephi-data.csv' file in order to get a file that our networking graph application can read. We are using first low-level programming tools in order to extract every relationships in our 'gephi-data.csv' file and to put them comma separated on one line. 

We then use a python script to save in the file 'texttopic.txt' the relationships between texts in the 'News' column and the topics.

Finally, we use low-level programming tools to make out of texttopic.txt an edge file, as well as a node file. Let us go to the code and explain it.

```python
# Python script

csv = open("gephi-data.csv") # open the gephi-data.csv file
columns = csv.readline().strip().split(',')[1:] # read each line and split it at each comma, save the result in a variable columns
file=open("texttopic.txt", "w") # open a file texttopic.txt for writing
for line in csv: # iterate over each line and make a variable tokens and a variable row
    tokens = line.strip().split(',')
    row = tokens[0] 
    for column, cell in zip(columns,tokens[1:]): # iterate for each column and cell over columns and the second elements of tokens
        print ('{},{},{}'.format(row,column,cell)) # formate the result
        s = str('{},{},{}'.format(row,column,cell)) # save the result into a variable s
        file.write(s + "\n") # write the variable s to the file texttopic.txt, jump to next line for each iteration
file.close() # close the file texttopic.txt

# Create nodes and edges from texttopic.txt

!sed '/,0.0/d' texttopic.txt > ttedge_list.txt # use sed to delete null entries, and save the results as ttedge_list.txt
!awk -F',' ' { print $1 "," $1 } ' texttopic.txt | sort | uniq | sed 's/\.txt//' | awk -F',' ' {print $2 "," $1} ' > ttnode_list.txt # make a sorted list of node using the first column of texttopic.txt and save the nodes as ttnode_list.txt
!echo "id,Label" | cat - ttnode_list.txt > ttnode_list.csv # Add the line id,label as first line of the ttnode_list.txt file
!echo "Topic_0,Topic_0" >> ttnode_list.csv # add the topics to the node list -- here for Topic_0, and below for the other topics
!echo "Topic_1,Topic_1" >> ttnode_list.csv
!echo "Topic_2,Topic_2" >> ttnode_list.csv
!echo "Topic_3,Topic_3" >> ttnode_list.csv
!echo "Topic_4,Topic_4" >> ttnode_list.csv
!echo "Source,Target,Weight" | cat - ttedge_list.txt > ttedge_list.csv # Same as above with other labels added to ttedge_list.csv file
```

## Making our network graph in python

Now that we have our nodes and edges files, we can do a network graph with python and within this notebook, which is useful for a presentation from the notebook directly. In order to do this, we are using pyvis and also networkx in the background of pyvis, which enable us do display nice graphs -- in my view nicer than using networkx alone. If you don't have pyvis and networkx installed, you can install them with pip, like this: 

pip3 install pyvis networkx

```python
from pyvis.network import Network as net
import networkx as nx

med_net = net(height='750px', width='75%', bgcolor='#222222', font_color='white', notebook = True, directed=False) # give some cosmetic parameters for the graph
med_net.barnes_hut() # use an algorythm for the shape of the graph
med_data = pd.read_csv('ttedge_list.csv') # take our ttedge_list.csv file to plot the graph

# Define the variables corresponding to the columns of the ttedge_list.csv file

sources = med_data['Source']
targets = med_data['Target']
weights = med_data['Weight']

# Zip the three variables above into a adge_data variable

edge_data = zip(sources, targets, weights)

# Iterate over the edge_data variable in order to plot the departure nodes (src), the arrival nodes (dst) and the edge between them (w); add them to the graph (med_net)

for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]

    med_net.add_node(src, src, title=src)
    med_net.add_node(dst, dst, title=dst)
    med_net.add_edge(src, dst, value=w)

neighbor_map = med_net.get_adj_list() # get a map of the neighbor -- the nodes which are near from oneanother

# add neighbor data to node on hover -- when you move the mouse on the node, you will see the nodes related to it
for node in med_net.nodes:
    node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
    node['value'] = len(neighbor_map[node['id']])

#med_net.show_buttons(filter_=True) # if you want to use the buttons enabling to modify the parameters of the graph
med_net.show('med.html')
```

Now, you have a network graph of your topic model analysis, and it is an interactive one that you can personalize, and which have been saved as an independent html file (med.html). 

**Please note**: we are not using other facilities of network graphs analysis, since we are not performing a network analysis in the proper sense of this expression. We are using such tools in order to display a weighted view of our results all together, directly using the results of our topic analysis. So, in our case, network software are used in order to better our presentation of the results, and not as an analytical tool in itself.


## Gephi -- standalone solution

Gephi is unfortunately no more actively developed, but there are plans to develop it further. In the meantime, you can download the [free gephi](https://gephi.org/users/download/) software which gives a standalone solution to plot beautiful network graphs -- at least in my view -- based on the files that we have generated from our texttopic.txt file. How do you do that? This is what I want to show you in our course, and do it with you in presence, instead of in this notebook. 


## Other alternatives

You are not forced to use the software mentioned in this notebook, as there are other ones that could better suit your need taken into account that you provide the skills in order to run these other software. For example, instead of using voila for your dashboard, you could also use [dash plotly](https://dash.plotly.com/) which is a python software enabling you to output interactive graphs based on python and html. Provided that you master some html scheme, this could be a better choice for your dashboarding tasks.

The same applies to network graphs utilities. If you want impressive aesthetic graphs, Gephi provides a nice interface which is less involving for the user -- you don't need specific knowledge in network graphs in order to quickly make nice graphs. Pyvis is a bit more demanding, as is [cytoscape](https://cytoscape.org/) which is more tailored to natural sciences. In the same register, you could also use the [graphia](https://graphia.app/) application which is fast and offers 3D views of your network of topics, even if its layout and export capabilities are limited at the moment.
