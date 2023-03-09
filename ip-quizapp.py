import streamlit as st

# Seite Layout

st.set_page_config(layout="wide") # um die Webseite breiter zu machen

st.markdown("<h1 style='text-align: center; color: orange;'>Quiz</h1>", unsafe_allow_html=True) # Haupttitel zentriert in orangen Farbe

st.sidebar.title("Willkommenstext") # Menu links

### Session_state -- erlaubt das Speichern von Ergebnissen per Sitzung mit dem Quiz

if 'results' not in st.session_state:
    st.session_state.results = 0
if 'mylist' not in st.session_state:
    st.session_state.mylist = []

### Auswahl der Fragen im Menü

button = st.sidebar.radio("Bittte wählen Sie die Fragen aus", ('Frage 1', 'Frage 2', 'Frage 3', 'Ergebnis'))

### Formulierung der Fragen, Auswahlmöglichkeiten und Speichern der Ergebnisse

if button == 'Frage 1':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Formulierung der Frage")
        check_1 = st.checkbox("Antwort-1")
        check_2 = st.checkbox("Antwort-2")
        if check_1 == True:
            st.session_state.results += 1

        st.form_submit_button("Antwort aufnehmen")

elif button == 'Frage 2':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Formulierung der Frage")
        check_3 = st.checkbox("Antwort-3")
        check_4 = st.checkbox("Antwort-4")
        if check_3 == True:
            st.session_state.results += 1

        st.form_submit_button("Antwort aufnehmen")

elif button == 'Frage 3':
    with st.form("checkboxes", clear_on_submit = True):
        st.markdown("Formulierung der Frage")
        check_5 = st.checkbox("Antwort-5")
        check_6 = st.checkbox("Antwort-6")
        if check_5 == True:
            st.session_state.results += 1

        st.form_submit_button("Antwort aufnehmen")

### Ergebnis sehen und Vergleich mit Ergebnisse der anderen

elif button == 'Ergebnis':
    st.write('Ihr Ergebnis ist: ', str(st.session_state.results), ' Punkt/e von 10 möglichen Punkten')
    st.session_state.mylist.append(st.session_state.results)

    st.markdown('**Ihr Ergebnis im Vergleich**')

    st.bar_chart(st.session_state.mylist)
    st.session_state.results = 0
