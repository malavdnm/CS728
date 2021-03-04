from bs4 import BeautifulSoup as bs
import pandas as pd
import os

path = '/home/gainyny/Downloads/data_assn1/data_assn1/Train/Source'
files = []
for filename in os.listdir(path):
    if filename.endswith('.xml'):
        files.append(os.path.join(path, filename))
    else:
        continue

for f in files:
    content = []

    with open(f, "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = bs(content, "xml")

    df_cols = ["ID", "Sense ID", "head", "context_left", "context_right"]
    rows = []

    instances = bs_content.findAll('instance')

    for inst in instances:
        ID = inst.get('id')
        sense_id = inst.find('answer').get('senseid')
        context_left, head_tag, context_right = inst.find('context').contents
        head = head_tag.text
        rows.append({"ID": ID, "Sense ID": sense_id, "head": head,
                    "context_left":context_left , "context_right":context_right})

    out_df = pd.DataFrame(rows, columns = df_cols)
    print(out_df)

