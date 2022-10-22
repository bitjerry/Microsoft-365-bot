# 开发文档

### 获取机器人所有命令

```python
# core.py
def cmd(self, command: str | Callable = ""):
    print(command)
    ...
```

### 订阅显示美化

> ./resource/name_for_sub.csv  
> [文件更新](https://learn.microsoft.com/en-us/azure/active-directory/enterprise-users/licensing-service-plan-reference)

### 本地化

[翻译文件 传送门>>>](../../src/resource/i18n/en_us.py)

不同语种翻译步骤:  

- 在 `i18n` 目录下新建一个 `.py` 文件, 文件名命名规范见[语言代码表](#语言代码表)
- 对照已有文件进行字符串本地化
- 变量名, 字符串内`{}`, 键盘 (`control`类列字典) 标号 (键) 禁止翻译

### 功能模块

> service模块功能建立于app模块之上    
> app模块与service模块并非一一对应的关系

#### app模块

> 每一个app模块对应一个Microsoft Graph API模块

- 在`app`目录下新建一个模块, 模板如下:  
```python
from util.request import *


class ModuleName(MsRequest):

    def __init__(self, request: Requests):
        super().__init__(request)
    
    def method(self, *args, **kwargs):
        self.req.get(...)
```
- 每个模块必须继承 [MsRequest >>>](#msrequest)   
- 微软API使用方法参考
[微软API文档](https://learn.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0) |
[API测试工具](https://developer.microsoft.com/zh-cn/graph/graph-explorer)  
- 调用方法: `app.ModuleName.method()`  
例: [用户创建文档]( https://docs.microsoft.com/en-us/graph/api/user-post-users?view=graph-rest-1.0&tabs=http)
```python
# 文档用例:
"""
POST https://graph.microsoft.com/v1.0/users
Content-type: application/json

{
  "accountEnabled": true,
  "displayName": "Adele Vance",
  "mailNickname": "AdeleV",
  "userPrincipalName": "AdeleV@contoso.onmicrosoft.com",
  "passwordProfile" : {
    "forceChangePasswordNextSignIn": true,
    "password": "xWwvJ]6NMw+bWH-d"
  }
}
"""
# App层对应代码:
def create(self, username: str, password: str):
    """
    :param password: user password
    :param username: xxx@domain.com
    :return:
    """
    display_name = username.split('@', 1)[0]
    json = {
        'accountEnabled': True,
        'displayName': display_name,
        'mailNickname': display_name,
        'passwordPolicies': 'DisablePasswordExpiration, DisableStrongPassword',
        'passwordProfile': {
            'password': password,
            'forceChangePasswordNextSignIn': True
        },
        'userPrincipalName': username,
        'usageLocation': 'CN'
    }
    res = self.req.post(url="/users", json=json)
    return res.json["id"]

#Service层调用方法
@bot.cmd("newuser")
@app_autowired
def create(msg: Message, app: App):
    app.User.create(username)
    ...
```


#### service模块

> 每一个service模块对应一类Telegram bot功能  
> 工具方法: [helper >>>](#helper)  
> 核心组件: [core >>>](#core)

- 在`service`目录下新建一个模块  
- 数据持久化
  - 新建`session = Session()`, 会话信息务必在`__init__`内初始化
  - 注册`session_util.register(session)` 
- 装饰器
    ```python
    #注册bot命令
    @bot.cmd("get")
    def get_cmd(msg: Message):
        ...
    #注册回调函数, 可以使用函数标识字符串作为参数
    @bot.callback
    def get(msg: CallbackQuery):
        ...
    #注入app
    @bot.cmd("adduser")
    @app_autowired
    def add_cmd(msg: Message, app: App):
        ...
    #bot启动时即触发
    @bot.on_startup
    def start():
        ...
    ```
- 键盘事件
    ```python
    buttons = [[Btn(text=text,
                    callback_data=callback_data,
                    callback_func=function)]]
    bot.send_msg(msg, Text.xxx, Keyboard(buttons))
    
    # text为按钮显示文本
    # callback_data为按钮触发后返回的数据, 多参数请使用列表, 则回调数据仍为列表
    # callback_func为按钮触发后触发的回调函数(必须事先注册), 可以为函数标识字符串
    # buttons即键盘按钮, 是一个二维数组, 第一维为列, 第二维为行
    ```
- 消息发送
    参考 [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
    ```python
    edit_msg(msg, text, keyboard, **keyword)
    send_msg(msg, text, keyboard, **keyword)
    send_doc(msg, doc, keyboard, **keyword)
    register_next_step(func, *args, **kwargs)
    ```
- 跨模块调用(尽量不要有相互调用)  
   - 信息传递
     - 跨模块传递`field`, `session_util.get(field)`
   - 回调方法
     - 使用字符串表示方法名


### util模块

### MsRequest

发起请求
```python

def get(url: str, headers: dict, params: dict) -> Response:
    ...

def post(url: str, headers: dict, params: dict, data: dict, json) -> Response:
    ...

def delete(url: str, headers: dict) -> Response:
    ...

def patch(url: str, headers: dict, data: dict, json) -> Response:
    ...
```
响应数据
- `ok`状态码,注意到如果请求不成功响应会抛出异常
- `text`响应文本,响应体
- `json`json格式响应数据

#### helper
> 为service模块方法提供便捷工具

- `session_util`:
  > 管理service下每个模块的子会话
  - get(): 
    - 功能: 用于跨模块获取会话参数
    - 参数:
      - var: session字段
  - set(): 
    - 功能: 用于跨模块修改会话参数(慎用, 可能会破坏数据一致性)
    - 参数: 
      - var: session字段
      - value: 修改的值
  - register():
    - 功能: 注册一个会话实例
    - 用法: register(session())
  - reset():
    - 功能: 重置所有会话, 这回导致bot显示没有相应对象
  
- `task`:
  > 守护线程, 用于执行所有延迟任务, 例如计时器
  - clear(): 
    - 功能: 清除所有任务
  - cancel(name): 
    - 功能: 清除指定任务
    - 参数: 任务名
  - delay(time_out, loop, name)
    - 功能: 注册一个延时任务
    - 用法: 作为装饰器
    - 参数:
      - time_out: 延迟事件
      - loop: 是否循环
      - name: 任务名字

- `Format`: 
  - 功能: json数据转yaml风格的html字符串
  - 用法: str(Format(json))

- `lock`:
  - 功能: 在设置了操作密码后, 要求用户对装饰的函数功能进行身份验证
  - 用法: 作为装饰器为函数加锁, 务必在bot装饰器之后, 因为是被动触发的

- `app_autowired`:
  - 功能: 为函数注入`app:App`参数, 而不是使用`app:App = app_pool.get(session_util.get("app_id"))`
  - 用法: 作为装饰器, 务必在bot装饰器之后, 因为这会使得函数减少一个参数

- `gen_control_keyboard`
  - 功能: 生成控制面板按钮, 即键盘
  - 用法: 生成一个`Keyboard`对象
  - 参数: 
     - btn_data: 按钮字典, 参见`i18n`下控制面板文本
     - btn_line: 按钮每行数量, 默认两个

- `gen_page_switch`
  - 功能: 生成一个上下页切换按钮
  - 用法: 生成一个包含上下页按钮的列表, `Keyboard([gen_page_switch(...)])`
  - 参数:
    - page_index: 页码
    - has_next_page: 是否有下一页

### 附录

#### 语言代码表
![lang.png](https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/lang.png)
