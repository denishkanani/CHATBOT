import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0 Safari/537.36"
            )
        }

    def scrape(self, url):
        """
        Scrape webpage and return title + clean text.
        """

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted tags
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            title = (
                soup.title.string.strip()
                if soup.title and soup.title.string
                else "No Title"
            )

            text = soup.get_text(separator=" ", strip=True)

            return {
                "url": url,
                "title": title,
                "content": text
            }

        except Exception as e:
            return {
                "url": url,
                "title": "",
                "content": "",
                "error": str(e)
            }


# Example usage
if __name__ == "__main__":
    scraper = WebScraper()

    data = scraper.scrape("https://en.wikipedia.org/wiki/Artificial_intelligence")

    print("Title:")
    print(data["title"])

    print("\nFirst 1000 characters:\n")
    print(data["content"][:1000])