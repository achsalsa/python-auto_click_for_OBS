import csv
 
# opening the CSV file
with open('./ensembles des sites.csv', mode ='r', encoding="utf8")as file:
   
  # reading the CSV file
  csvFile = csv.reader(file)
 
  # displaying the contents of the CSV file
  for lines in csvFile:
        print(lines[0])