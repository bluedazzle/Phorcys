# Phorcys API

标签（空格分隔）： api

---

**host: http://Phorcys.com**

**api_version: v1**

#概要

 2. API请求格式：host + "api" + api_version + 请求地址。
 3. API返回格式：`json:{"status":1,"body":{}}`status返回操作结果码,body包含返回信息，如果无返回信息，body为空。
 4. status结果码对照表：
|status结果码|状态|
| --------------  | :---: |
|0|未知错误|
|1|成功|
|2|权限不足|
|3|帐号不存在|
|4|数据错误|
|5|密码错误|
|6|已存在|
|7|不存在|
|8|已过期|
|10|验证码为空|
|11|验证码错误| 


#API安全

为保证接口调用安全，所有接口都需要：`timestamp`与`sign`两个参数，用来验证接口请求的合法性。其中： 


 1. `timestamp`是类型为数字的10位的时间戳，代表发生请求时的时间。
 2. `sign` 是类型为字符串的32位验证字符串，具体生成方式为`MD5(timestamp + secret)`，其中`secret` 从系统申请后分配。请保证`secret` 的安全性，如果不慎泄露请及时更换。
 3. 验证合法性请均使用`get`方式构造参数请求，即在所有请求地址后构造类似`?timestamp=xx&sign=xx`的参数

#文档

#用户
##**获取注册验证码**
```
POST /verify
```
###**Parameters**
* phone(_Required_|string)-手机号
* type(_Optional_|integer)-验证码类型，默认为1

|type类型码|含义|
| - | :-: |
|1|注册|
|2|找回密码|
###**Return**
成功
```
{
  "body": {},
  "status": 1,
  "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "请求短信时间间隔过短"
}

{
  "body": {},
  "status": 4,
  "msg": "请输入11位手机号"
}

{
  "body": {},
  "status": 4,
  "msg": "请输入手机号"
}
```

##**验证注册验证码**
```
GET /verify
```
###**Parameters**
* phone(_Required_|string)-手机号
* code(_Required_|string)-验证码
* type(_Optional_|integer)-验证码类型，默认为1

|type类型码|含义|
| - | :-: |
|1|注册|
|2|找回密码|
###**Return**
成功
```
{
  "body": {},
  "status": 1,
  "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "数据缺失"
}

{
  "body": {},
  "status": 10,
  "msg": "请获取验证码"
}

{
  "body": {},
  "status": 11,
  "msg": "验证码不正确"
}

```

##**用户注册**
```
POST /user/register
```
###**Parameters**
* phone(_Required_|string)-手机号
* password(_Required_|string)-密码
* nick(_Required_|string)-昵称
###**Return**
成功
```
{
  "body": {
    "nick": "2333",
    "token": "pBgtwFXgCuN0GnsPOnbfe9paDfbyK2qM1vjoYhHdIloRem7icEZzkltarLx8WwvV",
    "create_time": 1460382192,
    "id": 7,
    "phone": "18212666355"
  },
  "status": 1,
  "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "帐号已存在"
}
```

##**用户登陆**
```
POST /user/login
```
###**Parameters**
* phone(_Required_|string)-手机号
* password(_Required_|string)-密码
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**用户忘记密码**
```
PUT /user/password
```
###**Parameters**
* phone(_Required_|string)-电话号码
* verify(_Required_|string)-验证码
* new_password(_Required_|string)-新密码
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**用户修改密码**
```
PATCH /user/password
```
###**Parameters**
* token(_Required_|string)-用户识别码
* password(_Required_|string)-旧密码
* new_password(_Required_|string)-新密码
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**用户登出**
```
POST /user/logout
```
###**Parameters**
* token(_Required_|string)-用户识别码
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

#资讯

##**获取资讯列表**
```
GET /news/?[@page]
```
###**Return**
```
{
  "body": {
    "paginator": null,
    "page_obj": {},
    "news_list": [
      {
        "content": "test",
        "modify_time": 1460173491,
        "create_time": 1460173491,
        "id": 1,
        "title": "test"
      },
      {
        "content": "test1",
        "modify_time": 1460173799,
        "create_time": 1460173799,
        "id": 2,
        "title": "test1"
      },
      {
        "content": "大西瓜",
        "modify_time": 1460357753,
        "create_time": 1460357753,
        "id": 3,
        "title": "大西瓜"
      }
    ],
    "is_paginated": false,
    "view": null
  },
  "status": 1,
  "msg": "success"
}
```

##**获取资讯详情**
```
GET /news/[@news_id]
```
###**Return**
```
{
  "body": {
    "news": {
      "content": "大西瓜",
      "title": "大西瓜",
      "create_time": 1460357753,
      "id": 3,
      "modify_time": 1460357753
    },
    "view": null
  },
  "status": 1,
  "msg": "success"
}
```

##**获取资讯评论**
```
GET /news/[@news_id]/comment
```
###**Return**
```
{
  "body": {
    "paginator": null,
    "newscomment_list": [
      {
        "content": "post comment",
        "create_time": 1460356933,
        "thumb": 0,
        "id": 18
      },
      {
        "content": "post comment",
        "create_time": 1460358306,
        "thumb": 0,
        "id": 22
      },
      {
        "content": "post comment",
        "create_time": 1460358644,
        "thumb": 0,
        "id": 24
      }
    ],
    "page_obj": {},
    "is_paginated": false,
    "view": null
  },
  "status": 1,
  "msg": "success"
}
```


#社区

##**获取社区列表**
```
GET /bbs/?[@page]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**获取帖子详情**
```
GET /bbs/detail/[@bbs_id]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**新建帖子**
```
GET /bbs/new
```
###**Parameters**
* token(_Required_|string)-用户识别码
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

#关注

##**搜索关注**
```
GET /focus/player/search
```
###**Parameters**
* content(_Required_|string)-搜索内容
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**关注/取关选手**
```
PATCH /focus/player/[@player_id]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**获取关注选手资讯列表**
```
GET /focus/news/[@page]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**获取关注选手资讯详情**
```
GET /focus/news/detail/[@news_id]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

#信息

##**获取战队列表**
```
GET /team/[@page]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**获取战队详情**
```
GET /team/detail/[@team_id]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**获取选手列表**
```
GET /player/[@page]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**获取战队详情**
```
GET /player/detail/[@player_id]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**获取联赛列表**
```
GET /tournament/[@page]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**获取联赛详情**
```
GET /tournament/detail/[@tournament_id]
```
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

#评论

##**评论**
```
POST /comment
```
###**Parameters**
* token(_Required_|string)-用户识别码
* type(_Required_|integer)-评论类型
* content(_Required_|string)-评论内容
* id(_Required_|integer)-被评论事件id

|type码|状态|
| - | :-: |
|1|资讯|
|2|社区|
|3|关注|
|4|联赛|
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```

##**点赞/取赞**
```
POST /thumb
```
###**Parameters**
* token(_Required_|string)-用户识别码
* type(_Required_|integer)-点赞类型
* id(_Required_|integer)-被赞事件id

|type码|状态|
| - | :-: |
|1|资讯|
|2|社区帖子点赞|
|3|社区评论点赞|
|4|关注点赞|
|5|联赛评论点赞|
###**Return**
```
{"status":1,"body":{}, "msg": "success"}
```