# ReAct Agent 방식
# 외부 정보 검색 기능 추가, 원달러 환율을 알려줄 수 있음
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
# 추가
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.utilities import PythonREPL
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.agents import Tool, load_tools, create_react_agent, AgentExecutor

# 외부 검색 가능한 도구를 추가한 AgentExcutor 생성
def create_agent_chain():
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    
    tavily_tool = TavilySearchResults(k=5)
    
    python_repl = PythonREPL()
    python_repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. \
        Input should be a valid python command. \
        If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    )
    
    tools = [tavily_tool, python_repl_tool]
    
    prompt = hub.pull("hwchase17/react")
    
    llm = ChatOpenAI(model_name='gpt-4o-mini', temperature=0, streaming=True)
    
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools) # AgentExecutor 리턴


st.set_page_config(page_title="온라인 챗봇", page_icon="🌐", layout='wide')
st.header('온라인 챗봇')

# chat history
if('app_name' not in st.session_state):
    st.session_state.app_name = 'online_chatbot'
elif(st.session_state.app_name != 'online_chatbot'):
    st.session_state.app_name = 'online_chatbot'
    StreamlitChatMessageHistory().clear();

history = StreamlitChatMessageHistory() 

for message in history.messages:
    st.chat_message(message.type).write(message.content)

query = st.chat_input("하고 싶은 말")

if query:
    with st.chat_message("user"):
        history.add_user_message(query)
        st.markdown(query)

    with st.chat_message("assistant"):
        callback = StreamlitCallbackHandler(st.container())
        agent_chain = create_agent_chain()
        response = agent_chain.invoke(
            {"input": query},
            {"callbacks": [callback]},
        )
        #messages = [HumanMessage(content=query)]  # 삭제
        #response = llm.invoke(messages)            # 삭제
        history.add_ai_message(response["output"])
        st.markdown(response["output"])  # agent_chain의 응답이므로 변경

# 문제점: 기억이 없음. 내 이름을 알려줘도 모름. 1 to 50 게임도 못함.