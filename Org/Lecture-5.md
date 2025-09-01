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

## First steps in topic modeling with MTA

In this lecture, we are making our first steps in the topic modeling of qualitative data using MTA. We will cover it at the example of a sample of articles on nanomedicine published in the Times (London) from 2000 until 2021 that we have downloaded from the database Nexis Lexis. 

In this lecture, we are going through the following steps:

  1. first, based on our lectures 3 and 4, we extend our practice of parsing text data using this new dataset;
  2. second, we explore MTA in order to understand what this program is doing;
  3. third, we perform our first analysis on the Times dataset with MTA
  
At the end of this lecture, you will have a typical general workflow enabling you to do a topic model analysis with MTA easily. Before, just check out our second lecture to be sure that you have all the needed packages to work with MTA.


## Preprocessing and parsing our data

The Nexis Lexis database let you query lot of newspapers' articles, and in this example, we are querying newspapers related to the topic of nanomedicine. This is based on our work on nanotechnologies developed for medicine (Papilloud, Schultze 2022), that we have done mainly at the example of the European nanomedicine. As an introduction to this research, we were interested in the reception of nanomedicine in the newspaper worldwide. As you may know, nanotechnologies have been controversial technologies at the beginning of 2000, and they have attracted the attention of the press which was at the same time fascinated by the possible applications of such technologies in several areas of society, while suspecting that such technologies could also present severe risks due to nanoparticles threatening human health.

Therefore, we wanted to first question if nanomedicine has really made the headlines of the press in the twenty past years, and we wanted to know which themes have been related to the nanomedicine in the press' coverage of such technology. 

### The data of the Times

The Times (London) is one of the newspaper which has been investigated. Nexis Lexis gives you the possibility to save the results of your research in one RTF file, and to download it to your hard drive. We just did that for the articles of the Times on nanomedicine found on this database, and in this lecture, we are working with a sample of it in order to illustrate the first steps in topic modeling with MTA. 

Let us now explore this sample file in more details. This is a single file with nine documents. This file has a structure with following elements. 

  1. a summary of all articles in the file
  2. all the articles of your query with details of the rubric, the author of the article, the body of the article and the date of publication etc.

What we want to do first is to parse this file in order to extract the nine articles as separate files ready to be preprocessed, as we have seen in our first lectures. Let us do it, step by step. 


### First, convert our file to txt

We firstly convert our file to txt. We can use soffice headless to do this:

```python
#!for i in *.rtf; do soffice --headless --convert-to txt:Text "$i"; done
```

If you run this line, you will get a txt copy of your rtf file with the content of the rtf file. Now, we want to extract the content of each article into a new file. We are using the tag 'Body' in our txt file which signalizes the begin of each article. With awk, we construct a program to take the parts of text between two tags 'Body like this, and to save them in files beginning with 'times-1-9.numberofthefile':

```python
#!awk '/Body/{i++}{print > "times-1-9."i}' TheTimes-1-9.txt
```

Now, if you run this line, you will see that awk will take everything in our source text file before, between and after the 'Body' tags. This means that we are also creating useless files -- actually two files times-1-9. and times-1-9.1, the former with the summary of the articles in this rtf document, the later with only some tags (rubrique, author, date) --, that we can remove. At the moment, we have achieve our first goal which was isolating the articles in dedicate files. We can go to the second task, tagging our files. 

### Tag our files with the date of publication

In this example, we would like to see the evolution of the coverage on nanomedicine in time. So we need the information in each file corresponding to the publication date of each article. If you take one of our file containing an article, you will see at the end of this file 'Load-Date' and the corresponding date of publication -- this is the information which we need to tag our files. As we operate on a line, we are writing a program with sed in order to get the publication date. To avoid problems retrieving our publication date, we remove from the files everything which is coming _after_ the tag 'Load-Date':

  1. we create a for loop to operate on our files;
  2. we list all our file containing 'times-1-9' in their filename;
  3. we tell sed to remove all lines after the tag 'Load-Date';
  4. we tell sed to save the new content in a file with same file name, ending with 'new' in order to recognize our new files easily.

```python
#!for i in `ls times-1-9*`; do sed '/Load/q' $i > ${i}.new; done
```

Running this line, you have now new times-1-9.somenumber files in your directory, ending with 'new'. We are using this new cleaned files to get the publication date from the line with the 'Load-Date' tag, and save these lines one after one in a file containing the tag 'Load-Date' and the corresponding dates. For that, we just change our for loop above with: 

  1. sed using the p parameter after the tag /Load/ to take this line only;
  2. the >> operator to save all lines one after one in the file times-dates.

```python
#!for i in `ls times-1-9*.new`; do sed -n '/Load/p' $i >> times-dates; done
```

Now, let us create a file 'Dates-Files-times' to save the name of our files ending with 'new' and after them, their corresponding publication date. To do that, we are using grep which enables us to find the line with the tag 'Load-Date' in each of our 'new' files and to save them in our file 'Dates-Files-times':

```python
#!grep 'Load-Date' times-1-9*.new > Dates-Files-times
```

Running this line, you get a file 'Dates-Files-times' with the following content: 

```
times-1-9.10.new:Load-Date: May 7, 2010
times-1-9.2.new:Load-Date: February 27, 2006
times-1-9.3.new:Load-Date: September 27, 2017
times-1-9.4.new:Load-Date: January 18, 2016
times-1-9.5.new:Load-Date: January 18, 2016
times-1-9.6.new:Load-Date: October 31, 2015
times-1-9.7.new:Load-Date: August 12, 2009
times-1-9.8.new:Load-Date: May 2, 2012
times-1-9.9.new:Load-Date: November 20, 2014
```




We are going to use this file in order to extract some information of it for our preprocessing task. First, we want to save the name of the files in a separate file. We take up awk again, and we write a program that basically prints the first column -- note that we tell awk what are column with the -F switch and the column mark -- in our file 'Dates-Files-times' and save it in another file called 'Filesdatesfig':

```python
#!awk -F":" '{ print $1 }' Dates-Files-times > Filesdatesfig
```

Our file 'Filesdatesfig' has now only the filenames of our 'new' files. We do the same with the date part of our file 'times-dates', taking everything coming after 'Load-Date:', i.e. the day, the month and the year of publication that we save in a file 'Fclean':

```python
#!awk -F":" '{ print $2 }' times-dates > Fclean
```

In the file 'Fclean', we actually need all the information in this file, but in another format that MTA can easily recognized -- basically, we need the year, then the month, then the day separated by a dash, like this: 2020-12-01 for the first December of the year 2020. How to do it?

Let us begin with the easy part, the years. Note that each year is coming right after a comma and a blank space. So, let us take that comma as a delimiter for awk, and let us tell awk to take the column after that comma. Awk will also take the blank space after the comma which we don't want. Let us then pipe the result of awk into a sed program removing blank spaces from this results, and let us save the final result of both awk and send in a new file 'Fyear':

```python
#!awk -F"," '{ print $2 }' Fclean | sed 's/ //' > Fyear
```

### Add a month tag

All right -- we have now a file 'Fyear' with the years without blank spaces. Let us go to the months. 

The months have been written in plain letters, so we have to replace these letters with numbers. We can use sed for this task, telling sed to read each line of the file 'Fclean' and to replace the months in letters with months as numbers. 

Because sed will take all the complete lines, and we just want the months, we send the result of our sed program to awk, telling awk to take only the first column in the sed result, which is our columns with the months turned into numbers.

Finally, as we don't want to overwrite our file 'Fclean', we tell sed to save the results in a new file 'Fmonths'. 

In the following, we give a solution for more than only few month as in the file 'Fclean':

```python
#!sed -e 's/January/01/g' -e 's/February/02/g' -e 's/March/03/g' -e 's/April/04/g' -e 's/May/05/g' -e 's/June/06/g' -e 's/July/07/g' -e 's/August/08/g' -e 's/September/09/g' -e 's/October/10/g' -e 's/November/11/g' -e 's/December/12/g' Fclean | awk -F" " '{ print $1 }' > Fmonths
```

If you now look at the 'Fmonths' file, you will see that we have forgotten to remove the blank space at the beginning of each line -- just let do that using our sed program above

```python
#!sed -i 's/ //' Fmonths # -i is for in place = overwrite the file with the new content
```

But if you look at the Fmonths file, nothing has been changed... Why is it so? 

When you are dealing with text files, as well as with other files, they can come from very different operating systems marking these files differently. Such marks are not visible for you, and sometimes they also remain hidden for the common text editor that take them as if these marks were blank spaces. In our case, we don't have a blank space before each line of our file 'Fmonths', but instead a hidden character. So, how can you delete such hidden character. 

In sed -- but it is also true for other unix low level programs --, you can catch up these character with the dot, which acts as a symbol of any kind of character, even hidden ones. So, let us suppose that we have one (or more) hidden character(s) here; in order to remove it/them, we modify our sed program, telling it to remove any hidden character in our file and, as a cautious measure, to save the result in a file 'fm':

```python
#!sed 's/.//' Fmonths > fm # ^ is for 'begin of line' and here we don't overwrite the file; input -i to overwrite it
```

Our supposition was true -- we had one or more hidden character(s) that we have removed with sed and its character symbol.  


Now that everything is fine, let us paste together our files 'Fyear' and our new file 'fm' in order to get our finale result: 

```python
#!paste -d'-' Fyear fm > Fyearmonth
```

### Add the day tag

We are doing the same for the day tag, that we will add to our file 'Fyearmonth'. First, we take the day tag from the 'Fclean' file with awk, taking the second column in this file which corresponds to the day and saving the days in a 'Fday' file. Caution: we also have to remove the comma at the end of the day, that we don't want to take up in the new file 'Fday' -- as usual, we are using sed to remove this comma on each line:

```python
#!awk -F" " '{ print $2 }' Fclean | sed 's/,$//' > Fday
```

We can afterwards paste the files 'Fyearmonth' and 'Fday' together and save them in the file 'Fyearmonthday', in order to have the final filename for our files:

```python
!paste -d'-' Fyearmonth Fday > Fyearmonthday 
```

Now, we add to each line of our last file 'Fyearmonthday' the general name of the document of the times that we had in our first files containing the articles of our rtf file, which were labeled 'times-1-9' something: 

```python
#!sed 's/$/-times-1-9/' Fyearmonthday > Finaltimes # YOUR TURN -- try to explain the meaning of the sed parameters in this line and what do the line
```

### Your turn -- Make a rename script

We are almost there -- but now, it is your turn. You have the original files and our new file 'Finaltimes' with the new names that you want to use in order to rename our 'times-1-9.x.new' files. How can you combine these files to have a script that you could use in order to rename all 'times-1-9.x.new' files adequately? 

In order to help you, here are the step that you would have to perform: 

  1. list your 'times-1-9.x.new' files and then find a way to paste this listing with the 'Finaltimes' file;
  2. remember the program to rename your file -- add it programatically to the file resulting out of the pasting in 1.
  3. remember the first line that you have to have in order to execute a script in Linux -- write this line at the bottom of the file.
  4. a difficult one: even if we have tags to avoid duplicate files, and therefore possible problems, we had to find a strategy avoiding possible duplicates -- here we have taken only a file with 10 articles; think about it if you would have a sample with 100 or 1000 articles. What would be your strategy and how would you implement it in the script?
  
Now that we have our files ready, we want to run MTA on them and to make our first steps in the topic model analysis. Let us say some words about topic analysis from a theoretical and practical viewpoints. 


## Topic modeling from a theoretical viewpoint

Topic modeling in few words: 

  - belongs to methods that aims at revealing hidden structures in collections of data
  - sociologically, goes hand in hand with macro-theoretical explanation of society 
  - supports assumptions related to the idea that social phenomenons and society are not products of the pure willingness of actors, of their pure rationality -- society is a collective more or less controlled, more or less conscious production, which is not entirely intelligible for its actors
  - supports assumptions related to the underlying principles organizing social life (grammar of practice), individual attitudes and comportment (habits, coping), individual and collective expressions forms (rules, norms); does not take into account that such organizational principles are strongly rational, conscious etc.
  
When you are doing topic modeling, you are doing it in order to find these transversal principles in a collection of data that could explain the behavior of your data as a collection, as well as the behavior of the individual items in this collection in relationship to the behavior of the collection.

Topic modeling is a well suited method of modeling qualitative data in the frame of macro-relational scheme in sociology. But it is an exploratory method only, and it does not deliver a causal explanation of data. This can be seen as a disadvantage, because: 

  - representativeness of the models needs big data, which suppose big infrastructure (f.ex. datacenter), or at least very powerful computers
  - reliability of the models needs to survey the data constantly, adding them to existing topic models, which also suppose big infrastructure or very powerful computers. 
  
A third disadvantage of topic modeling is its age -- this is an old method dated back in the early 2000, and nowadays being supplanted by artificial intelligence. So what is the point to use such a method in social science and sociology?

There are the following advantages: 

  - low cost in terms of infrastructure needed: you can compute topic modeling with affordable computers -- even normal office machine will be able to modeling hundreds to few thousand of data easily
  - you can gain in representativeness with adapted methodological frame, f.ex. doing repeated measures on several batches of data, and comparing the evolution of models alongside these batches; this way, you can gain in reliability;
  - the algorithms are public, you can read them in order to understand how they work -- AI algorithms are most of the time patented or under private license, and therefore not available publicly
  - you can bridge the gap between qualitative and quantitative research -- topic modeling can act as context variables in quantitative research frameworks
  - transparency of topic modeling methods enhances collaboration on projects and insure the reproductibility of findings -- better control through peers


## Topic modeling from a technical viewpoint

In the frame of qualitative data analysis, topic modeling is faster than other interpretation methods resting on human centric interpretation, and it provide results that fit all cases in the analysis, preventing a reduction of these results to one hidden structure organizing your data. Topic modeling is therefore: 

  - a method in line with other data reduction methods -- it reduces data to dimensions organizing these data in smaller groups
  - a method underlying the complexity of the data -- it does not output one dimension, it outputs several dimension, which are several organization principles, each representing an interpretation of your data supported by the actors/actants having produced these data
  
Topic modeling is a way to categorize your data, and this kind of categorization is performed by algorithms. This is why you don't have one topic modeling method, but a family of topic modeling methods resting on different algorithm. In the literature about topic modeling, this family has been called Latent Semantic Analysis -- topic modeling is the modeling of such latent semantic structures with algorithms. 


## MTA in theory

There are different algorithms performing topic modeling. MTA is using three of them: 

  - Latent Dirichlet allocation (LDA): this algorithm by Blei has made topic modeling famous in the early 2000; it works based on probability/statistic models;
  - Non negative matrix factorization (NMF): this algorithm renew the approach of topic modeling introduced with LDA; it outputs a model based on matrices of words qua documents under the assumption of non negative element in these matrices; it is linear algebra oriented;
  - Word-to-Vector: this algorithm is a deep-learning algorithm which aims at reconstructing the semantic similarities of words in documents based on the principle that if one word has this meaning, then it is in relation with other words having a similar meaning; this algorithm, however, does not take contexts of words' meaning into account -- this is done by more AI oriented algorithms like BERT, which comes at the cost of more powerful infrastructure / computers, and therefore have not been implemented in MTA now.
  
One of the problem that you have when you are modeling topics is related to the unknown number of hidden structures which you could have in your data. This is what you don't know when you are modeling your data, and this is therefore a problem because all these algorithms need to know how much topic they have to model in order to do their job. MTA solves this problem using other clustering techniques whith which it tests the optimal number of topics to input in your topic modeling. This is the point where you can see how much topic modeling is an exploratory methods: the optimal number of topics to input in your topic modeling is not something in which you have to believe, it is something giving you an indication about what could be a good model. Therefore, this value has to be interpreted, and in order to interpret this value, you need to know what are your data, i.e. what kind of information you have in your data. 

The point regarding the number of optimal topic to model you data is also critical in regard of the reliability of your model. Most often, it is unlikely to take a huge number of topics, not only because it defeats the first purpose of topic modeling related to data reduction, but also because of the entropy of topic modeling. The more topics you have, the more underlying structures you will be able to see in your data, but the less reliable is your model. At the reverse, if you have only few topics in your data -- and providing that you have a lot of data --, you will have reliable topics, but you will loose information regarding how your data can be structured. 

The optimal number of topics is therefore a kind of compromise between reliable topics -- i.e. not too much topics --, and reliable information about the structure of your data -- i.e. not too few topics. 

In MTA, topic modeling is the first step in the modeling of your data. The result is a categorization of each individual items of your data in the number of topics you have given. For example, if you are modeling texts -- the most emblematic case of topic modeling --, and if you have an optimal model with let us say four topics, then you will get this kind of result: 

```

Topic_0      Topic_1        Topic_2       Topic_3

car          drive          economics     environment
highway      holiday       crisis        energy
motor        buy            ford          renewable
oil          traveling     volkswagen    climate
...
...
...
```

In order to make sense out of these four topics, you have to interpret the meaning of each topic based on the words in each of them -- MTA returns the 20 most important words depicting your topics, and based on these words, it should be easy to understand the meaning of each topics. F.ex. in our model with four topics, the first one is related to cars, the second to traveling by car, the third topic underlines the economic dimension, i.e. the car industry and the crisis affecting it, and the last topic underlines the questions about the impact of the car industry on climate, and the way to renew this industry with other kinds of energy. 

Based on your model, you will be able to perform other operations, which are:

  - studying the evolution of your model (and of your topics) in time if you have a give a time stamp in the filename of your data -- this is a longitudinal analysis of your data;
  - studying the contribution of items in your data to the different topics you have modeled: items contribute to topics differently, and in some case for items which are of first importance for you, it is advisable to see how they contribute to support your topics;
  - studying the semantics field associated with the items that are important for you regarding your research purpose. 


## MTA in practice

In order to show you how to run MTA, we provide a video tutorial with the following steps: 

  - open MTA and input your data
  - tune your models
  - simulate your modeling and choose the optimal number of topics
  - do your topic analysis
  - represent your topics in time
  - look for meaningful words and their contribution to your topics
  - look for semantic similarity for given words
  
You can find this tutorial video here:

  - [English version](https://cp.soziologie.uni-halle.de/MQD/MTA-Intro-ENG.webm)
  - [German version](https://cp.soziologie.uni-halle.de/MQD/MTA-Intro-DE.webm)

```python

```
