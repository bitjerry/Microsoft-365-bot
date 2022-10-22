about = "<b>Welcome to Microsoft 365 Global Management Bot!</b>\n" \
        "<a href='https://github.com/bitjerry/Microsoft-365-bot'>Version 2.3</a>"
cancel = "The current operation has been cancelled."
expire = "Session has expired!!!"
error = "Unknown error!!!"
null = "None data"
empty = "Message text is empty"
init_f = "Error initializing bot!!!"
not_modified = "message is not modified"
params_error = "Parameter type or number mismatch"
page_up_btn = "⏫ page up"
page_down_btn = "page down ⏬"
"""
bot area
"""

key = "<i>The key is only shown once and will be hidden in <b>{}</b> seconds.\n<pre>{}</pre>\n" \
      "Please save that in time.</i>"
key_hidden = "<pre>{}</pre>"
key_op = {"new": "New"}
key_ops = {"unlock": "Unlock"} | key_op
key_decrypt = "<b>Existing apps are detected, enter a key to unlock them, \n" \
              "or generate a new key (which will empty them) !!!</b>"
key_empty = "No key is found!!!"
key_gen = "Generate a new key to protect my apps"
key_input = "Enter the decryption key of the current apps"
key_decrypt_f = "decryption failure"
key_encrypt_f = "encryption failure"
key_unlock_s = "Unlock succeeded"
key_unlock_f = "Unlock failed"
"""
key area
"""

secret_hidden = "<pre>***</pre>"
secret_cmp = "Enter the secret to continue"
secret_cmp_error = "Incorrect secret. You still have <b>{}</b> retries, please enter the correct secret to continue"
secret_lock = "The current operation is locked"
"""
secret area
"""

app_control = {"delete": "Delete",
               "edit": "Edit auth info",
               "rename": "Rename",
               "back_to_apps_list": "Back to apps list"}
app_select = "Select an app from the list below:"
app_empty = "Oops!!! No app"
app_no = "Oops!!! No app is specified"
app_id_no = "App id that does not exist"
app_add_more = "Download this template, and after filling out all apps information, return it to add apps in bulk."
app_add = "Send me app data. Please use this format:\n\napp_name\nclient_id\nclient_secret\ntenant_id\n"
app_add_s = "Successfully added global management app!"
app_add_f = "Failed to add global management app!"
app_del_s = "Delete success"
app_del_f = "Delete fail"
app_clear_s = "All apps have been removed!"
app_rename = "Send me a new name"
app_rename_s = "Rename success"
app_edit = "Send me app auth info. Please use this format:\n\nclient_id\nclient_secret\ntenant_id\n"
app_edit_s = "Edit success"
app_edit_f = "Edit fail"
app_data = "<b>You've already specified the App:</b>\n\n"
app_info_f = "Info format error"
"""
app area
"""

sub_control = {"back_to_subs_list": "Back to subs list"}
sub_select = "Select a subscription from the list below:"
sub_no = "Oops!!! No subscription"
"""
subscription area
"""

role_back_btn = "Beck to role"
role_control = {"get_member": "Get member",
                "back_to_roles_list": "Back to roles list"}
role_select = "Select a role from the list below:"
role_no = "Oops!!! No role"
role_no_user = "There are no members for this role"
"""
role area
"""

user_control = {'asg_lic': 'Assign license',
                'my_lic': 'My license',
                'asg_role': 'Assign role',
                'my_role': 'My role',
                'rename': 'Rename',
                'modify_display_name': 'Modify display name',
                'reset_pwd': 'Reset password',
                'chang_name_suffix': 'Chang name suffix',
                'delete': 'Delete',
                'disable': 'Disable',
                'enable': 'Enable',
                'refresh': 'Refresh'}
user_control_back_only = {'back_to_user_list': 'Back to user list'}
user_control_back = user_control | user_control_back_only
user_back_btn = "Back to user"
user_select = "Select a user from the list below:"
user_by_name = "Select a user by username: xxx@contoso.com.\nPlease enter the username."
user_search = "Search for users by username (fuzzy matching).\nPlease enter the keyword."
user_search_f = "No user was found. Please re-enter the keyword"
user_no = "Oops!!! No user"
user_name = "The current username is: <b>{}</b>\n"
user_data = "The current username suffix is <b>{}</b>. \nPlease send me more information. "\
            "In this format:\n\nusername\npassword (Optional) "
user_create_s = "<b>Successfully create user\nThis information is displayed only once!!!\n" \
                "For password security, it is better to delete it after use</b>" \
                "\n===========\n\nUsername: <b>{}</b>\nPassword: <b>{}</b>"
user_delete_s = "User deleted successfully"
user_update = user_data
user_update_s = "User information updated successfully"
user_name_suffix_back = "Back to username suffix list"
user_name_suffix_select = "<b>Select one of the following domain names as the username suffix</b>"
user_name_suffix_update_s = "Username suffix updated successfully"
user_rename = "Send me a new name"
user_rename_s = "Rename user successfully"
user_reset_password = "Your new password is: <pre>{}</pre>\n" \
                      "Please save it in time, and then delete it for security"
user_lic_no = "Oops!!! No license for user"
user_lic_asg_btn = "Assign License"
user_lic_asg = "You've already selected:\n\n<i>{}</i>\nPress <b>Assign License</b> to assign them to the user"
user_lic_asg_sel = "Select the licenses you want to assign, click Select, and click Unselect again"
user_lic_asg_s = "License assigned successfully"
user_lic_del_s = "License deleted successfully"
user_lic_del_btn = "Delete License"
user_lic_del = "You've already selected:\n\n<i>{}</i>\nPress <b>Delete License</b> to delete them from the user"
user_lic_del_sel = "Select the license you want to delete, click Select, and click Unselect again"
user_role_asg = "Select one role to assign, only one at a time. Do not assign again"
user_role_del = "Select one role to delete, only one at a time. Do not delete again"
user_role_del_s = "Role deleted successfully"
user_role_asg_s = "Role assigned successfully"
user_role_no = "Oops!!! No role for user"
user_disable = "User has been disabled"
user_enable = "User has been enabled"
user_modify_display_name = user_rename
user_modify_display_name_s = "Successfully modified the display name"
"""
user area
"""

org_no = "Oops!!! No organization"
"""
org area
"""

domain_control = {'delete': 'Delete'}
domain_control_back_only = {'back': 'Back'}
domain_control_verify = {'verify': 'Verify'} | domain_control
domain_control_back = domain_control | domain_control_back_only
domain_control_verify_back = domain_control_verify | domain_control_back_only
domain_select = "Select a domain from the list below:"
domain_add = "Send me a domain name"
domain_add_f = "Domain added failure"
domain_del_s = "Domain deleted successfully"
domain_dns = "Add the DNS records to your domain name Manager to verify the domain name:\n"
domain_verify_f = "Domain verify failure!!!\nAre you sure the correct DNS record has been added?"
domain_no = "Oops!!! No domain"
"""
domain area
"""

match_error = "No case matched"
module_name_error = "Module is not in service directory!!!"
"""
other
"""
