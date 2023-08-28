import base64
import os
import requests
def scanVariables(text):
  prev=0
  commandList=[]
  commandNames=[]
  while True:
    
    if (text.find("var ",prev)) != -1:
        start=(text.find("var ",prev))+5
        end=text.find(" end!",prev)
        nameEnd=text.find(")",prev+5)
        commandList.append(text[nameEnd+2:end])
        commandNames.append(text[start:nameEnd])
        prev=end+4
    else:
      return commandList
def editVariable(text, variable, value):
  start_marker = f" ({variable}) "
  end_marker = " end!"
  start_location = text.find(start_marker)
  if start_location != -1:
    end_location = text.find(end_marker, start_location)
    if end_location != -1:
      text = text[:start_location + len(start_marker)] + value + text[end_location:]
  # Encode the new content in base64
  new_file_content_base64 = base64.b64encode(text.encode()).decode()
  # Create a JSON payload with the new file content and the current SHA
  data = {
      "message": "Update file via API",
      "content": new_file_content_base64,
      "sha": current_sha
  }
  # Make the API request to create/update the file
  response = requests.put(url, json=data, headers=headers)
def getText(username,repo_name,file_path,access_token):
  global url
  url = f'https://api.github.com/repos/{username}/{repo_name}/contents/{file_path}'
  global headers
  headers = {"Authorization": f"token {access_token}"}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
      current_file_info = response.json()
      global current_sha
      current_sha = current_file_info['sha']
      current_content = base64.b64decode(current_file_info['content']).decode()
      return current_content
