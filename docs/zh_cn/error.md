# 常见问题

### ORM的错误

当你使用不同数据库时, 可能会出现运行错误. 
orm中包含了一些数据库的默认驱动, 但仍可能出现错误找不到xxx. 
此时请手动安装需要的数据库驱动包, `pip install xxx`  
或者将包写到`requirements.txt`中

### 命令不响应

如果是个别情况, 请到readme文档中对照命令列表. 在项目更新后, 可能会有新命令加入, 一般对现有命令不会进行修改, 除非大版本更新.  
如果大部分都无法响应, 请使用`/log`查看机器人日志

### InvalidAuthenticationToken

在切换新的app时, 立刻发起请求可能会出现
> {'error': {'code': 'InvalidAuthenticationToken', 'message': 'CompactToken parsing failed with error code: 80049217', 'innerError': {'date': '2022-09-26T15:00:36', 'request-id': '2e1dfda1-63f2-4c23-a584-df45cb282b03', 'client-request-id': '2e1dfda1-63f2-4c23-a584-df45cb282b03'}}}

这个问题应该属于微软的api. 
已知如果同样的app已经请求过token, 再请求新的token并不是立即生效的, 只需要稍等一会儿 
程序在加载了app后才会兑换token, 待过期后重新刷新, 考虑到可能用户有最多全局, 
因此无法将所有app一次性加载到app池中, 所以token是懒加载的

### Insufficient privileges to complete the operation

1. 先检查API权限是否给够
2. 全局账户如果被限制, 某些功能可能会显示无权限, 去给微软提工单
3. 修改用户密码需要给特殊权限, 详见此处
[StackOverflow](https://stackoverflow.com/questions/61004464/how-to-update-the-password-of-user-in-azure-ad-using-graph-api)

### 为什么获取数据这么慢

首先说明, 这不是python慢的问题, ~~也不是我代码质量的问题(别笑)~~  
这么小型的项目还到不了python的瓶颈, 这样的延迟用户几乎感受不出来  
主要由两个方面造成的明显延迟:  
1. 微软API响应, 占了延迟时间的80%
2. telegram服务器的延迟

### 为什么机器人这么丑

主要由以下两方面原因:
1. 受限于telegram的消息格式限制, 消息支持的样式无论是html还是markdown
都十分有限, 机器人可以发送键盘, 最多加几个emoji, 仅此而已. 
~~下拉列表都没有你还想要什么特效? 做梦!~~ 等telegram官方支持更多格式.
2. 小弟不才, 不会设计, 有什么想法可以提issue

### 其它问题

- 启动失败: 查看机器终端, 会直接输出错误信息
- 运行时错误: 使用`/log`获取机器人运行日志
- Bug: 提issue反馈问题, 或者设置环境变量`DEBUG=True`, 记得生产环境改回`False`
- 其它: 提issue反馈问题
