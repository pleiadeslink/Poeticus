import scrapy, json, requests
from mastodon import Mastodon

class spider(scrapy.Spider):
    name = "Poeticus"
    title = ""
    poet = ""

    # Save URL from argument
    def __init__(self):
        poem = json.loads(requests.get("https://www.poemist.com/api/v1/randompoems").content)[0]
        self.title = poem["title"]
        self.poet = poem["poet"]["name"]
        self.start_urls = [poem["url"]]
        
    # Find poem by css tag and save it into txt file
    def parse(self, response):

        # Mastodon token and domain
        mastodon = Mastodon(
            access_token = "asdf",
            api_base_url = "https://domain.com/"
        )

        string = self.title.strip() + " by " + self.poet.strip() + "\n\n"

        imported = response.css('.poem-content::text')
        text = imported.getall()

        string += text[0].strip() + "\n"
        for i in range(1, len(string)):
            if(len(string) < 450 and text[i] != "\n" and text[i] != "\n\n"  and text[i] != "\n\n\n" and text[i] != "I\n" and text[i] != "II\n" and text[i] != "*\n"):
                string += text[i].strip() + "\n"

        mastodon.status_post(string)