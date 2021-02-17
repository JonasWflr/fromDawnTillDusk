import streamlit as st
import altair as alt
import datetime
import pandas as pd
import numpy as np
from io import StringIO
import requests

# STREAMLIT ADJUSTMENTS
st.set_page_config(
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
	page_title='Dawn Till Dusk',  # String or None. Strings get appended with "• Streamlit".
	page_icon=':hibiscus:'  # String, anything supported by st.image, or None.
)
# hide hamburger menu (top right) and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

###############################################
# Definitions

site_width=400

color_all = alt.Color('Geschlecht',
        title="",
        scale=alt.Scale(
            domain=['Herr','Frau'],
            range=['#f2b713','#f2dc13'] # orange / yellow
            #range=['#ff66b3','#ff99cc'] # Klaebo style
            #range=['#ff9900','#ff6600']
        ),
        legend=None
    )

tooltip_all = [alt.Tooltip('id',title=None),
        alt.Tooltip('Km',format=',.0f'),
        alt.Tooltip('Höhenmeter',format='.0f')
    ]

#####################################################################################
# READ Dummy DATA
#df_data_dummy = pd.read_excel("./test_data.xlsx",engine="openpyxl")#, skiprows=2,nrows=20)
def fill_with_dummy_data(df):
    # fill with dummy data to show plots
    df['Km'] = np.random.randint(80, 200, df.shape[0])
    df['Höhenmeter'] = np.random.randint(500, 2000, df.shape[0])
    return(df)

# READ FROM GOOGLE
st.cache(ttl=60*1)
def read_data():
    GOOGLE_SPREADSHEET = 'https://docs.google.com/spreadsheets/d/1mV3lzutv90A3xjoTANt1-qg7XxZ-8-7LkgdfldQr8CA/gviz/tq?tqx=out:csv'
    response = requests.get(GOOGLE_SPREADSHEET)
    assert response.status_code == 200, 'Wrong status code'
    response_string = response.content.decode('utf-8')
    TEST = StringIO(response_string)
    df_data_google = pd.read_csv(TEST, sep=',')
    return(df_data_google)

# SHOW THE TEXT, WHAT IS IT ETC.
def show_infos():
    st.title('__Format/Details:__')

    st.write('''
    __Datum:__ 6.3.2021\n
    __Start:__ 06.49\n
    __Zielschluss:__ 18.13\n
    __Technik:__ frei wählbar

    __Sieger*in__: Wer am __meisten Kilometer__ läuft in dieser Zeit.
    Du bist eher der Typ "Bergfloh"? Dann laufe so viele __positiv Höhemeter__ wie du kannst und sichere dir den ersten Rang in der Kategorie "Bergpreis".\n
    __Kategorien:__ Frauen, Männer

    __Spezialwertung:__ Team Schweden vs. Team Doppelstock; weitere Battles sind gerne gesehen ;)

    __Messung:__ jede\*r Läufer\*in misst die Kilometer selbst mit einem Gerät/App nach Wunsch.

    __Reporting:__ Kilometer, Höhenmeter und Lauftechnik per Text/Whatsapp/etc an Michael +41 (0)79 961 73 12 bis um 20.00 Uhr am Tag des Rennens (6.3.2021) senden. 

    Bei Anregung oder Fragen, meldet euch einfach im Chat. 

    Wir freuen uns auf einen grossartigen Lauf!

    ''')

# SHOW COMPLETE RESULTS WITH PLOTS
def show_plots(df_selected):
    # RADIO
    st.title('__Resultate__')
    sex = st.radio('',('alle','Frau','Herr'))
    if(sex=='alle'):
        df_selected = df_selected
    else:
        df_selected = df_selected[df_selected['Geschlecht']==sex]
        #df_selected = df_data

    ###########################
    # DISTANCE
    st.header(':straight_ruler: __Distanz__')
    chart_distance = alt.Chart(
        df_selected#.sort_values(by='Km',ascending=False)
    ).mark_bar().encode(
        x='Km:Q',
        y=alt.Y('id',sort='-x',title=None),
        color= color_all,
        tooltip= tooltip_all
    )
    st.altair_chart(chart_distance, use_container_width=True)

    ###########################
    # ALTITUDE
    st.header(':snow_capped_mountain: __Höhenmeter__')
    chart_altitude = alt.Chart(
        df_selected
    ).mark_bar().encode(
        y='Höhenmeter:Q',
        x=alt.X('id', sort='-y',title=None),
        color= color_all,
        tooltip= tooltip_all
    )
    st.altair_chart(chart_altitude, use_container_width=True)

    ###########################
    # COMBINED
    st.header(':muscle: __Kombiniert__')
    chart_combined = alt.Chart(
        df_selected
    ).mark_circle().encode(
        y='Höhenmeter:Q',
        x=alt.X('Km'),
        color=color_all,
        size=alt.Size('Km', scale=alt.Scale(range=[100, 500]), legend=None),
        tooltip= tooltip_all
    )
    st.altair_chart(chart_combined, use_container_width=True)

#################
# CHOOSE DATE
today = datetime.date.today()
# for testing:
#today = datetime.date(2021,3,7)
#st.write(today)
date_race = datetime.date(2021,3,6)
remaining_days = (date_race -today).days
df_data_google = read_data()
df_selected = df_data_google
# if remaining_days>0:
#     date = st.sidebar.radio('Navigation',('heute','postrace'),0)
#     if(date=='postrace'):
#         today_selected = datetime.date(2021, 3, 7)
#         #df_selected = fill_with_dummy_data(df_data_google)#df_data_dummy
#         df_selected = df_data_google
#         #st.header('Die Plots zeigen Dummydaten')
#     else:
#         today_selected = datetime.date.today()
#         df_selected = df_data_google
# else:
#     date = st.sidebar.radio('Navigation', ('prerace','heute'), 1)
#     if (date == 'prerace'):
#         today_selected = datetime.date(2021, 3, 5)
#         df_selected = df_data_google
#     else:
#         today_selected = today
#         df_selected = df_data_google
#st.write('today {}'.format(today_selected))
#remaining_days = (date_race -today_selected).days

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# define id and set as index
df_selected['Technik'] = df_selected['Technik'].fillna(value='Skating')
df_selected['id'] = df_selected['Vorname']+' '+df_selected['Name']
df_selected = df_selected.set_index('id',drop=False)

#####################################################################################
#####################################################################################
#####################################################################################

# IMAGE
st.image('banner_dawn_till_dusk.jpeg', width=site_width, use_column_width='always')

# SHOW GENERAL RULES AND INFOS
show_infos()

if(remaining_days)>0:
    #st.header('\n\n\n Nur noch {} Mal schlafen!\n\n'.format(remaining_days))
    st.info('\n\n__Nur noch {} Mal schlafen!__\n\n'.format(remaining_days))
    st.write('Noch nicht angemeldet? [Melde dich jetzt an!](http://bit.ly/3pg5KX3)')

    st.subheader('Angemeldet sind momentan {} Langläufer*innen'.format(df_selected['id'].count()))
    for id in df_selected['id']:
        st.write(id)

# SHOW THE RESULTS AND PLOTS
show_plots(df_selected)
##############################################################################
# FOOTER

st.info(""":palm_tree: :hibiscus: :palm_tree: :hibiscus: :palm_tree: :hibiscus: :palm_tree: :hibiscus: :palm_tree: :hibiscus: :palm_tree:

Mehr Infos gibt es in unserer WhatsApp-Gruppe.
""")