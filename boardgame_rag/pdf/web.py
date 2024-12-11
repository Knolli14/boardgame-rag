import requests

from bs4 import BeautifulSoup

from boardgame_rag.data import save_pdf, load_json, save_to_json
from boardgame_rag.params import MAX_SEARCH_PAGE

class PDFExtractor:
    ''' Class handling Extraction from web '''

    URL = "https://en.1jour-1jeu.com/rules/search?page="
    MAX_SEARCH_PAGE = MAX_SEARCH_PAGE

    def __init__(self, games_list=None):
        self.games_list = games_list if games_list else []


    def extract_games_list(self, language="English") -> list:
        ''' Ectract a List of dicts with url and title of Boardgames '''

        # helper function to extract title
        def _extract_title(url) -> str:
            ''' Extract title out of link'''

            title_full = url.split("/")[-1] \
                            .strip(".pdf")

            return " ".join(title_full.split("-")[1:-1])

        # helper function to get soup and extract tags
        def _extract_tags(page):

            # get soup of a page
            response = requests.get(PDFExtractor.URL + str(page))
            soup = BeautifulSoup(response.content, "html.parser")

            # find all games tags on a page
            tag_results = soup.find_all(
                class_="btn btn-sm btn-secondary mb-1",
                title="In "+language
            )

            return tag_results

        # loop over all pages
        for page in range (self.MAX_SEARCH_PAGE+1):
            print("Extracting URLs and titles from page:", page)

            # extract tags
            tags = _extract_tags(page)

            # loop over games in tags
            for game in tags:

                # extract {url, title}
                url = game.get("href")
                title = _extract_title(url)

                # add to self. games_info_list
                self.games_list.append({
                    "title": title,
                    "url": url
                })
                print(title, "was added to games_list")

        print(30*'-',
              str(len(self.games_list)) + "games have been added in total",
              sep="\n")


    def save_games_list(self):
        ''' saves extracted urls and title locally as json'''

        if self.games_list:
            save_to_json("games_list.json", self.games_list)
            print("Successfully saved to './games_list.json'")

        else:
            print("No games_list extrcted yet!")


    def download_pdfs(self):
        ''' downloads the games saved in the games_list'''

        for game in self.games_list:

            title = game["title"]
            content = requests.get(game["url"]).content
            save_pdf(content, title)
            print(title, "has been saved.")

        return None


    # Class Methods

    @classmethod
    def from_json(cls):

        games_list = load_json("games_list.json")
        print("Successfully loaded 'games_list.json' into PDFExtractor")

        return cls(games_list=games_list)


if __name__ == "__main__":
    pass
