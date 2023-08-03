import re


class DiscogsMarketplaceParser:
    def __init__(self, soup: object):
        """
        Parser class for Discogs marketplace items.

        Available getters:
            * artist
            * title
            * label
            * number_of_tracks
            * release_date
            * price
            * rating
            * votes
            * have
            * want
            * limited_edition
            * release_format
            * media_condition
            * sleeve_condition

        :param soup: BeautifulSoup object
        """
        self.__soup = soup
        if self.item_exists:
            self.__ratings_section = self.__soup.select("div.release_info_buttons > div")[0].text
            self.__release_info = (" ".join(self.__soup.select("div.head:-soup-contains('Format')")[0]
                                            .find_next_sibling("div").text.split()))

    @property
    def item_exists(self) -> bool:
        if not self.__soup.select("div.release_info_buttons > div"):
            return False
        return True

    @property
    def artist(self) -> str:
        return self.__soup.select("div.profile > h1 > span > span")[0].text.strip()

    @property
    def title(self) -> str:
        return self.__soup.select("div.profile > h1 > span")[1].text.strip()

    @property
    def label(self) -> str:
        return " ".join(self.__soup.select("div.head:-soup-contains('Label')")[0]
                        .find_next_sibling("div").text.replace("\n", "").split())

    @property
    def number_of_tracks(self) -> int:
        return len(self.__soup.find_all("tr", class_="tracklist_track"))

    @property
    def release_date(self) -> str:
        return " ".join(self.__soup.select("div.head:-soup-contains('Released')")[0]
                        .find_next_sibling("div").text.split())

    @property
    def price(self) -> float:
        return self.__soup.select("span.price")[0].text.replace("€", "").strip()

    @property
    def rating(self) -> str:
        if "No Rating Yet" in self.__ratings_section:
            return "N/A"
        else:
            return self.__soup.select("span.rating_value_sm")[0].text

    @property
    def votes(self) -> str:
        if "No Rating Yet" in self.__ratings_section:
            return "N/A"
        else:
            return re.search("of (.*) votes", self.__soup.select("span.rating_value_sm")[0].next_sibling).group(1)

    @property
    def have(self) -> str:
        if "No Rating Yet" in self.__ratings_section:
            return re.search("\\((.*) have", self.__ratings_section).group(1)
        else:
            return re.search("\\((.*) have", self.__soup.select("span.rating_value_sm")[0].next_sibling).group(1)

    @property
    def want(self) -> str:
        if "No Rating Yet" in self.__ratings_section:
            return re.search(", (.*) want", self.__ratings_section).group(1)
        else:
            return re.search(", (.*) want", self.__soup.select("span.rating_value_sm")[0].next_sibling).group(1)

    @property
    def limited_edition(self) -> int:
        if "Limited Edition" in self.__release_info:
            return 1
        else:
            return 0

    @property
    def release_format(self) -> str:
        return re.search("Vinyl, (.*)", self.__release_info).group(1).split(None, 1)[0].replace(",", "")

    @property
    def media_condition(self) -> str:
        return " ".join(self.__soup.select("strong:-soup-contains('Media:')")[0].find_next_sibling("span").text.split())

    @property
    def sleeve_condition(self) -> str:
        if not self.__soup.select("strong:-soup-contains('Sleeve:')"):
            return "N/A"
        return self.__soup.select("strong:-soup-contains('Sleeve:')")[0].next_sibling.strip()

    @property
    def release_page_url(self) -> str:
        return f'https://discogs.com{self.__soup.select("a.release-page")[0]["href"]}'


class DiscogsSearchParser:
    def __init__(self, soup: object):
        """
        Parser class for Discogs marketplace items.

        Available getters:
            * artist
            * title
            * label
            * number_of_tracks
            * release_date
            * price
            * rating
            * votes
            * have
            * want
            * limited_edition
            * release_format
            * media_condition
            * sleeve_condition

        :param soup: BeautifulSoup object
        """
        self.__soup = soup

    @property
    def artist(self) -> str:
        return self.__soup.select("#page > div > div:nth-child(2) > div > h1 > span > a")[0].text.strip()

    @property
    def title(self) -> str:
        release_text = self.__soup.select("#page > div > div:nth-child(2) > div > h1")[0].text
        return release_text.replace(
            self.__soup.select("#page > div > div:nth-child(2) > div > h1 > span > a")[0].text.strip(), "")[3:]

    def price(self) -> float | None:
        try:
            return self.__soup.select("#master-release-marketplace > header > div > span > span")[0].text.replace('\\xa','')
        except:
            print("Price could not be scraped")
            return None


    @property
    def have(self) -> int:
        return int(
            self.__soup.select("#master-statistics > div > div > div:nth-child(1) > ul > li:nth-child(1) > a")[0].text)

    @property
    def want(self) -> int:
        return int(
            self.__soup.select("#master-statistics > div > div > div:nth-child(1) > ul > li:nth-child(2) > a")[0].text)

    @property
    def url(self) -> str:
        return f'https://discogs.com/master/{self.__soup.select("#master-actions > header > button > span")[0].text.replace("[", "").replace("]", "").replace("m", "")}'
