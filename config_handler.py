import os
import sys
import yaml

if sys.platform == "win32":
    import msvcrt

if getattr(sys, 'frozen', False):
    # Running as .exe — use the exe's directory
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    # Running as .py script — use the script's directory
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.yaml")

#Function to look for a yaml config in the same directory
def load_config():
    #===========================================
    #Generates a template if none was found so the user can edit it themselves
    if not os.path.exists(CONFIG_PATH):
        print("No config file found.")
        generate_template()
        print(f"Template create at: {CONFIG_PATH}")
        print("Please edit template file with a text editor and run the script again.")
        print("Press any key to exit...")
        if sys.platform == "win32": msvcrt.getch()
        else: input()
        sys.exit(0)
    #===========================================

    #If config file is found load it into variable config
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)


    #Exception handling so that the discord bot wont start if theres no TOKEN
    if not config["credentials"].get("TOKENsecret") or config["credentials"]["TOKENsecret"] == "your_TOKEN_secret_here":
        print("No TOKEN secret detected please enter your token.")
        sys.exit(0)

    #Returns yaml file as a variable if you call this function
    return config


TEMPLATE_COMMENT = """# ===== Auto-Login Configuration =====
# Add your TOKENsecret in this file
# =====================================

"""

DEFAULT_CONFIG = {

    "credentials": {
        "TOKENsecret": "your_TOKEN_secret_here"
    }
}


#===================================
def generate_template():
    #Python's way to create a YAML file
    with open(CONFIG_PATH, "w") as yaml_file:
        yaml_file.write(TEMPLATE_COMMENT)
        yaml.dump({"credentials": DEFAULT_CONFIG["credentials"]}, yaml_file, default_flow_style=False, sort_keys=False)
    pass

if __name__ == "__main__":
    load_config()