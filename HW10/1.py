from smolagents.agents import ToolCallingAgent
from smolagents import tool, LiteLLMModel
from smolagents import OpenAIServerModel
import subprocess
import os
import IPy 
import requests

# 使用ollama api
model = LiteLLMModel(
   model_id="ollama_chat/llama3.2:latest",
   api_base="http://127.0.0.1:11434",
   api_key="ollama",
   temperature=0
)

# model=OpenAIServerModel(
#             model_id="gemini-2.0-flash-exp ",
#             api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
#             api_key="",
#             temperature=0
#         ) 

def is_ip(address):  
    try:  
        IPy.IP(address)  
        return True  
    except Exception as  e:  
        return False
        
@tool
def pingtestwithip(ip: str) -> str:
    """
    Try to answer whether provided the ip address can be pinged or not
    
    Args:
        ip: provided ip address for ping test

    Returns:
        ping test result or return that the provided ip address is not legal address
    """
    
    answer=is_ip(ip)
    
    if not answer:
      return "please provide the legal ip address"
    
    command="ping -c 1 -W 1 " + ip + " 1>/dev/null 2>&1 ; echo $? >/tmp/result"
    print("command=", command)
    os.system(command)
    f = open("/tmp/result", "r")
    result=f.read()
    f.close()
    if '0' in result:
      return "ping test ok"
    else:
      return "ping test failed"

@tool
def DN2IP(dn: str) -> str:
    """
    Answer the ip address for the provided domain name
    
    Args:
        dn: domain name 

    Returns:
        return the resolved IP address
    """
    command="dig +short " + dn + " >/tmp/result"
    print("command=", command)
    os.system(command)
    f = open("/tmp/result", "r")
    result=f.read()
    f.close() 
    return result

@tool
def sendmsg2TG(msg: str) -> str:
    """
    Send a message to telegram
    
    Args:
        msg: the provided message that is needed to send to telegram 
        
    Returns:
        return send result: done or failed
    """
    assert type(msg) == str, "傳入訊息必須為字串"
    #7580013563:AAHuK-7Hz-gOj_WpF8h8TvGNIYkxbUCP70g
    token=""
    chatID="-4783058800"
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chatID}&text={msg}'
    result=requests.get(url)
    print("result=", result)
    if "200" in str(result):
      print("done")
      return "done"
    else:
      print("failed") 
      return "send failed"  


@tool
def is_apache2_running() -> str:
    """
    Check if the apache2 server is running on the local machine.
    
    Returns:
        str: A message indicating if the apache2 service is running or not.
    """
    # 使用 systemctl 檢查 apache2 服務狀態
    command = "systemctl is-active apache2"
    result = os.popen(command).read().strip()  # 執行命令並讀取結果
    
    if result == "active":
        return "Apache2 server is running."
    else:
        return "Apache2 server is not running."

@tool
def install_software(software_name: str) -> str:
    """
    Try to install the software
    
    Args:
        software_name: the software name 

    Returns:
        installation status: failed, installed, or already installed
    """
    command="sudo dpkg -l | grep " + software_name + " 1>/dev/null 2>&1 ; echo $? >/tmp/result"
    print("command=", command)
    os.system(command)
    f = open("/tmp/result", "r")
    result=f.read()
    f.close()
    if '0' in result:
      return "already installed"
    else:
      command="sudo apt install -y " + software_name + " 1>/dev/null 2>&1 ; echo $? >/tmp/result"
      print("command=", command)
      os.system(command)
      f = open("/tmp/result", "r")
      result=f.read()
      f.close()
      if '0' in result:
        return "installed"
      else:
        return "failed"


agent = ToolCallingAgent(tools=[DN2IP, pingtestwithip, sendmsg2TG,install_software], model=model)

#print(agent.run("can i ping www.google.com?"))
#print(agent.run("What is the IP address for www.google.com ?"))
#print(agent.run("can i ping 8.8.8.8 ?"))
#print(agent.run("can i ping www.google.com ? And send the result to telegram."))
while True:
    user_input = input("User : ")
    if (user_input.lower()=="bye"):
        print( "Ok Bye")
        break
    else:
        print("ChatBot : ")
        print(agent.run(user_input))