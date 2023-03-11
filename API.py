import requests, json
from prettytable import PrettyTable

url = "https://api.notion.com/v1/pages"

token = ''
databaseId = ''


headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        "{}".format(json.dump(data, f, ensure_ascii=False,indent=2))
    with open('./db.json','r',encoding='utf8') as f:
      data = json.load(f)
    #print("{}".format(json.dumps(data,indent=2)))
    print(data["results"][1]["properties"]["Japanese"]["rich_text"][0]["plain_text"])

    result_len = len(data["results"])
    print(result_len)
    selected_rows = []
    for i in range(result_len):
      a = []
      japanese = data["results"][i]["properties"]["Japanese"]["rich_text"][0]["plain_text"]
      english = data["results"][i]["properties"]["English"]["title"][0]["plain_text"]
      a.append(japanese)
      a.append(english)
      selected_rows.append(a)
    print(selected_rows)

    table = PrettyTable()
    table.field_names = ["Japanese", "Englsih"]
    for row in selected_rows:
        table.add_row([row[0], row[1]])
    print(table)

# readDatabase(databaseId, headers)


def createPage(databaseId, headers):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
    "parent": { "database_id": databaseId },
	"properties": {
		"Japanese": {
      "rich_text": [
          {
              "type": "text",
              "text": {
                  "content": "どういたしまして",
              }
          }
      ]
  },
  "English": {
      "title": [
          {
              "type": "text",
              "text": {
                  "content": "You're welcome"
              }
          }
      ]
            }
       }
    }

    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    print(res.text)

createPage(databaseId, headers)

def updatePage(pageId, headers):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    updateData = {
        "properties": {
            "Value": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Pretty Good"
                        }
                    }
                ]
            }
        }
    }

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)

    print(response.status_code)
    print(response.text)

