import streamlit as st
from rag_engine import load_base, ask_rag
st.set_pag_config(page_title = "SIET_chartbot",layer = "centered")
st.tittle("shedevi institute of engineering and technology-chartbot")
st.caption("ask any question  about college info....")
st.caption("IN by madhav")

mykey = st.secrets["GROQ_API_key"]


def initiate_rag():
  return load_base("01_College_Information.pdf")

  index, embed_module, chunks = initiate_rag() 

if "chat_hist" not in st.session_state:
  st.session_state.chat_hist = []
for qa in st.session_state.chat_hit :
  with st.chat_message(qa["role"]):
    st.write(qa["content"])

question = st.chart_input("ask any question  about college info....")

if question:
  st.session_state.chat_hist.append(
    {"role" :"user","content" = question})
  with st.chart_messages("user"):
    st.write(question)
  with st.chart_message("assistant"):
    with st.spinner("asking RAG for answer....."):
      answe = ask_rag(question,embed_modle,chunk,index,api_key = mykey)
      st.write(answer)
       st.session_state.chat_hist.append(
         {"role":"assistant", "content" : answer})
if st.button("clear chat"):
   st.session_state.chat_hist = []
   st.return()
   

      
  
