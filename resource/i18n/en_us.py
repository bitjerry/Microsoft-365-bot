about = "<b>Welcome to Microsoft 365 Global Management Bot!</b>\n<a " \
        "href='https://github.com/bitjerry/Microsoft-365-bot'>About</a>"
cancel = "The current operation has been cancelled."
expire = "Session has expired!!!"
error = "Unknown error!!!"
null = "None data"
empty = "Message text is empty"
init_f = "Error initializing bot!!!"
params_error = "Parameter type or number mismatch"
page_up_btn = "⏫ page up"
page_down_btn = "page down ⏬"
"""
bot area
"""

key = "<i>The token is only shown once and will be hidden in 10 seconds.\n<pre>{}</pre>\n" \
      "Please save that in time.</i>"
key_hidden = "<pre>{}</pre>"
key_ops = [(0, "Unlock"), (1, "New")]
key_op = key_ops[1:]
key_decrypt = "<b>Detect existing databases, enter a token to unlock them, \n" \
              "or generate a new token (which will empty them) !!!</b>"
key_empty = "No token is found!!!"
key_gen = "Generate a new token to protect my apps"
key_input = "Enter the decryption token of the current apps"
key_decrypt_f = "decryption failure"
key_encrypt_f = "encryption failure"
key_unlock_s = "Unlock succeeded"
key_unlock_f = "Unlock failed"
"""
key area
"""

secret_hidden = "<pre>***</pre>"
secret_cmp = "Enter the secret to continue"
secret_cmp_error = "Incorrect secret. Please enter the new secret to continue"
"""
secret area
"""

app_control = [(0, "Delete"),
               (1, "Edit auth info"),
               (2, "Rename"),
               (3, "Back to apps list")]
app_select = "Select an app from the list below:"
app_empty = "Oops!!! No app"
app_no = "Oops!!! No app is specified"
app_id_no = "App id that does not exist"
app_add_more = "Send me the <i>template.json</i> to add more apps"
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

sub_control = [(0, "Back to subs list")]
sub_select = "Select a subscription from the list below:"
sub_no = "Oops!!! No subscription"
"""
subscription area
"""

role_back_btn = "Beck to role"
role_control = [(0, "Get member"), (1, "Back to roles list")]
role_select = "Select a role from the list below:"
role_no = "Oops!!! No role"
role_no_user = "There are no members for this role"
"""
role area
"""

user_control_back = [(0, "Assign license"),
                     (1, "My license"),
                     (2, "Assign role"),
                     (3, "My role"),
                     (4, "Delete"),
                     (5, "Rename"),
                     (6, "Reset password"),
                     (7, "Chang name suffix"),
                     (8, "Refresh"),
                     (9, "Back to user list")]
user_control_back_only = user_control_back[-1:]
user_control = user_control_back[:-1]
user_select = "Select a user from the list below:"
user_by_name = "Select a user by username: xxx@contoso.com"
user_search = "Search for users by username (fuzzy matching)"
user_no = "Oops!!! No user"
user_name = "The current username is: <b>{}</b>\n"
user_data = "Send me user info. Please use this format:\n\nusername\npassword (Optional)"
user_create_s = "<b>Successfully create user\nThis information is displayed only once!!!\n"\
                "For password security, it is better to delete it after use</b>" \
                "\n===========\n\nUsername: {}\nPassword: {}"
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
user_role_del = "Select one role to delete, only one at a time. Do not assign again"
user_role_del_s = "Role deleted successfully"
user_role_asg_s = "Role assigned successfully"
user_role_no = "Oops!!! No role for user"
user_back_btn = "Back to user"
"""
user area
"""

org_no = "Oops!!! No organization"
"""
org area
"""

domain_control_verify_back = [(0, "Verify"), (1, "Delete"), (2, "Back")]
domain_control_verify = domain_control_verify_back[:-1]
domain_control_back = domain_control_verify_back[1:]
domain_control = domain_control_verify_back[1:2]
domain_control_back_only = domain_control_verify_back[-1:]
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
