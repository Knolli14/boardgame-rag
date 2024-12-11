import os
import json

from boardgame_rag.params import LOCAL_DATA_PATH

def save_pdf(content, title):

    filepath = os.path.join(LOCAL_DATA_PATH, "gb_manuals", title+".pdf")

    if not os.path.exists(filepath):
        with open(filepath, "wb") as output:
            output.write(content)


def load_json(filepath):

    if os.path.exists(filepath):
        with open(filepath) as file:
            return json.load(file)
    else:
        print("No such file!")
        return None


def save_to_json(filepath, content):

    with open(filepath, "w") as output:
        output.write(json.dumps(content))

    return None
