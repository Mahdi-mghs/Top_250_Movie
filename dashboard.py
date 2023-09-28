import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Top 250 _Movies_ :movie_camera:')

movies = pd.read_csv('Datas/movies.csv')

st.header('Choose :rainbow[Yourself]')
st.subheader('Movies By :orange[Year] :book:')
begin = st.number_input('begin from', 1921)
end = st.number_input('to', max_value=2023, min_value=2000)

filter1 = movies['year'] > begin
filter2 = movies['year'] < end
result_df = movies.where(filter1 & filter2).dropna()
st.dataframe(result_df)

st.divider()
###################

st.subheader('Movies By :gray[Ruintime] :watch:')
t_begin = st.number_input('begin from', 80)
t_end = st.number_input('to', max_value=220, min_value=100)

filter1 = movies['runtime'] > t_begin
filter2 = movies['runtime'] < t_end
result_time_df = movies.where(filter1 & filter2).dropna()

st.dataframe(result_time_df)

st.divider()
###################

person = pd.read_csv('Datas/person.csv', names=['person_id', 'name'])
cast = pd.read_csv('Datas/cast.csv', names=['ind', 'movie_id', 'person_id'])

pivot = person.join(cast.set_index('person_id'), on='person_id').join(movies.set_index('movie_id'), on='movie_id')

pivot = pivot.drop(['ind', 'movie_id', 'person_id'], axis=1).dropna().reset_index(drop=True)

st.subheader('Movies By :blue[Actor] :dancer:')
names = st.text_input('Enter your character name:(seprated by ",")', 'Matthew McConaughey', max_chars=128)
names = names.split(',')

filters = []
for name in names:
    name = name.strip()
    filters.append(name)

final = pivot.iloc[0:0]
for actor in filters:
    final =  pd.concat([final, pivot[pivot['name'] == actor]])

st.dataframe(final.reset_index(drop=True))

st.divider()
###################

genre = pd.read_csv('Datas/genre_movie.csv', names=['ind', 'movie_id', 'genre'])

pivot1 = genre.join(movies.set_index('movie_id'), on='movie_id')

pivot1 = pivot1.drop(['ind', 'movie_id'], axis=1).dropna()

st.subheader('Movies By _Genre_ :knife:')
gen_name = st.text_input('Enter your Genre', 'Action', max_chars=16)

genre_df = pivot1.where(pivot1['genre'] == gen_name)

st.dataframe(genre_df.dropna())

st.divider()
####################################################################

st.header('Movies $Chart$ :chart_with_upwards_trend:', divider='rainbow')
st.subheader('Top 10 :star:')
top_10 = movies.sort_values(by='gross_us', ascending=False).head(10)

st.bar_chart(top_10, x='title', y='gross_us')

###################

top_actor = pivot.groupby(by='name').count()['title'].sort_values( ascending=False)
top_actor = pd.DataFrame(top_actor.head(5))
top_actor.reset_index(inplace=True)
top_actor.columns = ['Name', 'Play Movies']

st.subheader('Top 5 Actor :tophat:')
st.bar_chart(top_actor, x='Name', y='Play Movies')

###################

pie_gen = genre.groupby(by='genre').count()['movie_id']
pie_gen = pd.DataFrame(pie_gen)
pie_gen.reset_index(inplace=True)
pie_gen.columns = ['Name', 'Count Movies']
li_gen = pie_gen['Name']
li_size = pie_gen['Count Movies']
fig, axe = plt.subplots()
axe.pie(li_size, labels=li_gen)
fig.set_size_inches(15, 15)
st.subheader('Pie Chart _Genres_ :cake:')
st.pyplot(fig=fig)

###################

pie_parent = movies.groupby(by='parental_guide').count()['movie_id']
pie_parent = pd.DataFrame(pie_parent)
pie_parent.reset_index(inplace=True)
pie_parent.columns = ['Name', 'Count Parental']
li_paren = pie_parent['Name']
li_size_paren = pie_parent['Count Parental']
fig1, axe1 = plt.subplots()
axe1.pie(li_size_paren, labels=li_paren)
fig1.set_size_inches(15, 15)
st.subheader('Pie Chart _Parntal Guide_ :underage:')
st.pyplot(fig=fig1)

###################

gen_movie = pivot1.groupby(by=['genre', 'parental_guide']).count()['title']
gen_movie = pd.DataFrame(gen_movie)
gen_movie.reset_index(inplace=True)
gen_movie.columns = ['genres', 'parental_guide', 'count_guide']
st.subheader('BarChart _Genres_')
st.bar_chart(gen_movie, x='genres', y='count_guide', color='parental_guide')

####################################################

st.header('Top Sales In $Genre$ :money_with_wings:')
gen_t = st.text_input('Enter your Genres:', 'Drama', max_chars=16)
top_in_gen = pivot1[pivot1['genre'] == gen_t].dropna()
top_in_gen.sort_values(by='gross_us', ascending=False, inplace=True)
st.bar_chart(top_in_gen.head(10), x='title', y='gross_us', color='#ffaa00')

####################################################
crew = pd.read_csv('Datas/crew.csv', names=['ind', 'movie_id', 'person_id', 'role'])

testt  = person.merge(crew.set_index('person_id'), on='person_id').merge(movies.set_index('movie_id'), on='movie_id').dropna()
testt = testt.merge(genre.set_index('movie_id'), on='movie_id')
testt = testt[testt['role'] != 'Director']

st.header('Suggestion Movies :magic_wand:')
name_m = st.text_input('Enter Your Movie Name:', 'The Shawshank Redemption')
cust_tb = testt[testt['title'] == name_m]
gen_se = cust_tb['genre'].drop_duplicates()
wri_se = cust_tb['name'].drop_duplicates()

filter_wr = testt['name'].isin(wri_se)
filter_gen = testt['genre'].isin(gen_se)
final_sug = testt.where(filter_wr | filter_gen).dropna()
final_sug = final_sug.drop(['person_id', 'ind_x', 'role', 'ind_y'], axis=1).drop_duplicates(['title']).reset_index(drop=True)
st.text('My Suggestion Is:')
st.dataframe(final_sug[final_sug['title'] != name_m])