import asyncio
import datetime

'''

 I can have noise filter/stt feature layers
- machinery noise filter
- other people filter
- tinny sound filter
- pitch detection layer
- continuity layer
'''

# Define ANSI escape codes for colors
COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_YELLOW = '\033[33m'
COLOR_BLUE = '\033[34m'
COLOR_MAGENTA = '\033[35m'
COLOR_CYAN = '\033[36m'
COLOR_WHITE = '\033[37m'
COLOR_RESET = '\033[0m'

user_role = {"role" : "user", "content" : "this is sample input. disregard"}
system_role = {"role" : "system", "content" : "this is sample output. disregard"}
assistant_role = {"role" : "assistant", "content" : "this is sample output. disregard"}

default_log_name = "quicksave.log"

async def server():
  async with websockets.serve(on_receive, "localhost",6009,ping_timeout=None):
    await asyncio.Future()

async def on_receive(websocket):
  async for message in websocket:
    print("Incoming message: "+message)
    await websocket.send(process_incoming_message(message))

def chatbot_layer():
# This is used to prime the chatbot, or keep track of prior conversation
  tailored_prompt_history = [
    {"role": "system",
     "content": "You are a helpful assistant, your name is Sapphire.exe. Your purpose is to help your developer Chris manage his ADHD, schedule, and his projects"}
  ]

  return tailored_prompt_history

def alarm_calendar_decider(prompt):
    user_role["content"] = prompt 

    current_datetime = datetime.date.today()
    time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # This is used to prime the chatbot, or keep track of prior conversation
    messages = [
        {"role": "system",
         "content": "You decide if input falls in to the categories of alarm, calendar, or neither. If something seems like it should be related to a timer it shpuld fall under the category alarm. Alarms are to be set within the next two day. Calendar events are things that happen farther in the future. A calendar event OR an alarm could happen on the next day, but extra care should be used to discriminate between alarms and calendar events when there is a potential time overlap. Extract the key variables such as the event title, and time. if the decided type is an alarm type, Don't add anything other than \"key: value\" responses. if it is a calendar type, disreguard the \"key: value\" and produce a full ical entry. Todays date is "+time+", use that to calculate the date in the future"},
        {"role": "user", "content": "Wake me up at eight tomorrow"},
        {"role": "assistant", "content": "type: alarm time: 0800"},
        {"role": "user", "content": "I have aerials every monday at six"},
        {"role": "assistant", "content": "type: calendar time: 1800 reoccurance: weekly"},
        user_role
    ]

    return messages

def variable_extraction_layer():
  messages = [
    {"role": "system",
     "content": "You are a variable extractor for an ai pipeline. your job is to extract relavent variables in a way that can be directly passed to another machine learning system. examples will be passed below. You will attempt to infer contextual information from the data. all information will be passed in form \"key: value\", separated by commas, and in lower case"},
    {"role": "user", "content": "I have to wake up tomorrow at eight?"},
    {"role": "assistant", "content": "event: Wake up, time: 0800"},
    {"role": "user", "content": "I am having lunch tomorrow with Bailey"},
    {"role": "assistant", "content": "event: Lunch with Bailey, time: 1200"},
    {"role": "user", "content": "I need to write my program, afterwards I need to get my passport"},
    {"role": "assistant", "content": "task1: write program, task2: get passport"}
  ]

  return message

def standard_chat():
  # This is used to prime the chatbot, or keep track of prior conversation
    messages=[
      {"role": "system","content": "You are a helpful assistant, your name is Sapphire.exe. Your purpose is to help your developer Chris manage his ADHD, schedule, and his projects. understanding that he has ADHD and will switch between multiple topics, you will use the given prompts and repsonses to help keep up with the conversations"},
      {"role": "user", "content": "What is your name?"},
      {"role": "assistant", "content": "My name is Sapphire.exe"}
    ]

    return messages

def print_help():
    print("(h)elp = print this help")
    print("exit = end the program")
    print("echo = print last output to a file")
    print("(i)gnore = ignore last user/assistant pair")
    print("show = show retained conversation")
    print("show unedited history = show the full, unedited transcript for this session")
    print("(s)ave = write currently retained conversation to log")
    print("(q)uicksave = quick save a file with the name "+default_log_name)
    print("(l)oad = load a conversation log for priming Sapphire")
    print("init = reset assistant to default")
    print("edit = edit transcript, select lines to keep")
    print("attach = append a file for context to the asked question")
    print("bash = drop to bash command line, then return here with "exit")
