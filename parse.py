from bs4 import BeautifulSoup as bs
import pandas as pd
import os, re
import string 

def parse_xml_to_csv(path='/mnt/c/Users/gainyny/workspace/github/CS728/data_assn1/Train/Source', csvname="parsed_data.csv", test=0):
    files = []
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            files.append(os.path.join(path, filename))
        else:
            continue

    rows = []
    for f in files:
        content = []

        with open(f, "r") as file:
            content = file.readlines()
            content = "".join(content)
            bs_content = bs(content, "xml")

        df_cols = ["context_left", "context_right", "head"]
        if not test:
            df_cols.append("Sense ID")
        else:
            df_cols.append("sentence")

        instances = bs_content.findAll('instance')

        for inst in instances:
            ID = inst.get('id')
            context_left, head_tag, context_right = inst.find('context').contents
            context_left = re.split(r'\W+', context_left)
            context_right = re.split(r'\W+', context_right)
            head = head_tag.text
            if test:
                rows.append({"head": head,
                        "context_left": " ".join(context_left).split()[-2:] ,
                        "context_right": " ".join(context_right).split()[:2],
                        "sentence": context_left+head+context_right})
            else:
                sense_id = inst.find('answer').get('senseid')
                rows.append({"Sense ID": sense_id, "head": head,
                            "context_left": " ".join(context_left).split()[-2:] , "context_right": " ".join(context_right).split()[:2]})

        out_df = pd.DataFrame(rows, columns = df_cols)

    out_df.to_csv(csvname)

if __name__ == '__main__':
    train_path = '/mnt/c/Users/gainyny/workspace/github/CS728/data_assn1/Train/Source'
    test_path = '/mnt/c/Users/gainyny/workspace/github/CS728/data_assn1/Test/Source'
    parse_xml_to_csv(train_path, csvname="train_parsed_data.csv")
    parse_xml_to_csv(test_path, csvname="test_parsed_data.csv", test=1)
