from ....config import config
from ....utils import console

def update_git_credentials() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Git Account Updater")
    print("")

    git_accounts = config.git_accounts()
    if not git_accounts:
        console.display.error("No Git accounts have been saved in WP-DEV's config")
        return
    
    console.display.info("Saved Git Accounts:")
    for index, account in enumerate(git_accounts):
        print('[' + str(index) + '] ' + account['name'] + '@' + account['domain'])
    print("")

    account_to_delete = int(console.display.request("Select the number of the Git account to update"))
    if account_to_delete < 0 or len(git_accounts) <= account_to_delete:
        console.display.error("Invalid Account Number. Please, select a number from 0 and " + str(len(git_accounts)))
        return
    
    new_credentials = console.display.request("Input the new Git credentials")
    git_accounts[account_to_delete]["password"] = new_credentials
    new_config = config.get_config()
    new_config["git_accounts"] = git_accounts
    config.save_new_config(new_config)

    console.display.success("Git account updated successfully")
    return

class UpdateGitCredentialsCommand:
    parent_page = "Manage Git Accounts"
    submenu_page = False
    key = '2'
    description = 'Update a Git Account from WP-DEV'
    handler = update_git_credentials