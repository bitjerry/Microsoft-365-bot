about = "<b>欢迎使用 Microsoft 365 全局账户管理机器人!</b>\n" \
        "<a href='https://github.com/bitjerry/Microsoft-365-bot'>Version 2.0</a>"
cancel = "当前操作已被取消."
expire = "会话已过期!!!"
error = "未知错误!!!"
null = "没有数据"
empty = "消息为空"
init_f = "未初始化机器人!!!"
not_modified = "消息不需要更新"
params_error = "没有匹配的参数类型或数据"
page_up_btn = "⏫ 上一页"
page_down_btn = "下一页 ⏬"
"""
bot area
"""

key = "<i>令牌仅显示一次, 并且将在300秒后被销毁.\n<pre>{}</pre>\n" \
      "请及时保存它.</i>"
key_hidden = "<pre>{}</pre>"
key_ops = [(0, "解锁"), (1, "生成")]
key_op = key_ops[1:]
key_decrypt = "<b>检测到数据库已有数据, 请输入令牌解锁它们, \n" \
              "或者生成一个新令牌 (那将清空已有数据) !!!</b>"
key_empty = "未找到令牌!!!"
key_gen = "生成一个新令牌以保护你的app数据"
key_input = "输入解密令牌以解密你的app数据"
key_decrypt_f = "解密失败"
key_encrypt_f = "加密失败"
key_unlock_s = "解锁成功"
key_unlock_f = "解锁失败"
"""
key area
"""

secret_hidden = "<pre>***</pre>"
secret_cmp = "请输入密码以继续"
secret_cmp_error = "密码不正确, 请重新输入新密码以继续"
"""
secret area
"""

app_control = [(0, "删除"),
               (1, "编辑身份识别信息"),
               (2, "重命名"),
               (3, "返回app列表")]
app_select = "从以下列表中指定一个app:"
app_empty = "没有app"
app_no = "没有app被指定"
app_id_no = "App id 不存在"
app_add_more = "下载此模板, 在填写完app信息后, 传回此模板以批量添加app"
app_add = "发给我app数据. 请遵循以下格式:\n\napp_name\nclient_id\nclient_secret\ntenant_id\n"
app_add_s = "添加全局管理app成功!"
app_add_f = "添加全局管理app失败!"
app_del_s = "删除成功"
app_del_f = "删除失败"
app_clear_s = "所有app都已被移除!"
app_rename = "发给我一个新名字"
app_rename_s = "重命名成功"
app_edit = "发给我app的身份验证信息. 请遵循以下格式:\n\nclient_id\nclient_secret\ntenant_id\n"
app_edit_s = "编辑成功"
app_edit_f = "编辑失败"
app_data = "<b>当前指定的app是:</b>\n\n"
app_info_f = "信息格式错误"
"""
app area
"""

sub_control = [(0, "返回订阅列表")]
sub_select = "从以下列表中选择一个订阅:"
sub_no = "没有订阅"
"""
subscription area
"""

role_back_btn = "返回角色"
role_control = [(0, "获取用户"), (1, "返回角色列表")]
role_select = "从以下列表中选择一个角色:"
role_no = "没有角色"
role_no_user = "没有用户属于此角色"
"""
role area
"""

user_control_back = [(0, "分配许可"),
                     (1, "我的许可"),
                     (2, "分配角色"),
                     (3, "我的角色"),
                     (4, "重命名"),
                     (5, "修改显示名"),
                     (6, "重置密码"),
                     (7, "修改用户名后缀"),
                     (8, "删除"),
                     (9, "禁用"),
                     (10, "启用"),
                     (11, "刷新"),
                     (12, "返回用户列表")]
user_control_back_only = user_control_back[-1:]
user_control = user_control_back[:-1]
user_back_btn = "返回用户"
user_select = "从以下列表中选择一个用户:"
user_by_name = "选择一个用户通过指定用户名: xxx@contoso.com"
user_search = "搜索用户通过用户名 (模糊匹配)"
user_no = "没有用户"
user_name = "当前用户名是: <b>{}</b>\n"
user_data = "发给我用户信息. 请遵循以下格式:\n\nusername\npassword (可选)"
user_create_s = "<b>成功创建用户\n此信息仅显示一次!!!\n" \
                "为了密码安全起见, 请在用后删除此信息</b>" \
                "\n===========\n\nUsername: {}\nPassword: {}"
user_delete_s = "用户被成功删除"
user_update = user_data
user_update_s = "用户信息被成功更新"
user_name_suffix_back = "返回用户名后缀列表"
user_name_suffix_select = "<b>从下列域名中选择一个作为用户名后缀</b>"
user_name_suffix_update_s = "用户名后缀更新成功"
user_rename = "发给我一个新名字"
user_rename_s = "重命名成功"
user_reset_password = "你的新密码是: <pre>{}</pre>\n" \
                      "请及时保存它, 出于安全考虑最好在用后删除它"
user_lic_no = "用户没有许可证"
user_lic_asg_btn = "分配许可"
user_lic_asg = "你已经选择了:\n\n<i>{}</i>\n按下 <b>分配许可</b> 以为用户分配它们"
user_lic_asg_sel = "选择你想要为用户分配的许可证, 单击选择, 双击取消选择"
user_lic_asg_s = "许可证分配成功"
user_lic_del_s = "许可证删除成功"
user_lic_del_btn = "删除许可"
user_lic_del = "你已经选择了:\n\n<i>{}</i>\n按下 <b>删除许可</b> 以为用户删除它们"
user_lic_del_sel = "选择你想要为用户删除的许可证, 单击选择, 双击取消选择"
user_role_asg = "选择一个角色为用户分配, 请勿重复分配"
user_role_del = "选择一个角色为用户删除, 请勿重复删除"
user_role_del_s = "角色删除成功"
user_role_asg_s = "角色分配成功"
user_role_no = "用户没有角色"
user_disable = "用户已被禁用"
user_enable = "用户已被启用"
user_modify_display_name = user_rename
user_modify_display_name_s = "成功修改用户的显示名"
"""
user area
"""

org_no = "没有组织信息"
"""
org area
"""

domain_control_verify_back = [(0, "验证"), (1, "删除"), (2, "返回")]
domain_control_verify = domain_control_verify_back[:-1]
domain_control_back = domain_control_verify_back[1:]
domain_control = domain_control_verify_back[1:2]
domain_control_back_only = domain_control_verify_back[-1:]
domain_select = "从以下列表中选择一个域名:"
domain_add = "发给我一个域名"
domain_add_f = "域名添加失败"
domain_del_s = "域名删除成功"
domain_dns = "请在你的域名托管商中添加一个DNS记录以验证域名:\n"
domain_verify_f = "域名验证失败!!!\n你确定DNS记录已被正确添加吗?"
domain_no = "没有域名"
"""
domain area
"""

match_error = "No case matched"
module_name_error = "Module is not in service directory!!!"
"""
other
"""
