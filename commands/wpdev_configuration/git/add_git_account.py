from ....config import config
from ....utils import console

def check_git_account_existence(name: str, domain: str) -> bool:
    git_accounts = config.git_accounts()
    if not git_accounts:
        return False
    
    for account in git_accounts:
        if account['name'] == name and account['domain'] == domain:
            return True
        
    return False

def add_git_account() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Git Account Adder")
    print("")

    git_accounts = config.git_accounts()
    if not git_accounts:
        git_accounts = []
        console.display.info("No Git accounts have been saved in WP-DEV's config")
    else:
        console.display.info("Saved Git accounts:")
        for account in git_accounts:
            console.display.statement(account['name'] + '@' + account['domain'])
    print("")

    confirm = console.display.request("Do you want to add a new Git account? (y/n)")
    if confirm.lower() == 'n':
        console.display.info("Git account addition aborted")
        return
    
    account_domain = console.display.request("Git Account Domain")
    account_name = console.display.request("Git Account Name")
    account_pass = console.display.request("Git Account Token")
    
    if check_git_account_existence(account_name, account_domain):
        console.display.warning("The account introduced is already saved. Aborting.")
        return
    
    git_accounts.append({
        "domain": account_domain,
        "name": account_name,
        "password": account_pass
    })
    new_config = config.get_config()
    new_config["git_accounts"] = git_accounts
    config.save_new_config(new_config)

    console.display.success("Git account added successfully")
    return

class AddGitAccountCommand:
    parent_page = "Manage Git Accounts"
    submenu_page = False
    key = '1'
    description = 'Add a Git Account to WP-DEV'
    handler = add_git_account