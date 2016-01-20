from Scrapers.tools import tools
from lxml.html import tostring

class RipleyInfo:
    """Model for each elements"""
    def __init__(self):
        self.name = None
        self.platform = None
        self.price = None
        self.stock = None
        self.url = None
        self.image_url = None


class Ripley:
    """Scrapping for www.ripley.cl"""
    def __init__(self):
        pass

    @staticmethod
    def scraper_dealer(url):
        """Get all url index from one platform
        :param url: to scraping
        http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/play-station?ic-cat-tecno
        http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/xbox?ic-cat-tecno
        http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/nintendo?ic-cat-tecno
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            max_products = html.cssselect('div.num_products')
            #print(tostring(max_products[0]))
            if max_products:
                max_products = max_products[0].text_content().strip()
                if max_products:
                    max_products = max_products.split()[-1]
                    #http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/play-station?ic-cat-tecno&beginIndex=0&pageSize=100
                    if max_products:
                        index = list(range(int(max_products)))[::24] ## cada 24 elementos, igual que en la web
                        for i in index:
                            url_max_prod = '{0}&beginIndex={1}&pageSize={2}'.format(url, i, 24)
                            urls.append(url_max_prod)
        return urls, http_code


    @staticmethod
    def scraper_links(url):
        """Get url index for ALL product by platform
        :param url: page
        :return: list of links urls
        http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/nintendo?ic-cat-tecno&beginIndex=0&pageSize=29'
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            links = html.cssselect('div.product > div.product_image > div.product_info')
            #print(tostring(links[0]))
            if links:
                for l in links:
                    l = l.cssselect('div.product_name > a')
                    #print(tostring(l[0]))
                    l = l[0].get('href')
                    urls.append(l)
        return urls, http_code


    @staticmethod
    def scraper_info(url):
        """Get all information of a game
        :param url: game link
        :return: class with all info
        http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/ver-todo-video-juegos/dragon-age-inquisition-2000349619428p
        """
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        product = RipleyInfo()

        name = html.cssselect('#catalog_link > span')
        #print(tostring(name[0]))
        if name:
            name = name[0].text_content().strip()
            name = tools.clear_name(name)
            product.name = name

        platform = html.cssselect('#Description > p:nth-child(3)')
        #print(tostring(platform[0]))
        if platform:
            platform = platform[0].text_content()
            platform = platform.replace('Juego','').strip()
            product.platform = tools.clear_platform(platform)

        price = html.cssselect('#WC_CachedProductOnlyDisplay_div_4 > p.ofomp') #precio Internet Oferta
        #print(tostring(price[0]))
        if price:
            price = price[0].text_content()
            price = price.split()[-1]
            price = price.replace('.', '').strip()
            price = price.replace('$', '').strip()
            product.price = price

        product.stock = ''
        product.url = url
        product.image_url = Ripley.get_image(url, html)
        print(vars(product))
        return product, http_code


    @staticmethod
    def get_image(url, html):
        if html is None:
            http = tools.get_html(url)
            html = http[2]
            #http_code = http[1]
        image_url = html.cssselect('#imagen-mini')
        print(tostring(image_url[0]))
        if image_url:
            image_url = image_url[0].get('src')
        else:
            image_url = ''
        return image_url

###################################################
#URL='http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/play-station?ic-cat-tecno'
#URL='http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/xbox?ic-cat-tecno'
#URL='http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/nintendo?ic-cat-tecno'
#Ripley.scraper_dealer(URL)
#URL='http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/play-station?ic-cat-tecno&beginIndex=0&pageSize=95'
#Ripley.scraper_links(URL)
#URL='http://www.ripley.cl/ripley-chile/tecnologia/videojuegos/play-station/fallout-4-2000354809289p'
#Ripley.scraper_info(URL)