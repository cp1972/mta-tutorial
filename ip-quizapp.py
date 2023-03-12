import streamlit as st

st.set_page_config(layout="wide") # um die Webseite breiter zu machen

st.markdown("<h1 style='text-align: center; color: orange;'>Quiz zur Chemiepräsentation</h1>", unsafe_allow_html=True) # Haupttitel zentriert in orangen Farbe

st.sidebar.title("Willkommen zur Quiz!") # Menu links

### Session_state -- erlaubt das Speichern von Ergebnissen per Sitzung mit dem Quiz

if 'results' not in st.session_state:
    st.session_state.results = 0
if 'mylist' not in st.session_state:
    st.session_state.mylist = []

### Auswahl der Fragen im Menü

button = st.sidebar.radio("Beantworte die folgenden Fragen. Vorsicht! Es sind manchmal eine, manchmal mehrere Antworten möglich", ('Bedeutung von LNG', 'Ort LNG-Terminals', 'Anzahl LNG-Terminals', 'Transport LNG', 'Umwandlung LNG', 'Vor- bzw. Nachteile der Umwandlung von LNG', 'Lieferanten von Erdgas nach Deutschland', 'Verhalten Tschechien', 'Ergebnis'))

### Formulierung der Fragen, Auswahlmöglichkeiten und Speichern der Ergebnisse
if button == 'Bedeutung von LNG':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Was bedeutet LNG?")
        check_1 = st.checkbox("Liquid Natural Gasoline")
        check_2 = st.checkbox("Liquified Natural Gas")
        check_3 = st.checkbox("Liquified Naturalised Gaspipeline")
        if check_1 == True and check_2 == False and check_3 == False:
            st.session_state.results += 1
        else:
            st.session_state.results += 0

        st.form_submit_button("Antwort aufnehmen")

elif button == 'Ort LNG-Terminals':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Wo gibt es bereits LNG-Terminals in Deutschland?")
        check_4 = st.checkbox("Ilmenau")
        check_5 = st.checkbox("München")
        check_6 = st.checkbox("Bielefeld")
        check_7 = st.checkbox("Stade")
        if check_4 == False and check_5 == False and check_6 == False and check_7 == True:
            st.session_state.results += 1
        else:
            st.session_state.results += 0

        st.form_submit_button("Antwort aufnehmen")

elif button == 'Anzahl LNG-Terminals':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Wie viele LNG-Terminals wurden bereits gebaut?")
        check_8 = st.checkbox("1")
        check_9 = st.checkbox("2")
        check_10 = st.checkbox("3")
        check_11 = st.checkbox("Keine")
        if check_8 == False and check_9 == True and check_10 == False and check_11 == False:
            st.session_state.results += 1
        else:
            st.session_state.results += 0

        st.form_submit_button("Antwort aufnehmen")

elif button == 'Transport LNG':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Wie transportiert man das LNG?")
        check_12 = st.checkbox("Durch Zug")
        check_13 = st.checkbox("Durch Piplines")
        check_14 = st.checkbox("Durch Schifftransport")
        check_15 = st.checkbox("Durch Flugzeuge")
        if check_12 == False and check_13 == True and check_14 == True and check_15 == False:
            st.session_state.results += 2
        elif check_12 == False and check_13 == False and check_14 == True and check_15 == False:
            st.session_state.results += 1
        elif check_12 == False and check_13 == True and check_14 == False and check_15 == False:
            st.session_state.results += 1
        else:
            st.session_state.results += 0

        st.form_submit_button("Antwort aufnehmen")

elif button == 'Umwandlung LNG':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Wie wandelt man Erdgas in LNG um?")
        check_16 = st.checkbox("Verflüssigung")
        check_17 = st.checkbox("Kompression")
        check_18 = st.checkbox("Abkühlung")
        if check_16 == False and check_17 == True and check_18 == True:
            st.session_state.results += 2
        elif check_16 == False and check_17 == False and check_18 == True:
            st.session_state.results += 1
        elif check_16 == False and check_17 == True and check_18 == False:
            st.session_state.results += 1
        else:
            st.session_state.results += 0

        st.form_submit_button("Antwort aufnehmen")

elif button == 'Vor- bzw. Nachteile der Umwandlung von LNG':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Gib einen Vor- und einen Nachteil der Umwandlung von Erdgas in LNG?")
        check_19 = st.checkbox("Verschmutzung")
        check_20 = st.checkbox("Infrastruktur überschaubar")
        check_21 = st.checkbox("Energieverlust")
        check_22 = st.checkbox("Niedriege Kosten")
        if check_19 == False and check_20 == True and check_21 == True and check_22 == False:
            st.session_state.results += 2
        elif check_19 == False and check_20 == False and check_21 == True and check_22 == False:
            st.session_state.results += 1
        elif check_19 == False and check_20 == True and check_21 == False and check_22 == False:
            st.session_state.results += 1
        else:
            st.session_state.results += 0

        st.form_submit_button("Antwort aufnehmen")

elif button == 'Lieferanten von Erdgas nach Deutschland':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Welche Länder beliefern Deutschland mit Erdgas zur Zeit?")
        check_23 = st.checkbox("Belgien")
        check_24 = st.checkbox("Dänmark")
        check_25 = st.checkbox("Katar")
        check_26 = st.checkbox("Marokko")
        check_27 = st.checkbox("Frankreich")
        check_28 = st.checkbox("Russland")
        check_29 = st.checkbox("Griechenland")
        check_30 = st.checkbox("Bhutan")
        if check_23 == True and check_24 == False and check_25 == True and check_26 == False and check_27 == True and check_28 == False and check_29 == False and check_30 == True:
            st.session_state.results += 4
        elif check_23 == False and check_24 == False and check_25 == True and check_26 == False and check_27 == True and check_28 == False and check_29 == False and check_30 == True:
            st.session_state.results += 3
        elif check_23 == True and check_24 == False and check_25 == False and check_26 == False and check_27 == True and check_28 == False and check_29 == False and check_30 == True:
            st.session_state.results += 3
        elif check_23 == True and check_24 == False and check_25 == True and check_26 == False and check_27 == False and check_28 == False and check_29 == False and check_30 == True:
            st.session_state.results += 3
        elif check_23 == True and check_24 == False and check_25 == True and check_26 == False and check_27 == True and check_28 == False and check_29 == False and check_30 == False:
            st.session_state.results += 3
        elif check_23 == False and check_24 == False and check_25 == False and check_26 == False and check_27 == True and check_28 == False and check_29 == False and check_30 == True:
            st.session_state.results += 2
        elif check_23 == False and check_24 == False and check_25 == False and check_26 == False and check_27 == False and check_28 == False and check_29 == False and check_30 == True:
            st.session_state.results += 1
        elif check_23 == False and check_24 == False and check_25 == False and check_26 == False and check_27 == True and check_28 == False and check_29 == False and check_30 == False:
            st.session_state.results += 1
        elif check_23 == False and check_24 == False and check_25 == True and check_26 == False and check_27 == False and check_28 == False and check_29 == False and check_30 == False:
            st.session_state.results += 1
        elif check_23 == False and check_24 == False and check_25 == True and check_26 == False and check_27 == False and check_28 == False and check_29 == False and check_30 == False:
            st.session_state.results += 1
        elif check_23 == True and check_24 == False and check_25 == False and check_26 == False and check_27 == False and check_28 == False and check_29 == False and check_30 == False:
            st.session_state.results += 1
        else:
            st.session_state.results += 0

        st.form_submit_button("Antwort aufnehmen")

elif button == 'Verhalten Tschechien':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Wieso drosselt Tschechien die Lieferung von LNG nach Deutschland?")
        check_31 = st.checkbox("Tschechien braucht Gas für sich selber")
        check_32 = st.checkbox("Tschechiens Regierung mag Deutschland nicht")
        check_33 = st.checkbox("Klimaaktivisten haben die Pipeline sabotiert")
        if check_31 == True and check_32 == False and check_33 == False:
            st.session_state.results += 1
        else:
            st.session_state.results += 0

        st.form_submit_button("Antwort aufnehmen")

### Ergebnis sehen und Vergleich mit Ergebnisse der anderen

elif button == 'Ergebnis':
    st.write('Ihr Ergebnis ist: ', str(st.session_state.results), ' Punkt/e von 14 möglichen Punkten')
    st.session_state.mylist.append(st.session_state.results)

    st.markdown('**Ihr Ergebnis im Vergleich**')

    st.bar_chart(st.session_state.mylist)
    st.session_state.results = 0
