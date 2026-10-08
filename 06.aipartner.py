import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")
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
#保存会话信息函数
def save_session():

    if st.session_state.current_session:
        session_data={
            "current_session": st.session_state.current_session,
            "nickname": st.session_state.nickname,
            "nature": st.session_state.nature,
            "messages": st.session_state.messages
        }
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        filepath = os.path.join(SESSIONS_DIR, f"{st.session_state.current_session}.json")
        print(f"-------------->保存会话到: {filepath}")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

#加载所有列表会话信息
def load_sessions():
    session_lists = []
    #加载sessions目录下的所有文件
    if os.path.exists(SESSIONS_DIR):
        file_list = os.listdir(SESSIONS_DIR)
        for filename in file_list:
            if filename.endswith(".json"):
                session_lists.append(filename[:-5])
    return session_lists
#加载指定会话
def load_session(session_name):
    try:
        filepath = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            st.session_state.messages = session_data["messages"]
            st.session_state.nickname = session_data["nickname"]
            st.session_state.nature = session_data["nature"]
            st.session_state.current_session = session_name
    except Exception as e:
        st.error(f"加载会话失败: {e}")

#生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



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
#会话标识
if "session_id" not in st.session_state:
    st.session_state.current_session=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



# 展示聊天信息
st.text(f"会话名称：{st.session_state.current_session}")
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
#左侧侧边栏-with是streamlit中上下文的管理器
with st.sidebar:
    #会话信息：
    st.subheader("AI控制面板")
    #新建会话按钮：
    if st.button("新建会话", width="stretch", icon="📓"):
        #保存当前会话信息
        save_session()


        #创建新的会话
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()#重新运行这个页面
    #会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
            #加载会话信息
            #三元运算符：如果条件为真，则返回的是第一个值；否则，返回第二个值-->语法：值1 if 条件 else 值2
            if st.button(session,width="stretch",icon="📑",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("",width="stretch",icon="❌️",key=f"del_{session}"):
                pass



    #伴侣信息：
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
    save_session()
    # 调用大模型

