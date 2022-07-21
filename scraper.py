from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests

# Abstractmethod
class Food(ABC):

    def __init__(self, area="台北市"):
        self.area = area
    
    @abstractmethod
    def scrape(self):
        pass

# Ifoodie #inheritance from food
class Ifoodie(Food):
    def scrape(self):
        response = requests.get("https://ifoodie.tw/explore/" + self.area + "/list?sortby=rating&opening=true")
        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all('div', {'class': 'jsx-3292609844 restaurant-info'}, limit=5)
        content = ""
        for card in cards:
            title = card.find("a", {"class", "jsx-3292609844 title-text"}).getText()
            content += f"{title}\n"
        return content

# food = Ifoodie()
# print(food.scrape())