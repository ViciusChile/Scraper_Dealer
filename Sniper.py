from pprint import pprint
from Scrapers.tools import tools
from lxml.html import tostring

class SniperInfo:
    """Model for each elements"""
    def __init__(self):
        self.name = None
        self.platform = None
        self.price = None
        self.stock = None
        self.url = None
        self.image_url = None

class Sniper:
    """Scrapping for www.sniper.cl"""

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
        http://www.sniper.cl/index.php?id=VerTablaProductos&Cat=12&SubCat=36
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            links = html.cssselect('#pagina > table > tr > td > a')
            print(tostring(links[0]))
            if links:
                for l in links:
                    urls.append(l.get('href'))
        return urls, http_code


    @staticmethod
    def scraper_info(url):
        """Get all information of a game
        :param url: game link
        :return: class with all info
        http://www.sniper.cl/index.php?id=VerProducto&Item=2892
        """
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        product = Sniper()

        name = html.cssselect('#titulo')
        #print(tostring(name[0]))
        if name:
            name = name[0].text_content().strip()
            name = tools.clear_name(name)
            product.name = name

        platform = html.cssselect('#precio > strong:nth-child(14)')
        #print(tostring(platform[0]))
        if platform:
            platform = platform[0].text_content().strip()
            product.platform = tools.clear_platform(platform).upper()

        price = html.cssselect('#precio > strong:nth-child(2) > b > font')
        #print(tostring(price[0]))
        if price:
            price = price[0].text_content()
            if '$' in price:
                price = price.split('$')[1].replace('.', '').strip()
                product.price = price

        #stock = html.cssselect(None)
        #print(tostring(stock[0]))
        #if stock:
        #    stock = stock[0].text_content()
        #    if int(stock) > 0:
        #        product.stock = 'Disponible'
        #    else:
        #        product.stock = 'No Disponible'
        product.stock = 'Disponible'

        product.url = url
        product.image_url = Sniper.get_image(url, html)
        #print(vars(product))
        return product, http_code


    @staticmethod
    def get_image(url, html):
        if html is None:
            http = tools.get_html(url)
            html = http[2]
           #http_code = http[1]
        image_url = html.cssselect('#imgprov')
        if image_url:
            image_url = image_url[0].get('src')

        if image_url == []:
            image_url = ''
        return image_url



### TEST #######
#Sniper.scraper_dealer()
#Sniper.scraper_links('http://www.sniper.cl/index.php?id=VerTablaProductos&Cat=12&SubCat=36')
#Sniper.scraper_info('http://www.sniper.cl/index.php?id=VerProducto&Item=2892')
#PlanetaJuegos.scraper_info('http://www.planetajuegos.cl/pj_detalle_producto.php?producto=U5578')
#print(PlanetaJuegos.get_image('http://www.planetajuegos.cl/pj_detalle_producto.php?producto=5714'))
