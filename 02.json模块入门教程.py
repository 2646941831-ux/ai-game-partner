import json
#写入json数据文件
# user = {
#     "name":"涛哥",
#     "age" : 18,
#     "gender":"男",
#     "hobbies":["reading","swimming"]
# }
# with open("resources/user.json","w",encoding="utf-8") as f:
    #ensure_ascii默认为true,表示不支持中文，设置为false则支持中文
    #indent表示在json数据中添加缩进
    # json.dump(user,f,ensure_ascii=False,indent=2)
#读取json数据文件
with open("resources/user.json","r",encoding="utf-8") as f:
    user=json.load(f)
    print(user)
    print(type(user))
