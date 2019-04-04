
from scrapy import Request
import scrapy
from scrapy.item import Item, Field


class SiteProductItem(Item):

    Date = Field()
    Time = Field()
    VisitorTeam = Field()
    HomeTeam = Field()
    # Scores = Field()


class ZillowScraper (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.baseball-reference.com']
    DOMAIN_URL = 'https://www.baseball-reference.com'
    START_URL = 'https://www.baseball-reference.com/leagues/MLB/2017-schedule.shtml'
    # settings.overrides['ROBOTSTXT_OBEY'] = False

    def __init__(self, **kwargs):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/70.0.3538.102 Safari/537.36"}

    def start_requests(self):
        yield Request(url=self.START_URL,
                      callback=self.get_boxscore_urls,
                      headers=self.headers,
                      dont_filter=True
                      )

    def get_boxscore_urls(self, response):

        boxscore_urls = response.xpath('//p[@class="game"]/em/a/@href').extract()

        for boxscore_url in boxscore_urls:
            url = self.DOMAIN_URL + boxscore_url
            yield Request(url=url,
                          callback=self.parse_detail,
                          dont_filter=True,
                          headers=self.headers
                          )

    def parse_detail(self, response):

        product = SiteProductItem()

        Date = self._parse_Date(response)
        product['Date'] = Date

        Time = self._parse_Time(response)
        product['Time'] = Time

        VisitorTeam = self._parse_VisitorTeam(response)
        product['VisitorTeam'] = VisitorTeam

        HomeTeam = self._parse_HomeTeam(response)
        product['HomeTeam'] = HomeTeam
        #
        # Scores = self._parse_Scores(response)
        # product['Scores'] = Scores

        yield product

    @staticmethod
    def _parse_VisitorTeam(response):
        team_names = response.xpath('//div[@class="scorebox"]//strong/a/text()').extract()
        return str(team_names[0]) if team_names else None

    @staticmethod
    def _parse_HomeTeam(response):
        team_names = response.xpath('//div[@class="scorebox"]//strong/a/text()').extract()
        return str(team_names[1]) if team_names else None

    @staticmethod
    def _parse_Date(response):
        game_infos = response.xpath('//div[@class="scorebox_meta"]/div/text()').extract()
        return str(game_infos[0]) if game_infos else None

    @staticmethod
    def _parse_Time(response):
        game_infos = response.xpath('//div[@class="scorebox_meta"]/div/text()').extract()
        return str(game_infos[1]) if game_infos else None
    #
    # @staticmethod
    # def _parse_Scores(response):
    #
    #     visitor_team_name = response.xpath('//p[@class="game"]/em/a/@href').extract()
    #     return str(visitor_team_name) if visitor_team_name else None


