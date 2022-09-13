about = "<b>Welcome to Microsoft 365 Global Management Bot!</b>\n<a " \
        "href='https://github.com/bitjerry/Microsoft-365-bot'>About</a>"
cancel = "The current operation has been cancelled."
expire = "Session has expired!!!"
error = "Unknown error!!!"
null = "None data"
empty = "Message text is empty"
init_f = "Error initializing bot!!!"
params_error = "Parameter type or number mismatch"
"""
bot area
"""

db_data_found = "We find existing apps, decrypt them with a key, or discard them and generate a new key"
db_decrypt_f = "decryption failure"
db_encrypt_f = "encryption failure"
db_unlock_s = "Unlock succeeded"
db_unlock_f = "Unlock failed"
"""
database area
"""

key_op = ["Unlock", "New"]
key_empty = "No token is found!"
key_gen = "Generate a new token to protect my apps"
key_input = "Enter the decryption token of the current apps"
key_cmp = "Enter the token to continue"
key_cmp_error = "Incorrect token"
"""
key area
"""

app_choose = "Choose an app from the list below:"
app_no = "Oops!!! No app"
app_add = "Send me app data. Please use this format:\n\napp_name\nclient_id\nclient_secret\ntenant_id\n"
app_add_s = "Successfully added global management app!"
app_add_f = "Failed to add global management app"
app_del_s = "Delete success"
app_del_f = "Delete fail"
app_clear_s = "All apps have been removed!"
app_rename = "Send me a new name"
app_rename_s = "Rename success"
app_edit = "Send me app auth info. Please use this format:\n\nclient_id\nclient_secret\ntenant_id\n"
app_edit_s = "Edit success"
app_edit_f = "Edit fail"
app_info_f = "Info format error"
"""
app area
"""

sub_choose = "Choose a subscription from the list below:"
sub_no = "Oops!!! No subscription"
"""
subscription area
"""

role_choose = "Choose a role from the list below:"
role_no = "Oops!!! No role"
role_no_user = "There are no members for this role"
"""
role area
"""

user_choose = "Choose a user from the list below:"
user_by_name = "Choose a user by username: xxx@contoso.com"
user_search = "Search for users by username (fuzzy matching)"
user_no = "Oops!!! No user"
user_data = "Send me user info. Please use this format:\n\nusername\ndisplay name\npassword\n"
user_create_s = "<b>Successfully create user\nThis information is displayed only once!!!\n===========\n</b>"
user_assign_lic_s = "License assigned successfully"
user_delete_lic_s = "License deleted successfully"
user_delete_s = "User deleted successfully"
user_update = user_data
user_update_s = "User information updated successfully"
user_lic_no = "Oops!!! No license for user"
user_lic_assign = "Select the licenses you want to assign, click Select, and click Unselect again"
user_lic_del = "Select the license you want to delete, click Select, and click Unselect again"
user_role_assign = "Select one role to assign, only one at a time. Do not assign again"
user_role_del = "Select one role to delete, only one at a time. Do not assign again"
user_role_del_s = "Role deleted successfully"
user_role_assign_s = "Role assigned successfully"
user_role_no = "Oops!!! No Role for user"
"""
user area
"""

org_no = "Oops!!! No Org for app"
"""
org area
"""