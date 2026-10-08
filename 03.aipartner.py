import streamlit as st
import os
from openai import OpenAI


print("-------------->重新执行此文件，渲染展示页面")
st.set_page_config(
    page_title="AI Partner",
    page_icon="🐻‍❄️",
    #整个布局
    layout="wide",
    #控制的是侧边栏
    initial_sidebar_state="expanded",
    #菜单
    menu_items={
   }
)
#标题
st.title("AI Partner")
#logo
st.logo("./resources/logo.png")
#初始化大模型客户端
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
#系统提示词

system_prompt = "You are a helpful assistant"
#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state['messages'] = []
#展示聊天信息
for message in st.session_state.messages:
   st.chat_message(message["role"]).write(message["content"])

#聊天消息输入框
prompt=st.chat_input("What would you like to know?")
if prompt:#字符串会自动转换为布尔值，如果字符串不为空，则为True
    st.chat_message("user").write(prompt)
    print("-------------->调用大模型，提示词：",prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    print("-------------->大模型返回结果：",response.choices[0].message.content)
    st.chat_message("assistant").write(response.choices[0].message.content)
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    

    #调用大模型

