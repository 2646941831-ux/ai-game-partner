import streamlit as st

#设置页面配置项
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    #整个布局
    layout="wide",
    #控制的是侧边栏
    initial_sidebar_state="expanded",
    #菜单
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title("streamlit入门教学")
st.header("streamlit一级标题")
st.subheader("streamlit二级标题")

st.write("hello im peter park")

st.image("./resources/cat.jpg",width=500)

st.audio("./resources/news.mp3",format="wav")

st.video("./resources/news.mp4")

st.logo("./resources/logo.png")

student_data={"姓名":["张子睿","萧炎","陈平安","熊大"],
              "学号":["202402810749","202402810750","202402810751","202402810752"],
              "总成绩":["650","750","650","666"]
              }
st.table(student_data)

name=st.text_input("请输入姓名")
st.write(f"您输入的名字为：{name}",)

password=st.text_input("请输入密码",type="password")
st.write(f"您输入的密码为：{password}",)

gender=st.radio("请输入您的性别：",["male","female"],index=0)
st.write(f"您的性别为：{gender}")