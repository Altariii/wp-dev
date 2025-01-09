from ....config import config
from ....utils import console

def remove_git_account() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Git Account Remover")
    print("")

    git_accounts = config.git_accounts()
    if not git_accounts:
        console.display.error("No Git accounts have been saved in WP-DEV's config")
        return
    
    console.display.info("Saved Git Accounts:")
    for index, account in enumerate(git_accounts):
        print('[' + str(index) + '] ' + account['name'] + '@' + account['domain'])
    print("")

    account_to_delete = int(console.display.request("Select the number of the Git account to delete"))
    if account_to_delete < 0 or len(git_accounts) <= account_to_delete:
        console.display.error("Invalid Account Number. Please, select a number from 0 and " + str(len(git_accounts)))
        return

    confirm = console.display.request("Are you sure you want to remove this Git Account? " + git_accounts[account_to_delete]["name"] + '@' + git_accounts[account_to_delete]["domain"] + ' (y/n)' )
    if confirm.lower() == 'n':
        console.display.info("Git account removal aborted")
        return
    
    del git_accounts[account_to_delete]
    new_config = config.get_config()
    new_config["git_accounts"] = git_accounts
    config.save_new_config(new_config)

    console.display.success("Git account removed successfully")
    return

class RemoveGitAccountCommand:
    parent_page = "Manage Git Accounts"
    submenu_page = False
    key = '3'
    description = 'Remove a Git Account from WP-DEV'
    handler = remove_git_account