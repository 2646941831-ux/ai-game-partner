import streamlit as st
import os
from openai import OpenAI

print("-------------->重新执行此文件，渲染展示页面")
st.set_page_config(
    page_title="AI Partner",
    page_icon="🐻‍❄️",
    # 整个布局
    layout="wide",
    # 控制的是侧边栏
    initial_sidebar_state="expanded",
    # 菜单
    menu_items={
    }
)
# 标题
st.title("AI Partner")
# logo
st.logo("./resources/logo.png")
# 初始化大模型客户端
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
# 系统提示词

system_prompt = """
        你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。：
        规则：
            1. 每次只回1条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短，像微信聊天一样
            5. 有需要的话可以用❤️🌸等emoji表情
            6. 用符合伴侣性格的方式对话
            7. 回复的内容, 要充分体现伴侣的性格特征
        伴侣性格：
            - %s
        你必须严格遵守上述规则来回复用户。
    """
# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state['messages'] = []
#昵称
if "nickname" not in st.session_state:
    st.session_state.nickname="小甜甜"
#性格
if "nature" not in st.session_state:
    st.session_state.nature="活泼开朗的台湾女生"

# 展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
#左侧侧边栏-with是streamlit中上下文的管理器
with st.sidebar:
    st.subheader("伴侣信息")
    #昵称输入狂
    nickname=st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nickname)
    if nickname:
        st.session_state.nickname=nickname
    #性格输入框
    nature=st.text_area("性格",placeholder="请输入性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature=nature


# 聊天消息输入框
prompt = st.chat_input("What would you like to know?")
if prompt:  # 字符串会自动转换为布尔值，如果字符串不为空，则为True
    st.chat_message("user").write(prompt)
    print("-------------->调用大模型，提示词：", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    #调用大模型
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nickname, st.session_state.nature)},
            *st.session_state.messages,
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    response_message = st.empty()# 创建一个空的元素来显示响应
    full_response=""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content =chunk.choices[0].delta.content
            full_response+=content
            response_message.chat_message("assistant").write(full_response)

    print("-------------->大模型返回结果：", full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 调用大模型

