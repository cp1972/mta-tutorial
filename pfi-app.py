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

st.markdown("<h1 style='text-align: center; color: DarkOliveGreen;'>PF-I - Themen aus den Veröffentlichungen 2013-2023</h1>", unsafe_allow_html=True) # Jetzt Haupttitle zentriert

st.markdown("<h4 style='text-align: left; color: OliveDrab;'>Folgende freiwillige Mitglieder der PF-I nehmen an dieser Umfrage teil (Stand jetzt)</h4>", unsafe_allow_html=True)

teilnehmer = {
"Altertumw.": [2, 1],
"Ethnologie": [4, 6],
"Geschichte": [8, 33],
"Kunstge.": [1, 0],
"Orient.": [2, 0],
"Philosophie": [2,4], 
"Politikw.": [1, 2],
"Archeologie": [2, 4],
"Psychologie": [5, 7],
"Soziologie": [3, 6],
"PF Gesamt": [30, 63],
"PF Gesamt (%)": [71, 66],
}

#load data into a DataFrame object:
df_teil = pd.DataFrame(teilnehmer, index = ["Professoren", "Mitarbeiter"])
#df_teil2 = df_teil[["PF Gesamt","PF Gesamt (%)"]]
st.bar_chart(df_teil["PF Gesamt (%)"])

### Title für die Seite und dataframe in der Sidebar zeigen

## If else statements -- Zeigt die unterschiedlichen Elemente des boards, wenn eine Auswahl getätigt wird

button = st.sidebar.selectbox("**Institute/Bereiche auswählen**", ('Altertumwissenschaft', 'Ethnologie', 'Geschichte', 'Kunst', 'Orient', 'Philosophie', 'Politikwissenschaft', 'Archeologie', 'Psychologie', 'Soziologie'))
#button2 = st.sidebar.radio("**PF-I Gesamt**", ('Topics', 'Trends'))

if button == 'Altertumwissenschaft':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/ALTW.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:5])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)
    st.markdown("Topic_0: Schriftkultur in Ägypten und Griechenland in der ptolemäischen Zeit; Wechselwirkungen und Vergleich mit Latein/Rom")
    st.markdown("Topic_1: Grabepigramme und Kunstgeschichte in der ptolemäischen Zeit bezogen auf Machtakteure wie Könige oder auf wichtige kulturelle Institutionen wie Religion/Recht")
    st.markdown("Topic_2: Beschreibung von Riten (Priesterprozession, Kaiserkult usw.) in Verbindung mit Machtakteuren an der Schnittstelle zwischen Macht und Religion/Recht")
    st.markdown("Topic_3: Verbindungen mit Kulten (wie etwa Opfer- und Gabenkulten) auch in Verbindung mit anderen Disziplinen wie Archeologie")
    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Semantische Felder um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/ALTW.pdf-1.png",width=1400)

elif button == 'Ethnologie':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/ETHNO.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:6])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)
    st.markdown("Topic_0: Politische Kultur und Gestaltung der Kulturen in der Welt im Rahmen der UNESCO Welterbe")
    st.markdown("Topic_1: Rückgabe vom Land in Südafrika nach der Apartheid und Fragen der Justiz und der Identität in diesem Kontext, auch nicht zuletzt in Vergleich mit anderen Regionen in der Welt (wie etwa Irland)")
    st.markdown("Topic_2: Digitale Infrastrukturen in Nordeuropa auch im kulturellen Vergleich mit anderen Ländern; Frage der Mobilisation von Akteuren, der Konnektivität, der Legitimität und der Erkenntnis in diesem Kontext")
    st.markdown("Topic_3: Politik, Krisen und Materialität im indischen Ozean wie auch in Russland und in Sudan, hier vielleicht mit stärerer Betonung der ethnographischen Perspektive")
    st.markdown("Topic_4: Fragen der Identität, der Emotionen, der Empathie, der Zugehörigkeit und der Ethik in Bezug auf unterschiedliche Kulturen in der Welt (Asien, Australien, Deutschland)")
    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Semantische Felder um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/ETHNO.pdf-1.png",width=1400)

elif button == 'Geschichte':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/GESCH.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:6])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)
    st.markdown("Topic_0: Herrschaftspraktiken in Mitteldeutschland, mit besonderem Fokus auf Fürsten in Anhalt/Sachsen")
    st.markdown("Topic_1: Politik, Kapitalismus und Herrschaft in der Neuzeit, mit Akzentsetzung auf Erziehung/Waisenhaus und auf Pietismus")
    st.markdown("Topic_2: Polenstudien und entsprechende Fragen zu Polen und NS-Zeit, zu Juden, zu Aufarbeitung der Beziehungen zwischen Polen und Deutschland, zu Gerechtigkeit; Fallstudien")
    st.markdown("Topic_3: Universität Halle von der Aufklärung bis heute im deutschen Kontext; in diesem Topic ebenfalls die Betonung von Daten und Digitalisierung von Daten (Netzwerkforschung)")
    st.markdown("Topic_4: Diktaturen und Demokratien am Beispiel Spanien unter Franco in Verbindung mit Deutschland")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Semantische Felder um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/GESCH.pdf-1.png",width=1400)

elif button == 'Kunst':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/KUNST.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
    #df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:5])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)
    st.markdown("Topic_0: Krieg und (entartete) Kunst in der NS-Zeit, Expressionismus, Sammlungen und Austellungen in diesem Kontext")
    st.markdown("Topic_1: Kunst in der Zwischenkriegszeit in Deutschland und Österreich, besonders im Bezug auf Einzelkünstler und ihre Rezeption; Sachlichkeit von Kunst in diesem Kontext")
    st.markdown("Topic_2: Auseinandersetzung der Künstler mit dem System in der NS-Zeit, geschichstliche Rekonstruktion und politische Bedeutung")
    st.markdown("Topic_3: Vergleich mit der Weimar-Republik")

    st.bar_chart(df_1[column])
#    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verhältnis zu Transformation Nachhaltigkeit Digitalisierung</h4>", unsafe_allow_html=True)
#    st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/KUNST.pdf-1.png",width=1400)

elif button == 'Orient':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/ORI.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
#    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
#     df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:4])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen
    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)

    st.markdown("Topic_0: Fokus auf Turkey in der osmanischen Zeit und Syrien ab dem 18. Jh. bis heute")
    st.markdown("Topic_1: Texte zu Reisen und Briefwechsel zu Kulturen in diesen Gebieten mit Deutschland")
    st.markdown("Topic_2: Erweiterung der Perspektive auf kurdischen und persischen Kulturen, Untersuchung von Expeditionen in diesen Gebieten immer wieder in Wechselbeziehung mit Deutschland")

    st.bar_chart(df_1[column])
 #   st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verhältnis zu Transformation Nachhaltigkeit Digitalisierung</h4>", unsafe_allow_html=True)
 #   st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/ORI.pdf-1.png",width=1400)

elif button == 'Philosophie':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/PHILO.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:6])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen
    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)

    st.markdown("Topic_0: Kant-Forschung mit Themen um die Kritik der praktischen Vernunft, die Moral, die Freiheit; Hervorhebung der Verbindung zur Gesellschaft (Sozialontologie) und der epistemologischen Fragen in diesem Zusammenhang")
    st.markdown("Topic_1: Materialismus, analytische Philosophie und Salamanca Schule mit Betonung der Fragen zur Kognition und zum Bewusstsein")
    st.markdown("Topic_2: Rechstphilosophie besonders in Bezug auf Aufklärung und auf italienische Schulen")
    st.markdown("Topic_3: Große Rahmenthemen der Philosophie mit Fragen zum Naturalismus, Realismus, Objektivität, Wahrheit, Kontingenz in Bezug auf Sprachphilosophie; auch in diesem Topic Fragen zur Moral (Pflicht, Ethik, Kreativität) ")
    st.markdown("Topic_4: Debatten zwischen Denktraditionen (bes. Empirismus, Kantianismus, analytischer Philosophie und Sprachphilosophie), mit Einbezug der Philosophie von M. Heidegger und der praktischen Philosophie")
    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Semantische Felder um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
#    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verhältnis zu Transformation Nachhaltigkeit Digitalisierung</h4>", unsafe_allow_html=True)
    st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/PHILO.pdf-1.png",width=1400)

elif button == 'Politikwissenschaft':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/POWI.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
 #    df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:5])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen
    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)

    st.markdown("Topic_0: UNO-Forschung im Bezug auf europäische Sicherheitspolitik und Außenpolitik")
    st.markdown("Topic_1: Forschungsmethoden (bes. dokumentarische Methoden) und Fachdidaktik; Pädagogik ")
    st.markdown("Topic_2: Forschung zu Parteien in Deutschland (Wahl, Kandidaten, Bundestag)")
    st.markdown("Topic_3: Europäisierung und Governance im Bezug auf Wirtschaft, Digitalisierung und Familien")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Semantische Felder um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/POWI.pdf-1.png",width=1400)

elif button == 'Archeologie':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/PREHIST.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
 #    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
 #    df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:4])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen
    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)

    st.markdown("Topic_0: Forschung zu antiken und archaischen Kulturen bes. in der Turkey (Didyma)")
    st.markdown("Topic_1: Forschung zu mittelaterlischen Kulturen in Sachsen-Anhalt (Quedlingburg) und in Österreich")
    st.markdown("Topic_2: Gegenstände (etwa Keramiken) zur Interpration von Kulten und Riten in diesen Kulturen")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Semantische Felder um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/PREHIST.pdf-1.png",width=1400)

elif button == 'Psychologie':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/PSY.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:6])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen
    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)

    st.markdown("Topic_0: Forschung zum Wohlbefinden von Akteuren bezogen auf Themen wie Humor, Verspieltheit, Gelotophobie")
    st.markdown("Topic_1: Forschungsmethoden und Modellierungen in der Psychologie")
    st.markdown("Topic_2: Psychologie der Erwachsenen bezogen einerseits auf Beziehungen mit anderen (etwa ausgelacht werden, Täuschungen) und andererseits auf eigene kognitive Dimensionen (Persönlichkeit, Depression)")
    st.markdown("Topic_3: Sozialpsychologische Themen (Zuschreibungen, Wahrnehmungen, Stereotypen, Glauben) im Bezug auf Alterung mit kognitiven Folgen")
    st.markdown("Topic_4: Sozialpsychologische Themen im Bezug auf gesellschaftliche Differenzierungsphänomene (etwa Diskriminierung, Mitgefühl, Rollen, Vorurteile) und aktuelle gesellschaftliche Themen (wie etwa Klimawandel)")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Semantische Felder um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/PSY.pdf-1.png",width=1400)

elif button == 'Soziologie':
    df_eng = pd.read_csv('/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/Final/SOZ.csv')
    df_eng.rename(columns={ df_eng.columns[0]: "Veröffentlichungen" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[1]: "Topic_0" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[2]: "Topic_1" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[3]: "Topic_2" }, inplace = True)
    df_eng.rename(columns={ df_eng.columns[4]: "Topic_3" }, inplace = True)
 #    df_eng.rename(columns={ df_eng.columns[5]: "Topic_4" }, inplace = True)
    df_eng.drop('Dominant_Topic_NMF',axis=1,inplace=True)
    df_eng['Jahr'] = df_eng['Veröffentlichungen']
    df_eng['Autor'] = df_eng['Veröffentlichungen']
    df_eng['Jahr']= df_eng['Jahr'].map(lambda x: str(x)[0:4])
    df_eng['Autor']= df_eng['Autor'].map(lambda x: str(x)[5:7])
    jahre = list(df_eng['Jahr'].drop_duplicates())
    zeitungen = list(df_eng['Autor'].drop_duplicates())

    zeitungen_wahl = st.sidebar.multiselect('Autor auswählen:', zeitungen, default=zeitungen)
    jahre_wahl = st.sidebar.slider('Jahre:', 2013, 2023, value=2015)
    df_eng = df_eng[df_eng['Jahr'] <= str(jahre_wahl)] # str is important, if not there, then you'll get an error
    df_eng = df_eng[df_eng['Autor'].isin(zeitungen_wahl)]
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:5])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen
    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)

    st.markdown("Topic_0: Relationale Soziologie und Differenzierungstheorien bes. im Bereich der Kunst (bes. digitalen Kunst) und der Chancengleichheit vor (Hoch)Schulen im internationalen Vergleich")
    st.markdown("Topic_1: Bildungsforschung zur Akademisierung und Hochschulexpansion bes. in Deutschland")
    st.markdown("Topic_2: Institutionalisierungstheorien und Erziehungstheorien mit Brücken zwischen Ausbildungssystem und Arbeitsmarkt und mit Bezug auf Emotionen und Gefühlen")
    st.markdown("Topic_3: Soziologie von kleineren Kontexten in sozialstrukturellen Perspektiven (Kommunen, Kreisen), Migrationssoziologie, Soziologie der digitalen Welt mit Bezug auf relationale Perspektiven")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Semantische Felder um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.image("/home/cpsoz/MLU-PUbli-2013-2023/TRAIN/Fin/SOZ.pdf-1.png",width=1400)
