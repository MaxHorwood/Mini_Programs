from bs4 import BeautifulSoup
import requests

# Words that I want to be searched for
# WANTED_WORDS = ["computer", "warehouse", "leaflet", "leafleting", "student", "summer", "p/t", "part time"]
WANTED_WORDS = ["IT", "part", "time"]
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
    for _, item in enumerate(WANTED_WORDS):
        if item in desc:
            # Replace the given word wrapped <b> tags
            # Adding bold tags to just the keyword in the sentence
            textToWrite = desc.replace(item, '<b class=\"keyword\">'+item+'</b>')
            # Now wrap the whole sentance (job) in a span, so can be styled sepratly
            textToWrite = "<span class=\"job\">"+textToWrite+"</span>\n"
            fileWrite(fileName+".html", textToWrite)

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

    # Find all job descriptions
    for jobDesc in table.findAll('span', attrs={'class': 'a-text'}):
        lookForWord(jobDesc.text, fileName) # Looking for defined keywords

    # FINISH GENERATING HTML (add closing body tag)
    fileWrite(fileName+".html", HTML_END)

main()
