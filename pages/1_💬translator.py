from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

langs = ["Korean", "Japanese", "Chinese", 
         "English", "Italian", "French", "Spanish", 
         "Russian", "Vietnamise"]  #번역 언어를 나열

st.set_page_config(page_title="언어 번역 서비스", page_icon="💬")
st.header('언어 번역 서비스')

left_co, cent_co, right_co = st.columns(3)

#웹페이지 왼쪽에 언어를 선택할 수 있는 라디오 버튼 
with st.sidebar:
     language = st.radio('번역을 원하는 언어(출력)를 선택해주세요.:', langs)

prompt = st.text_area('번역을 원하는 텍스트를 입력하세요(언어 자동감지)')  #사용자의 텍스트 입력

trans_template = PromptTemplate(
    input_variables=['trans'],
    template='Your task is to translate this text to ' + language + '\nTEXT: {trans}'
)  

llm = ChatOpenAI(model_name='gpt-4o-mini', temperature=0.0)

trans_chain = LLMChain(
    llm=llm, prompt=trans_template, verbose=True, output_key='translate')

# 프롬프트(trans_template)가 있으면 이를 처리하고 화면에 응답을 작성
if st.button("번역"):
    if prompt:
        response = trans_chain({'trans': prompt})
        st.info(response['translate'])