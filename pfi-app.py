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

st.markdown("*Was wird untersucht, wie, wozu und mit welchem Ergebnis?*: 

  - *Was?*: Abbildung der Themen aus den Veröffentlichungen der Mitglieder der PF-I nach Bereichen/Instituten für die Zeit 2013-2023. 
  - *Wie?*: Topic-Modell-Analyse mit MTA-Software (https://cp.soziologie.uni-halle.de/MTA/doku.php).
  - *Wozu?*: Selbstbild der Themen in der PF-I, daran die Mitglieder der PF-I in den unterschiedlichen Bereich arbeiten. Bessere Position im Bezug auf die durchgeführte Diskussion zur inhaltlichen Profilierung der MLU und zu den Begriffen, die in diesem Zusammenhang kursieren (bes. Transformation, Nachhaltigkeit und Wissen -- unten wurde noch Digitalisierung hinzugefügt).
  - *Ergebnis?*: hohe Teilnahme an der Untersuchung führt zur mehrheitlichen guten bis sehr guten Abbildung der Themen in der PF-I; trotzdem bleiben einige Bereiche (Kunstgeschichte, Orient, Politikwissenschaft) unzureichend belegt, weshalb dort die Analyse nur Themen von teilnehmenden Einzelakteuren abbildet.")

st.markdown("*Grenzen*:

  - *Allgemein*: Die Abbildung von Themen auf der Grundlage der Titel von Veröffentlichungen führt häufig zu Unter/Überschätzungen, weil Titel Inhalte grob zusammenfassen; wir bilden also inhaltliche Tendenzen ab.
  - *Spezifisch*: Der Bezug auf Begriffe, die vom Rektorat im Rahmen der Profilierung der MLU verwendet werden, erfolgt oft mittelbar -- dabei wird bes. der Begriff Nachhaltigkeit wenig unterstützt (etwa mittelbar in der Psychologie und in der Soziologie). Deshalb werden auch Synonymen von Transformation, Nachhaltigkeit, Digitalisierung und Wissen auf Deutsch und Englisch verwendet (wie etwa Wandel, sustainability, digital, education usw.)"
    )

st.markdown("<h4 style='text-align: left; color: OliveDrab;'>Folgende freiwillige Mitglieder der PF-I nehmen an dieser Umfrage teil</h4>", unsafe_allow_html=True)

teilnehmer = {
"Altertumw.": [3, 1],
"Ethnologie": [4, 6],
"Geschichte": [8, 33],
"Kunstge.": [1, 0],
"Orient.": [2, 0],
"Philosophie": [2,4],
"Politikw.": [1, 2],
"Archeologie": [4, 9],
"Psychologie": [7, 9],
"Soziologie": [4, 8],
"PF Gesamt": [36, 72],
"PF Gesamt (%)": [86, 76],
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
    df_eng = pd.read_csv('Final/ALTW.csv')
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
    st.markdown("Topic_0 (55%): Schriftkulturen in Ägypten und Griechenland in der ptolemäischen Zeit; Wechselwirkungen und Vergleich mit Latein/Rom")
    st.markdown("Topic_1 (9%): Grabepigramme und Kunstgeschichte in der ptolemäischen Zeit bezogen auf Machtakteure wie Könige oder auf wichtige kulturelle Institutionen wie Religion/Recht")
    st.markdown("Topic_2 (23%): Beschreibung von Riten (Priesterprozession, Kaiserkult, Tiere usw.) in Verbindung mit Machtakteuren an der Schnittstelle zwischen Macht und Religion/Recht; Bedeutung von Plutarch")
    st.markdown("Topic_3 (13%): Verbindungen mit Kulten (wie etwa Opfer- und Gabenkulten) auch in Verbindung mit anderen Disziplinen wie Archeologie")
    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Kontexte um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.markdown("Wandel: insb. Topic_0 und Topic_1")
    st.markdown("Wissen: insb. Topic_2")
    st.image("Final/ALTW.pdf-1.png",width=1400)

elif button == 'Ethnologie':
    df_eng = pd.read_csv('Final/ETHNO.csv')
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
    st.markdown("Topic_0 (22%): Politische Kultur und Gestaltung der Kulturen in der Welt im Rahmen der UNESCO Welterbe")
    st.markdown("Topic_1 (18%): Rückgabe vom Land in Südafrika nach der Apartheid und Fragen der Justiz und der Identität in diesem Kontext, auch nicht zuletzt in Vergleich mit anderen Regionen in der Welt (wie etwa Irland)")
    st.markdown("Topic_2 (15%): Digitale Infrastrukturen in Nordeuropa auch im kulturellen Vergleich mit anderen Ländern; Frage der Mobilisation von Akteuren, der Konnektivität, der Legitimität und der Erkenntnis in diesem Kontext")
    st.markdown("Topic_3 (19%): Politik, Krisen und Materialität im indischen Ozean wie auch in Russland und in Sudan, hier vielleicht mit stärerer Betonung der ethnographischen Perspektive")
    st.markdown("Topic_4 (17%): Fragen der Identität, der Emotionen, der Empathie, der Zugehörigkeit und der Ethik in Bezug auf unterschiedliche Kulturen in der Welt (Asien, Australien, Deutschland)")
    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Kontexte um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.markdown("Wandel: insb. Topic_0, Topic_1, Topic_4")
    st.markdown("Digital: insb. Topic_2 und Topic_0")
    st.markdown("Wissen: insb. Topic_0, Topic_1 und Topic_4")
    st.image("Final/ETHNO.pdf-1.png",width=1400)

elif button == 'Geschichte':
    df_eng = pd.read_csv('Final/GESCH.csv')
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
    st.markdown("Topic_0 (13%): Herrschaftspraktiken in Mitteldeutschland, mit besonderem Fokus auf Fürsten in Anhalt/Sachsen")
    st.markdown("Topic_1 (20%): Politik, Kapitalismus und Herrschaft in der Neuzeit, mit Akzentsetzung auf Erziehung/Waisenhaus und auf Pietismus")
    st.markdown("Topic_2 (26%): Polenstudien und entsprechende Fragen zu Polen und NS-Zeit, zu Juden, zu Aufarbeitung der Beziehungen zwischen Polen und Deutschland, zu Gerechtigkeit; Fallstudien")
    st.markdown("Topic_3 (24%): Universität Halle von der Aufklärung bis heute im deutschen Kontext; in diesem Topic ebenfalls die Betonung von Daten und Digitalisierung von Daten (Netzwerkforschung)")
    st.markdown("Topic_4 (17%): Diktaturen und Demokratien am Beispiel Spanien unter Franco in Verbindung mit Deutschland")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Kontexte um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.markdown("Transformation, Wandel, change: in allen Topics")
    st.markdown("Digital: insb. Topic_3, auch Topic_1 und Topic_4")
    st.markdown("Wissen, Bildung, knowledge: insb. Topic_2 und Topic_1")
    st.image("Final/GESCH.pdf-1.png",width=1400)

elif button == 'Kunst':
    df_eng = pd.read_csv('Final/KUNST.csv')
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
    st.markdown("Topic_0 (27%): Krieg und (entartete) Kunst in der NS-Zeit, Expressionismus, Sammlungen und Austellungen in diesem Kontext")
    st.markdown("Topic_1 (36%): Kunst in der Zwischenkriegszeit in Deutschland und Österreich, besonders im Bezug auf Einzelkünstler und ihre Rezeption; Sachlichkeit von Kunst in diesem Kontext")
    st.markdown("Topic_2 (18%): Auseinandersetzung der Künstler mit dem System in der NS-Zeit, geschichstliche Rekonstruktion und politische Bedeutung")
    st.markdown("Topic_3 (19%): Vergleich mit der Weimar-Republik")

    st.bar_chart(df_1[column])
#st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Kontexte um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verhältnis zu Transformation Nachhaltigkeit Digitalisierung</h4>", unsafe_allow_html=True)
    st.markdown("Kein besonderes Verhältnis zu diesen Begriffen oder deren Synonymen")
#    st.image("KUNST.pdf-1.png",width=1400)

elif button == 'Orient':
    df_eng = pd.read_csv('Final/ORI.csv')
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

    st.markdown("Topic_0 (40%): Fokus auf Turkey in der osmanischen Zeit und Syrien ab dem 18. Jh. bis heute")
    st.markdown("Topic_1 (40%): Texte zu Reisen und Briefwechsel zu Kulturen in diesen Gebieten mit Deutschland")
    st.markdown("Topic_2 (20%): Erweiterung der Perspektive auf kurdischen und persischen Kulturen, Untersuchung von Expeditionen in diesen Gebieten immer wieder in Wechselbeziehung mit Deutschland")

    st.bar_chart(df_1[column])
    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verhältnis zu Transformation Nachhaltigkeit Digitalisierung</h4>", unsafe_allow_html=True)
    st.markdown("Kein besonderes Verhältnis zu diesen Begriffen oder deren Synonymen")
##   st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verhältnis zu Transformation Nachhaltigkeit Digitalisierung</h4>", unsafe_allow_html=True)
 #   st.image("ORI.pdf-1.png",width=1400)

elif button == 'Philosophie':
    df_eng = pd.read_csv('Final/PHILO.csv')
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

    st.markdown("Topic_0 (27%): Kant-Forschung mit Themen um die Kritik der praktischen Vernunft, die Moral, die Freiheit; Hervorhebung der Verbindung zur Gesellschaft (Sozialontologie) und der epistemologischen Fragen in diesem Zusammenhang")
    st.markdown("Topic_1 (33%): Materialismus, analytische Philosophie und Salamanca Schule mit Betonung der Fragen zur Kognition und zum Bewusstsein")
    st.markdown("Topic_2 (16%): Rechstphilosophie besonders in Bezug auf Aufklärung und auf italienische Schulen")
    st.markdown("Topic_3 (14%): Große Rahmenthemen der Philosophie mit Fragen zum Naturalismus, Realismus, Objektivität, Wahrheit, Kontingenz in Bezug auf Sprachphilosophie; auch in diesem Topic Fragen zur Moral (Pflicht, Ethik, Kreativität) ")
    st.markdown("Topic_4 (10%): Debatten zwischen Denktraditionen (bes. Empirismus, Kantianismus, analytischer Philosophie und Sprachphilosophie), mit Einbezug der Philosophie von M. Heidegger und der praktischen Philosophie")
    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Kontexte um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
#    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verhältnis zu Transformation Nachhaltigkeit Digitalisierung</h4>", unsafe_allow_html=True)
    st.markdown("Wissen: in allen Topics, etwas stärker in Topic_0 und Topic_2")
    st.image("Final/PHILO.pdf-1.png",width=1400)

elif button == 'Politikwissenschaft':
    df_eng = pd.read_csv('Final/POWI.csv')
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

    st.markdown("Topic_0 (49%): UNO-Forschung im Bezug auf europäische Sicherheitspolitik und Außenpolitik, und auf Menschenrechte")
    st.markdown("Topic_1 (22%): Forschungsmethoden (bes. dokumentarische Methoden) und Fachdidaktik; Pädagogik ")
    st.markdown("Topic_2 (14%): Forschung zu Parteien in Deutschland (Wahl, Kandidaten, Bundestag)")
    st.markdown("Topic_3 (15%): Europäisierung und Governance im Bezug auf Wirtschaft, Digitalisierung und Familien")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Kontexte um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.markdown("Digital: Topic_0, Topic_2 und Topic_3")
    st.markdown("Bildung: Topic_1")
    st.image("Final/POWI.pdf-1.png",width=1400)

elif button == 'Archeologie':
    df_eng = pd.read_csv('Final/PREHIST.csv')
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
    column = st.sidebar.multiselect('Topics auswählen', df_eng.columns[1:4])
    df_1 = df_eng.rename(columns={'Jahr':'index'}).set_index('index') # notwendig damit Jahre in der x Achse erscheinen
    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Verteilung der Topics in der Zeit</h4>", unsafe_allow_html=True)

    st.markdown("Topic_0 (22%): Forschung zu antiken und archaischen Kulturen bes. in der Turkey (Didyma)")
    st.markdown("Topic_1 (23%): Forschung zu mittelaterlischen Kulturen (etwa Keramiken, Grabungsergebnisse, Hausgeisterglauben usw.) in Sachsen-Anhalt (Quedlingburg), Pfalz und in Österreich")
    st.markdown("Topic_2 (47%): Interpration von Kulten und Riten, Bedeutung von Ringheiligtum, Opfer im Bezug auf Europa")
    st.markdown("Topic_3 (8%): Rekonstruktion der gesellschaftlichen Komplexität, der gesellschaftlichen Differenzierung in der Steinzeit in Europa und in Detuschland; Bedeutung von Sakralbauten und damit verbundenen Riten")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Kontexte um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.markdown("Wandel, Veränderung(en): in allen Topics")
    st.image("Final/PREHIST.pdf-1.png",width=1400)

elif button == 'Psychologie':
    df_eng = pd.read_csv('Final/PSY.csv')
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

    st.markdown("Topic_0 (19%): Forschung zur Kognition insb. Gedächtnis, Selektionsprozesse, Aufmerksamkeit, Kontrolle bei Erwachsenen")
    st.markdown("Topic_1 (24%): Forschung zum Wohlbefinden von Akteuren bezogen auf Themen wie Humor, Verspieltheit, Gelotophobie")
    st.markdown("Topic_2 (10%): Forschungsmethoden, Tests und Modellierungen in der Psychologie (Antwortzeiten, Motivation)")
    st.markdown("Topic_3 (17%): Psychologie der Erwachsenen bezogen einerseits auf Beziehungen mit anderen (etwa ausgelacht werden, Täuschungen) und andererseits auf eigene kognitive Dimensionen (Persönlichkeit, Depression)")
    st.markdown("Topic_4 (30%): Sozialpsychologische Themen (Zuschreibungen, Wahrnehmungen, Stereotypen, Glauben) im Bezug auf Alterung mit kognitiven Folgen und aktuelle gesellschaftliche Themen (wie etwa Klimawandel)")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Kontexte um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.markdown("Wandel, change(s), Veränderung(en): in allen Topics")
    st.markdown("Digitalisierung: bes. Topic_4")
    st.markdown("knowledge: bes. Topic_0 und Topic_2")
    st.image("Final/PSY.pdf-1.png",width=1400)

elif button == 'Soziologie':
    df_eng = pd.read_csv('Final/SOZ.csv')
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

    st.markdown("Topic_0 (19%): Relationale Soziologie und Differenzierungstheorien bes. im Bereich der Kunst (bes. digitalen Kunst) und der Chancengleichheit vor (Hoch)Schulen im internationalen Vergleich")
    st.markdown("Topic_1 (27%): Bildungsforschung zur Akademisierung und Hochschulexpansion bes. in Deutschland; Familien- und Gesundheitssoziologie mit Praxis- und Interventionsbezügen")
    st.markdown("Topic_2 (17%): Institutionalisierungstheorien und Erziehungstheorien mit Brücken zwischen Ausbildungssystem und Arbeitsmarkt und mit Bezug auf Emotionen und Gefühlen")
    st.markdown("Topic_3 (37%): Soziologie von kleineren Kontexten in sozialstrukturellen Perspektiven (Kommunen, Kreisen), Migrationssoziologie, Soziologie der digitalen Welt mit Bezug auf relationale Perspektiven")

    st.bar_chart(df_1[column])

    st.markdown("<h4 style='text-align: left; color: YellowGreen;'>Kontexte um Transformation, Nachhaltigkeit, Digitalisierung, Wissen</h4>", unsafe_allow_html=True)
    st.markdown("Wandel, change(s), Veränderung(en): in allen Topics")
    st.markdown("Bildung, knowledge, education: bes. Topic_1 und Topic_0")
    st.image("Final/SOZ.pdf-1.png",width=1400)
