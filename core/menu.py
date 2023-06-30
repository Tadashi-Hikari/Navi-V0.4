import sapphire_features

# This allows me to quick switch between modes
def switch():
    modes = "list all available .log files, give an index next to it"

def inverse_edit(assistant):
    sapphire_features.show(assistant.tailored_prompt_history)

def inverse_edit_full_log(assistant):
    sapphire_features.show(assistant.running_log)

def attach(assistant):
    print("Enter filepath: ", end="")
    path = input()

    file = open(path,"r")
    file_data = file.read()
    assistant.append_data = file_data

def freeze_current(assistsant):
    assistant.running_log.append({"content" : "context switched to X"})
    assistant.buffer_log = copy.deepcopy(assistant.tailored_prompt_history)
    
