import entry
import sapphire_features
import util

# Print the messages w/ line numbers
def transcript_selection(assistant):
    sapphire_features.show(assistant.tailored_prompt_history)
    print("Enter lines to keep. Separate lines with comma: ",end="") 
    lines = input()

    new_tailored_prompt = []
    
    lines = lines.split(",")
    for line in lines:
        new_tailored_prompt.append(assistant.tailored_prompt_history[int(line)])
    
    return new_tailored_prompt
