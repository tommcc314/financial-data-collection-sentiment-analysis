#This code takes as input a CSV file path and cleans the text in the CSV.
import sys
import re
import csv
def clean_csv(file_name): 
    csv_rows = []
    with open(file_name) as readfile:
        csv_reader = csv.DictReader(readfile,delimiter= ",")
        for row in csv_reader:
            csv_rows.append([row["Name"], row["Date of 10k Filing"], clean(row["1A"]), clean(row["7"])])
    with open(file_name, mode = "w") as writefile:
        writer = csv.writer(writefile)
        writer.writerow(["Name", "Date of 10k Filing", "1A", "7"])
        for row in csv_rows:
            writer.writerow([row[0], row[1], row[2], row[3]])

def clean(text):
    replace = {
        #replace codes with characters
        "&#8226;": "",
        "&#8203;": "",
        "&#160;": "",
        "&#8212;":"—",
        "&#8209;": "-",
        "&#8211;": "-",
        "&#8220;": "\"",
        "&#8221;": "\"",
        "&#8217;":"\'",
        "&#146;": "\'",
        "&#147;": "\"",
        "&#148;": "\"",
        "&#38;": "&"        
    }
    for key in replace:
        text = re.sub(key, replace[key], text)
    text = re.sub("&#.*?;", "", text)
    return text
if __name__ == "__main__":
    clean_csv(sys.argv[1])
