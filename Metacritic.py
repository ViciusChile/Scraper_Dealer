from Scrapers.tools import tools


class MetacriticInfo:
    """Model for each elements"""

    def __init__(self):
        self.name = None
        self.platform = None
        self.developer = None
        self.publisher = None
        self.esrb = None
        self.release = None
        self.tags = None
        self.metascore = None
        self.official_site = None
        self.description = None
        self.num_players = None
        self.sound = None
        self.connectivity = None
        self.resolution = None
        self.num_online = None
        self.customization = None
        self.image_mini = None
        self.url = None
        self.url_amazon = None


class Metacritic:
    """Scrapping for www.metacritic.com"""

    def __init__(self):
        pass

    @staticmethod
    def scraper_dealer(url):
        """Get url index from one platform an letter
        :param url: to scraping
        http://www.metacritic.com/browse/games/title/ps4    /a
        """
        url_pages = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            pages = html.cssselect('#main > div.module.filter.alpha_filter > div.page_nav > div > div.pages > ul > li')
            if pages:
                q = len(pages)
            else:
                q = 1
            for i in range(0, q):
                url_pages.append('{0}?view=condensed&page={1}'.format(url, i))
        return url_pages, http_code

    @staticmethod
    def scraper_links(url):
        """Get url index from one platform an letter
        :param url: page with many links
        :return: list of links urls
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            links = html.cssselect(
                '#main > div.module.filter.alpha_filter > div > div.body > div.body_wrap > div > ol > li > div > div.basic_stat.product_title > a')
            if links:
                for l in links:
                    urls.append(l.get('href') + '/details')
        return urls, http_code

    @staticmethod
    def scraper_info(url):
        """Get all information of a game
        :param url: game link
        :return: class with all info
        """
        http = tools.get_html(url)
        page = http[2]
        http_code = http[1]
        product = MetacriticInfo()

        name = page.cssselect('#main > div.content_head.product_content_head.game_content_head > div.product_title > a')
        if not name:
            name = page.cssselect('#main > div.content_head.product_content_head.game_content_head > h1 > a')

        if name:
            product.name = name[0].text_content().strip()


        platform = page.cssselect('#main > div.content_head.product_content_head.game_content_head > div.product_title > span > a')

        if not platform:
            platform = page.cssselect('#main > div.content_head.product_content_head.game_content_head > h1 > span > a')

        if platform:
            platform = platform[0].text_content().strip()
            product.platform = tools.clear_platform(platform).upper()

        publisher = page.cssselect(
            '#main > div.content_head.product_content_head.game_content_head > div.product_data > ul > li.summary_detail.publisher > span.data > a')
        if publisher:
            product.publisher = publisher[0].text_content().strip()

        release = page.cssselect(
            '#main > div.content_head.product_content_head.game_content_head > div.product_data > ul > li.summary_detail.release_data > span.data')
        if release:
            product.release = release[0].text_content().strip()

        metascore = page.cssselect(
            '#main > div.module.product_data > div > div.summary_wrap > div.section.product_scores > div.details.main_details > div > div > a > div > span')
        if metascore:
            product.metascore = metascore[0].text_content().strip()

        product_description = page.cssselect(
            '#main > div.module.product_data > div > div.summary_wrap > div.section.product_details > div > span.data')
        if product_description:
            product.description = product_description[0].text_content()

        og_image = page.cssselect('meta[name="og:image"]')
        if og_image:
            product.image_mini = og_image[0].get('content')

        product_details = page.cssselect('#main > div.product_details > table')
        if product_details:
            for i in product_details:
                for e in i:
                    th = e.cssselect('th')
                    td = e.cssselect("td")
                    th_val = th[0].text_content().replace(":", "").strip()
                    td_val = td[0].text_content().strip()
                    if th_val == "Rating":
                        product.esrb = td_val
                    elif th_val == "Official Site":
                        product.official_site = td_val
                    elif th_val == "Developer":
                        product.developer = td_val
                    elif th_val == "Genre(s)":
                        product.tags = td_val
                    elif th_val == "Number of Players":
                        product.num_players = td_val
                    elif th_val == "Sound":
                        product.sound = td_val
                    elif th_val == "Connectivity":
                        product.connectivity = td_val
                    elif th_val == "Resolution":
                        product.resolution = td_val
                    elif th_val == "Number of Online Players":
                        product.num_online = td_val
                    elif th_val == "Customization":
                        product.customization = td_val

        product_url = page.cssselect('#main > div.content_head.product_content_head.game_content_head > div.product_title > a')
        if product_url:
            product.url = product_url[0].get('href')

        #url_amazon = page.cssselect('#main > div.module.product_data > div > div.summary_wrap > div.section.product_details > div.amazon_wrapper > a')
        url_amazon = page.cssselect('#main > div.module.product_data > div > div.summary_wrap > div.section.product_details > div.esite_list > div.esite_items > div.esite_btn_wrapper > div.esite_btn > table > tr > td.esite_img_wrapper > a')
        #print('url_amazon', url_amazon)
        if url_amazon:
            product.url_amazon = url_amazon[0].attrib['href']
        return product, http_code

# ------------------------------------------------------------------------------ #

#from pprint import pprint
#pprint(Metacritic.scraper_pages('pc', letter))
#pprint(Metacritic.scraper_links('http://www.metacritic.com/browse/games/title/pc/u?view=condensed&page=1'))
#Metacritic.scraper_info('http://www.metacritic.com/game/playstation-4/fallout-4/details')

#platforms = ['ps4', 'xboxone', 'ps3', 'xbox360', 'pc', 'wii-u', '3ds', 'vita']
#letters = list('#' + string.ascii_lowercase)







