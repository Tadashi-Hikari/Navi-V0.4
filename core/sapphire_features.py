import util
import os
import json
import subprocess

logs_dir = "./logs/"

# this does the inital command preprocessing/check. I imagine I can have up to three word commands before I start bumping into serious natural language issues
def prefix_processor(assistant, prompt):
    prompt = prompt.strip()
    if prompt=="help" or prompt=="h":
        util.print_help()
        return False
    elif prompt=="exit":
        exit()
    elif prompt=="r" or prompt=="reprint":
        print_last_prompt(assistant)
    #todo: Make this print over the websocket
    elif prompt=="clear" or prompt=="c":
        clear()
        return False
    elif prompt=="ignore" or prompt=="i":
        ignore(assistant)
    elif prompt=="save" or prompt=="s":
        save(assistant)
    elif prompt=="echo":
        print_to_file(assistant)
    elif prompt=="quicksave" or prompt=="q":
        save(assistant,util.default_log_name)
    elif prompt=="load" or prompt == "l":
        load(assistant)
    elif prompt=="init":
        assistant.reset()
        # TODO: Replace w/ function call
        prefix_processor(assistant,"clear")
        print(util.COLOR_RED+"Reinitialized"+util.COLOR_RESET)
    elif prompt=="show":
        show(assistant.tailored_prompt_history)
    elif prompt=="show unedited history":
        show(assistant.running_log)
    elif prompt=="edit":
        new_tailored_prompt=transcript_selection(assistant)
        assistant.reset(new_tailored_prompt)
    elif prompt=="inverse edit":
        menu.inverse_edit(assistant)
    elif prompt=="full edit":
        menu.inverse_edit_full_log(assistant)
    elif prompt=="attach":
        menu.attach(assistant)
    elif prompt=="bash":
        subprocess.call(['bash'])
    else:
        return True
    
def clear():
    system = os.name
    if(system == "nt"):
        os.system("cls")
    elif(system == "posix"):
        os.system("clear")
    else:
        os.system("clear")
        
def print_last_prompt(assistant):
    print(util.COLOR_RED+assistant.tailored_prompt_history[-1]["content"]+util.COLOR_RESET)

def ignore(assistant):
    size = len(assistant.tailored_prompt_history)
    if(size > 2):
        assistant.tailored_prompt_history.pop()
        assistant.tailored_prompt_history.pop()
        # Print the last message so I remember what I was doing
        print_last_prompt(assistant)
        
    print(util.COLOR_RED+"Prompt scrubbed"+util.COLOR_RESET)
    
# TODO: Make a custom 'save' program, that allows me to mark what type it is
def save(assistant, filename=None): 
  if(filename == None):
    print("enter filename: ",end="")
    filename = input()
  else:
    filename="autosave.log"

  with open(logs_dir+filename,"w") as json_file:
    # Print it in a nice human readable format, so we can edit it if needed
    json.dump(assistant.tailored_prompt_history,json_file,indent=4)

  print(util.COLOR_RED+"log saved"+util.COLOR_RESET)

def autoload(assistant, filename):
  with open(filename, "r") as infile:
    # TODO: Centralize this through the assistant.init()/reset()
    assistant.reset(json.load(infile))
    
def load(assistant, filename=None):
    print("Did you want to save the current session? ",end="")
    prompt = input()
    if prompt=="yes" or prompt == "y":
        save(assistant,filename)
    if filename == None:
        print("enter filename to load: ",end="")
        filename = input()
    autoload(assistant, filename)
    print("file loaded")
  
def show(messages):
  for line, item in enumerate(messages):
    print(util.COLOR_RED+f"Line {line}: {item}\n"+util.COLOR_RESET)

def print_color(message, color,end=None):
    print(color+message+util.COLOR_RESET,end=end)

def print_to_file(assistant):
    # Currently, I want it to print to a file. just ask filename?
    print("Enter filename: ",end="")
    filename = input()
    file = open(filename,"w")
    file.write(assistant.tailored_prompt_history[-1]["content"])   

# Print the messages w/ line numbers
def transcript_selection(assistant):
    show(assistant.tailored_prompt_history)
    print("Enter lines to keep. Separate lines with comma: ",end="") 
    lines = input()

    new_tailored_prompt = []
    
    lines = lines.split(",")
    for line in lines:
        new_tailored_prompt.append(assistant.tailored_prompt_history[int(line)])
    
    return new_tailored_prompt

# This allows me to quick switch between modes
def switch():
    modes = "list all available .log files, give an index next to it"

def inverse_edit(assistant):
    show(assistant.tailored_prompt_history)

def inverse_edit_full_log(assistant):
    show(assistant.running_log)

def attach(assistant):
    print("Enter filepath: ", end="")
    path = input()

    file = open(path,"r")
    file_data = file.read()
    assistant.append_data = file_data

def freeze_current(assistsant):
    assistant.running_log.append({"content" : "context switched to X"})
    assistant.buffer_log = copy.deepcopy(assistant.tailored_prompt_history)