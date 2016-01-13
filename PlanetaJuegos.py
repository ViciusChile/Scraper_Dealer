from Scrapers.tools import tools
from lxml.html import tostring

class PlanetaJuegosInfo:
    """Model for each elements"""
    def __init__(self):
        self.name = None
        self.platform = None
        self.price = None
        self.stock = None
        self.url = None
        self.image_url = None

class PlanetaJuegos:
    """Scrapping for www.planetajuegos.cl"""

    def __init__(self):
        pass

    @staticmethod
    def scraper_dealer(url):
        pass

    @staticmethod
    def scraper_links(url):
        """Get url index for ALL product by platform
        :param url: page
        :return: list of links urls
        GET stock not works
        http://www.planetajuegos.cl/catalogo.php?consola=PS4&categoria=T&display=listado&stock=T
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            links = html.cssselect('td.consola_pr > a')
            #print(tostring(links[0]))
            if links:
                for l in links:
                    urls.append(l.get('href'))
        return urls, http_code


    @staticmethod
    def scraper_info(url):
        """Get all information of a game
        :param url: game link
        :return: class with all info
        http://www.planetajuegos.cl/pj_detalle_producto.php?producto=5546
        """
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        product = PlanetaJuegosInfo()

        name = html.cssselect('#contenidos > div > div.nombre_producto > h1')
        if name:
            name = name[0].text_content().strip()
            name = tools.clear_name(name)
            #product.name = name[:-1].strip()
            product.name = name

        platform = html.cssselect('div.ficha_info_separador')
        #print(tostring(platform[0]))
        if platform:
            platform_list = [i.text_content().strip() for i in platform ] # create list + text + strip
            platform_dict = {k:v for k,v in (i.split(':') for i in iter(platform_list)) } # create dict from list
            platform = platform_dict['Sistema']
            product.platform = tools.clear_platform(platform).upper()

        price = html.cssselect('div.precio_pro_2')
        if price:
            #print(price)
            price = price[0].text_content()
            if '$' in price:
                price = price.split('$')[1].replace('.', '').strip()
                product.price = price

        stock = html.cssselect('div.disponibilidad_stock')
        #print(tostring(stock[0]))
        if stock:
            stock = stock[0].text_content()
            if int(stock) > 0:
                product.stock = 'Disponible'
            else:
                product.stock = 'No Disponible'

        product.url = url
        product.image_url = PlanetaJuegos.get_image(url, html)
        return product, http_code


    @staticmethod
    def get_image(url, html):
        if html is None:
            http = tools.get_html(url)
            html = http[2]
           #http_code = http[1]
        image_url = html.cssselect('div.areaimagen > img')
        if image_url:
            image_url = image_url[0].get('src')

        if image_url == []:
            image_url = ''
        return image_url



### TEST #######
#PlanetaJuegos.scraper_links('http://www.planetajuegos.cl/catalogo.php?consola=PS4&categoria=T&display=listado&stock=T')
#PlanetaJuegos.scraper_info('http://www.planetajuegos.cl/pj_detalle_producto.php?producto=U5578')
#print(PlanetaJuegos.get_image('http://www.planetajuegos.cl/pj_detalle_producto.php?producto=5714'))
