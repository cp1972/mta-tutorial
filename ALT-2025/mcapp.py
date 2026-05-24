import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd
import csv
plt.rcParams['figure.figsize'] = [12, 8]

### Streamlit dashboard mit multipages -- hiermit benutzen wir radio buttons und if Bedingungen, um die Seiten zu simulieren

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
df_eng['Newspaper']= df_eng['Newspaper'].map(lambda x: str(x)[11:14])
jahre = list(df_eng['Year'].drop_duplicates()) 
zeitungen = list(df_eng['Newspaper'].drop_duplicates())
 
### Title für die Seite und dataframe in der Sidebar zeigen

st.sidebar.title("Erklärung der Ergebnisse")
st.sidebar.markdown('**Hier** wollen wir _einige_ Erklärungen schreiben')

## If else statements -- Zeigt die unterschiedlichen Elemente des boards, wenn eine Auswahl getätigt wird

button = st.sidebar.radio("Aus dem Menü auswählen", ('Rohe Daten anzeigen', 'Entwicklung der Topics in der Zeit', 'Kumulierte Topics in der Zeit'))

if button == 'Rohe Daten anzeigen':
    zeitungen_wahl = st.sidebar.multiselect('Zeitungen auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2002, 2021, value=2010)
    df_eng = df_eng[df_eng['Year'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Newspaper'].isin(zeitungen_wahl)]
    st.dataframe(df_eng)
    st.markdown ('Beispiel für eine Kommentierung der Tabelle')
elif button == 'Entwicklung der Topics in der Zeit':
    zeitungen_wahl = st.sidebar.multiselect('Zeitungen auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2002, 2021, value=2010)
    df_eng = df_eng[df_eng['Year'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Newspaper'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:5])
    df_1 = df_eng.rename(columns={'Year':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen
    st.line_chart(df_1[column])
elif button == 'Kumulierte Topics in der Zeit':
    zeitungen_wahl = st.sidebar.multiselect('Zeitungen auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2002, 2021, value=2010)
    df_eng = df_eng[df_eng['Year'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Newspaper'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:5])
    df_2 = df_eng.rename(columns={'Year':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen
    st.bar_chart(df_2[column])



st.markdown('Hier können wir weitere Erklärungen schreiben -- dies kann man auch bei der Auswahl in jeder Rubrik schreiben')
