#!/bin/sh

# Script to ease interpretation of topics with MTA using tgpt for access to AI, i.e. big transformers on the Internet (without API key)
#
# First install tgpt for your system (Windows, MacOS, Linux) following the indications here: https://github.com/aandrew-me/tgpt
#
# We are using two data in our MTA Folder to interpret the lists of words per Topics using tgpt:
#
# - Top_Words_*_Topics.csv
#
# - Weights_Words_*.csv
#
# Our goal is to pass the words describing the topics to an AI-Transformer in order to gain more insight in how to interprete the topic.
# Here is the code for Top_Words_*_Topics.csv data:

awk -F, 'NR>1{print $1}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words"

# -F,: we indicate to awk that our data are separated by a comma
# 'NR>1{print $1}': we don't take the header and we print the first column with the words for Topic_0 only; if we have 4 topics, we repeat this line 4 times and change print $1 to print $2 for the second topic and so on
# awk 'BEGIN { ORS = " " } { print }': we transpose the columns of words into a row of words
# tgpt --model groq "common thread among these words": we ask tgpt to find the common thread among the given words, and we are using the groq transformer here (other are available)
#
# The code for the Weights_Words_*.csv file look a bit different, but does the same with more words per topics (50 instead of 20)

awk -F'\t' 'NR>=2{print $2} NR==49{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words"

# -F'\t': we indicate to awk that our data is separated by tabulators
# 'NR>=2{print $2} NR==49{exit}': we take the words for the Topic_0 without the header; if we want to take the words for the Topic_1 after it, we would modify this code like this: 'NR>=50{print $2} NR==99{exit}'; and so on after the line 99 for other possible topics in this file
# 'NR>=2{print $2} : we are always printing the second column, i.e. the words in this file (hence $2); this remain always the same
# the rest of the code is the same as the code above related to the file Top_Words_*_Topics.csv
#
# If you want to save the results of tgpt to a file, you have to alter the code like this:

awk -F, 'NR>1{print $1}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" > my-specific-file.txt

awk -F'\t' 'NR>=2{print $2} NR==49{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" > my-specific-file.txt

# If you have four topics and you want to save the results of tgpt to the same file, you can do like this

awk -F, 'NR>1{print $1}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" > my-specific-file.txt
awk -F, 'NR>1{print $2}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
awk -F, 'NR>1{print $3}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
awk -F, 'NR>1{print $4}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt

awk -F'\t' 'NR>=2{print $2} NR==49{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" > my-specific-file.txt
awk -F'\t' 'NR>=50{print $2} NR==99{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
awk -F'\t' 'NR>=100{print $2} NR==149{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
awk -F'\t' 'NR>=150{print $2} NR==199{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt

# Example of code to better separate the results of tgpt by indicating to which topic the result is related (you can elaborate on that to make separations even nicer)

echo "TOPIC_0" > my-specific-file.txt
awk -F, 'NR>1{print $1}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
echo "TOPIC_1" >> my-specific-file.txt
awk -F, 'NR>1{print $2}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
echo "TOPIC_2" >> my-specific-file.txt
awk -F, 'NR>1{print $3}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
echo "TOPIC_3" >> my-specific-file.txt
awk -F, 'NR>1{print $4}' Top_Words_NMF_Topics_22_06_2024_11_17_03.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt

echo "TOPIC_0" > my-specific-file.txt
awk -F'\t' 'NR>=2{print $2} NR==49{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
echo "TOPIC_1" >> my-specific-file.txt
awk -F'\t' 'NR>=50{print $2} NR==99{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
echo "TOPIC_2" >> my-specific-file.txt
awk -F'\t' 'NR>=100{print $2} NR==149{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt
echo "TOPIC_3" >> my-specific-file.txt
awk -F'\t' 'NR>=150{print $2} NR==199{exit}' Weights_Words_NMF_Topics.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain the common thread among these words" >> my-specific-file.txt

# Taking advantage of the weights of the words for your interpretation: Using the data Weights_Words_*_Topics.csv, you can ask the AI to group the words based on their meaning and their score to gain in accuracy in your interpreation of the topics. Here is an example prompt

awk -F'\t' 'NR>=52{print $2" "$3} NR==99{exit}' Weights_Words_NMF*.csv | awk 'BEGIN { ORS = " " } { print }' | tgpt --model groq "explain clusters of these words based on their weights"

# 'NR>=52{print $2" "$3} NR==99{exit}': we take the words from Topic_1 and we print each word with its weight (column $3); we separate words and weight with a blank space (" " in the code)
# You can do it for all topics and you can save the results in a specific file for further consideration (see examples above)

# If you don't have awk and bash, you can copy the list of words to the tgpt prompt like this
# tgpt --model groq "explain the common thread among these words: car carwash (as example of your words)"
