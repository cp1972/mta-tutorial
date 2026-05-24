import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd
import csv
plt.rcParams['figure.figsize'] = [12, 8]

st.set_page_config(layout="wide") # um die Webseite breiter zu machen

#st.title("Vorstellung erster Ergebnisse") # Haupttitle nicht im Zentrum der Seite

st.markdown("<h1 style='text-align: center; color: orange;'>Vorstellung erster Ergebnisse</h1>", unsafe_allow_html=True) # Jetzt Haupttitle zentriert

### Veränderung der dataframe

df_eng = pd.read_csv('Dominant_Topics_ENG_2.csv')
df_eng.rename(columns={ df_eng.columns[0]: "Articles" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
df_eng.drop('Dominant_Topic_NMF', axis=1, inplace=True)
df_eng['Year'] = df_eng['Articles']
df_eng['Newspaper'] = df_eng['Articles']
df_eng['Year']= df_eng['Year'].map(lambda x: str(x)[0:4])
#df_eng['Year'].astype(int)
df_eng['Newspaper']= df_eng['Newspaper'].map(lambda x: str(x)[11:14])
#df_eng2 = df_eng.sort_values(by='Year',ascending=True)

### Title für die Seite und dataframe in der Sidebar zeigen

st.sidebar.title("Erklärung der Ergebnisse")
st.sidebar.markdown('**Hier** wollen wir _einige_ Erklärungen schreiben')

## Entscheidung, ob die Daten angezeigt werden müssen

if st.sidebar.checkbox('Daten anzeigen'):
    st.dataframe(df_eng)

### Filter zum Sortieren der dataframe

## Daten und Zeitungen einzel aus dem dataframe ziehen 

jahre = list(df_eng['Year'].drop_duplicates())
zeitungen = list(df_eng['Newspaper'].drop_duplicates())

## Filter herstellen mit mutliselect Auswahl für die Zeitungen und für die Jahre

#jahre_wahl = st.multiselect('Jahre auswählen:', jahre, default=jahre)
#zeitungen_wahl = st.multiselect('Zeitungen auswählen:', zeitungen, default=zeitungen)

## Filter auf dataframe anwenden mit multiselect

#df_eng = df_eng[df_eng['Year'].isin(jahre_wahl)]
#df_eng = df_eng[df_eng['Newspaper'].isin(zeitungen_wahl)]

## Filter für Newspaper und slider für Jahre

zeitungen_wahl = st.sidebar.multiselect('Zeitungen auswählen:', zeitungen, default=zeitungen)
jahre_wahl = st.sidebar.slider('Jahre:', 2002, 2021)

## Filter mit multiselect und slider anwenden

df_eng = df_eng[df_eng['Year'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
df_eng = df_eng[df_eng['Newspaper'].isin(zeitungen_wahl)]

### Vorbereitung der Graphiken -- Topics als Elemente in der Graphik, x = Jahre, y = Frequenzen

column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:5], default=df_eng.columns[1])
df_eng = df_eng.rename(columns={'Year':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen

## Zwei Spalten für eine Line und eine Bar Graphik herstellen

col1, col2= st.columns(2)

with col1:
    col1.header = "Line Graphik"
    #col1.write("Entwicklung der Topics in der Zeit") nicht zentriert
    col1.markdown("<h3 style='text-align: center; color: white;'>Topics in der Zeit</h3>", unsafe_allow_html=True)
    st.line_chart(df_eng[column])
    col1.markdown('Beispiel für eine Beschreibung in der Spalte unter der Graphik')

with col2:
    col2.header = "Bar Graphik"
    #col2.write("Dichte der Topics in der Zeit") nicht zentriert
    col2.markdown("<h3 style='text-align: center; color: white;'>Topics kumulativ</h3>", unsafe_allow_html=True)
    st.bar_chart(df_eng[column])

st.markdown('Hier können wir weitere Erklärungen für beide Graphiken schreiben.')
