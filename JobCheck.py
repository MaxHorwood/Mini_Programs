from bs4 import BeautifulSoup
import requests, os

# Words that I want to be searched for
WANTED_WORDS = ["computer", "student", "summer", "part time"]

# Used for the start of the HTML, will insert job in the main program
HTML_START = """
<head>
    <style>
        body{
            max-width: 900px;
            margin: 0 auto;
            font-family:verdana;
        }
        .job {
            padding:10px;
            background-color:#1258DC;
            display:block;
            border-bottom:1px solid white;
            color:#DEE9FC;
            font-size: 20px;
        }
        .keyword {
            color:#FDB768;
        }
        .keywords {
            padding:20px;
            text-align:center;
            background-color:#0A337F;
            color:#6395F2;
            margin:0;
        }
    </style>
</head>
<body>
"""

# Closing tag for the HTML
HTML_END = """
</body>
"""

# Looks for a particular word in a String
def lookForWord(desc, fileName):
    tempText = ""
    for _, item in enumerate(WANTED_WORDS):
        if item in desc:
            # Adding bold tags to just the keyword in the sentence
            tempText = desc.replace(item, '<b class=\"keyword\">'+item+'</b>')
    # Don't want empty span tags...
    if (tempText != ""):
        # Now wrap the whole sentence (job) in a span, so can be styled sepratly
        tempText = "<span class=\"job\">"+tempText+"</span>\n"
    return tempText

# Appends a given file
def fileWrite(file_name, text):
    f = open(file_name, 'a')
    f.write(text)
    f.close()

def main():
    try:
        fileName = input("File Name: ")
    except (IOError, OSError) as ex:
        print ("File error: ", ex)

    # GENERATE THE HTML START CODE
    tempInfo = "<h2 class=\"keywords\">KEYWORDS I LOOKED FOR<br>"
    fileWrite(fileName+".html", HTML_START)

    for word in WANTED_WORDS:
        tempInfo = tempInfo + word + " - "
    tempInfo = tempInfo + "</h2>"

    fileWrite(fileName+".html", tempInfo)

    # Getting the HTML data
    response = requests.get('http://www.dailyinfo.co.uk/jobs')

    # Sorts it for BS. So I can 'find'
    soup = BeautifulSoup(response.content, "html.parser")

    # Looks for ul tags with certain attrs
    table = soup.find('div', attrs={'class': 'row aboard-free'})

    textToWrite = ""
    # Find all job descriptions
    for jobDesc in table.findAll('span', attrs={'class': 'a-text'}):
        textToWrite = textToWrite + lookForWord(jobDesc.text, fileName) # Looking for defined keywords
    # If Nothing is found
    if (textToWrite == ""):
        textToWrite = "<span class=\"job\">Nothing Found!</span>"
    # FINISH GENERATING HTML (add closing body tag)
    fileWrite(fileName+".html", textToWrite+HTML_END)
    # Auto open file
    os.system('start ' + fileName + '.html')
main()
