from Scrapers.tools import tools
from lxml.html import tostring

class WeplayInfo:
    """Model for each elements"""
    def __init__(self):
        self.name = None
        self.platform = None
        self.price = None
        self.stock = None
        self.url = None
        self.image_url = None


class Weplay:
    """Scrapping for www.weplay.cl"""

    def __init__(self):
        pass

    @staticmethod
    def scraper_dealer(url):
        """Get all url index from one platform
        :param url: to scraping
        http://www.weplay.cl/resultado/juegos+ps4
        """
        url_pages = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]

        for i in range(1,100):
            url_base = '{0}/{1}/creacion_mayor/'.format(url,i)
            url_pages.append(url_base)
            http = tools.get_html(url_base)
            html = http[2]
            if html is not None:
                next_button = html.cssselect('#cont-paginacion > a > input[type="button"]')
                if next_button:
                    if not 'siguiente' in next_button[0].get('value'):
                        break #exit if not 'siguiente button'
                else:
                    break #exit if no button
        return url_pages, http_code


    @staticmethod
    def scraper_links(url):
        """Get url index for ALL product by platform
        :param url: page
        :return: list of links urls
        GET stock not works
        http://www.weplay.cl/resultado/juegos+ps4/1/creacion_mayor/
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            links = html.cssselect('#cont-cont > div.prod_b > a:nth-child(1)')
            if links:
                for l in links:
                    urls.append(l.get('href'))
        return urls, http_code


    @staticmethod
    def scraper_info(url):
        """Get all information of a game
        :param url: game link
        :return: class with all info
        http://www.weplay.cl/store/1579-thief_ps4
        """
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        product = Weplay()

        name = html.cssselect('#tit-prod > div.enc_prod_fich > h1')
        if name:
            name = name[0].text_content().strip()
            name = tools.clear_name(name)
            product.name = name

        platform = url.split('_')[-1]
        #TODO: can be better
        if platform in ['u','u_','u__']:
            product.platform = 'WIIU'
        else:
            product.platform = tools.clear_platform(platform).upper()

        if not platform:
            platform_img = html.cssselect('#logo_plat > img')
            if platform_img:
                platform_img = platform_img[0].get('src')
                if platform_img:
                    platform_img = platform.split('/')[-1]
                    if 'wiiu' in platform_img:
                        product.platform = 'WIIU'
        #-----

        if not platform:
            platform = html.cssselect('#tit-prod > div.enc_prod_fich > h1')
            if platform:
                platform = platform[0].text_content()
            if 'ps4' in platform.lower():
                product.platform = 'PS4'
            if 'xbox one' in platform.lower():
                product.platform = 'XONE'
            if 'wiiu' in platform.lower():
                product.platform = 'WIIU'
            if 'wii u' in platform.lower():
                product.platform = 'WIIU'
            if 'wii' in platform.lower():
                product.platform = 'WII'

        price = html.cssselect('#cont-cont > div.cont-full-single > div.cont-single-h > h1')
        if price:
            price = price[0].text_content()
            if '$' in price:
                price = price.split('$')[1].replace('.', '').strip()
                product.price = price

    #cont-cont > div > div:nth-child(3) > p:nth-child(8)

        if 'Preventa' in url:
            product.stock = 'Preventa'
        else:
            stock = html.cssselect('#cont-cont > div.cont-full-single > div.cont-single-h > p')
            #print(tostring(stock[0]))
            if stock:
                stock = stock[1].text_content().strip()
                product.stock = stock

        product.url = url
        product.image_url = Weplay.get_image(url, html)
        #print(vars(product))
        #print(product.price)
        return product, http_code


    @staticmethod
    def get_image(url, html):
        if html is None:
            http = tools.get_html(url)
            html = http[2]
            #http_code = http[1]

        image_url = html.cssselect('#cont-cont > div > div.cont-single-img > img')
            #print(tostring(image_url[0]))
        if image_url:
            image_url = image_url[0].get('src')
        if image_url == []:
            image_url = ''
        return image_url

#cont-cont > div > div.cont-single-img > img

### TEST #######
#Weplay.scraper_dealer('http://www.weplay.cl/resultado/juegos+ps4')
#Weplay.scraper_links('http://www.weplay.cl/resultado/juegos+ps4/1/creacion_mayor/')
#Weplay.scraper_info('http://www.weplay.cl/store/3613-fifa_16_deluxe_edition_xbox_one')

#print(Weplay.get_image('http://www.weplay.cl/store/3613-fifa_16_deluxe_edition_xbox_one'))
