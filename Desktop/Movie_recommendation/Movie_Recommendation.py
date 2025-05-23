import streamlit as st
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
os.environ["GOOGLE_API_KEY"]="AIzaSyBBA1BukryY3YxXJRVAJOqlkrsWOR2v4BE"
llm=GoogleGenerativeAI(model="models/gemini-2.0-flash",temperature=0.7)
prompt_template_name=PromptTemplate(
    input_variables=['language','genre','choice'],
    template="Recommend Top 10 {choice} {language} movies of {genre} genre  with release year in one line and basic info about movie in next line and cast details(hero,heroine,director and producer) in well ordered(understandable) without cast heading in next line.Display them one after another without any extra information"
)
chain=LLMChain(llm=llm,prompt=prompt_template_name)


st.title("🎬 Movie Recommendation App")
languages = ["English", "Telugu", "Hindi", "Tamil", "Kannada"]
language = st.selectbox("Choose a language", languages)

genres = ["Action", "Comedy", "Drama", "Romance", "Adventure", "Thriller"]
genre = st.selectbox("Choose a genre", genres)

filters = ["Top Rated", "Recent"]
filter_option = st.radio("Choose recommendation type", filters)

if st.button("Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        result = chain.run({
            "language": language,
            "genre": genre,
            "choice": filter_option
        })
        st.subheader(f"{filter_option} {language} {genre} Movies")
        movies=result.strip().split("\n\n")
        for movie in movies:
            details=movie.strip().split("\n")
            length=len(details)
            if length>=3:
                name=details[0]
                info=details[1]
                cast=details[2]
                with st.expander(f"🎬{name}"):
                    st.markdown(f"**Description: {info}")
                    st.markdown(f"**Cast: {cast}")
            else:
                st.write(movie)
