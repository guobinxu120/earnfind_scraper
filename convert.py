# -*- coding: utf-8 -*-
import xlrd, os, csv, xlsxwriter

# f2 = open('earnfind_b.csv')
# csv_items = csv.DictReader(f2)

validate_mails = []
with open('result_upc.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        i += 1
        # if len(row) < 1: continue
        if i<2000000: continue
        if i > 3000000: break
        validate_mails.append(row)

# for row in csv_items:
#     try:
#         validate_mails.append(row)
#     except:
#         continue
# f2.close()

filepath = 'eanfind_all2.xlsx'
if os.path.isfile(filepath):
    os.remove(filepath)
workbook = xlsxwriter.Workbook(filepath, {'strings_to_urls': False})
sheet = workbook.add_worksheet('sheet')
data = validate_mails
headers = ['Nom du produit','EAN','Marque','Modèle','Couleurs','Type de produit','Description','Chemin','Eanfind link']


print('---------------Writing in file----------------------')
print('total row: ' + str(len(data)))

for index, value in enumerate(data):
    for col, key in enumerate(value):
        # try:
        #     if key in value:
        sheet.write(index+1, col, key)

        # except:
        #     continue
    print('row :' + str(index))

workbook.close()