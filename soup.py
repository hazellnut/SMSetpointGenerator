import bs4
import csv

with open("C:/Users/Tom Work/source/repos/TwinCAT Project15/TwinCAT Project15/TwinCAT Project15.tsproj") as f:
    soup = bs4.BeautifulSoup(f,features="lxml-xml")

boxes = soup.find_all("Box")

with open("newfile.csv","w+",newline='') as csvfile:
    writer = csv.writer(csvfile)
    for box in boxes:
        cat = box.EtherCAT
        try:
            desc = cat["Desc"]
            code = cat["ProductCode"]
            rev = cat["RevisionNo"]
            type = cat["Type"]
            vid = cat["VendorId"]
            writer.writerow([desc,code,rev,vid,type])
        except KeyError:
            break