import os
import openai
import asyncio
import argparse
import util
import copy
import json
import sandbox
import sapphire_features

AUTOSAVE = "autosave.log"

class Assistant:
  # Maintains a running log of ALL prompts (global/singleton)

  # replace w/ org key
  openai.organization = os.getenv('AI_ORG')
  # replace w/ openai key
  openai.api_key = os.getenv('AI_KEY')

  # These will be lists of dictionaries
  running_log = []
  tailored_prompt_history = []
  buffer_log = []
  append_data = ""

  def __init__(self):
    print(util.COLOR_RED+"Assistant initalized"+util.COLOR_RESET)
    # TODO: Change this toreference a final STRING reference?
    self.reset()

  def log(self,prompt,result):
    sapphire_features.print_color(result,util.COLOR_RED)
    formatted_prompt = copy.deepcopy(util.user_role)
    formatted_result = copy.deepcopy(util.assistant_role)
    formatted_prompt["content"]=prompt
    formatted_result["content"]=result
    self.running_log.append(formatted_prompt)
    self.running_log.append(formatted_result)
    
  def retain(assistant):
    assistant.tailored_prompt_history.append(assistant.running_log[-2])
    assistant.tailored_prompt_history.append(assistant.running_log[-1])
    
  def reset(self,messages=None):
    if(messages == None):
      self.running_log = util.chatbot_layer()
      self.tailored_prompt_history = util.chatbot_layer()
    else:
      self.running_log = messages
      self.tailored_prompt_history = copy.deepcopy(messages)

  def process_incoming_message(self, prompt):
    # This returns false if a command was found
    if(sapphire_features.prefix_processor(self, prompt)):
      new_user_role = copy.deepcopy(util.user_role)
  
      prompt = prompt+"\n"+self.append_data
      # if append_data was empty, it'll get stripped out, which removes the unnescissary 
      prompt.strip()
      #reset appended_data
      self.append_data = ""

      new_user_role["content"] = prompt

      temp = copy.deepcopy(self.tailored_prompt_history)
      temp.append(new_user_role)
      
      response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=temp
      )

      return response['choices'][0]['message']['content']
    else:
      return False    



#--------------------------END CLASS DEFINITION-------------------------------

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Entry for Sapphire assistant")
  parser.add_argument('-d', dest='daemon', help="start the websocket daemon", action="store_true")
  #This should be for passing in a one off question, or starting a session w/ an eternal question
  parser.add_argument('-p', dest='prompt', help="pass an intial prompt to Sapphire when starting",type=str)
  #This should be for passing in a config file
  #parser.add_argument('-d', dest='daemon', help="start the websocket daemon", action="store_true")
  args = parser.parse_args()

  assistant = Assistant()
  sapphire_features.autoload(assistant,AUTOSAVE)

  if(args.daemon == True):
    asyncio.run(util.server())
  else:
    # Run forever
    while True:
      print(util.COLOR_GREEN+"What would you like to say to Sapphire.EXE? "+util.COLOR_RESET,end="")
      prompt = input()
      print("--------------------------------")
      result = assistant.process_incoming_message(prompt.strip())
      if(result != False):
        assistant.log(prompt,result)
        assistant.retain()
        #assistant.post()
        # record the log for reference
      # TODO: move save/load to assstant
#      sapphire_features.save(assistant,AUTOSAVE)
      print("--------------------------------")
