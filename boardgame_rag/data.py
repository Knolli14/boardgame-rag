import os

from boardgame_rag.params import LOCAL_DATA_PATH

def save_pdf(content, title):


    filepath = os.path.join(LOCAL_DATA_PATH, "gb_manuals", title+".pdf")

    if not os.path.exists(filepath):
        with open(filepath, "wb") as output:
            output.write(content)
