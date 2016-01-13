# -*- coding: utf-8 -*-
from Scrapers.tools import tools


class MicorplayInfo:
    """Model for each elements"""
    def __init__(self):
        self.name = None
        self.platform = None
        self.price = None
        self.stock = None
        self.url = None
        self.image_url = None


class Microplay:
    """Scrapping for www.microplay.cl"""

    def __init__(self):
        pass

    @staticmethod
    def scraper_dealer(url):
        """Get url index from one platform an letter
        :param url: to scraping
        http://www.microplay.cl/juegos/lista/playstation-4/
        """
        url_pages = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            pages = html.cssselect('#contenido > div.ficha > div.barra-filtros > div.paginar > div > span > a')
            if pages:
                max = len(pages)
                for i in range(1,max):
                    url_pages.append('{0}/page:{1}'.format(url,i))
        return url_pages, http_code


    @staticmethod
    def scraper_links(url):
        """
        :param url: page with many links
        :return: list of links urls
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            links = html.cssselect('#contenido > div.ficha > div.juegos-similares.lista > ul > li > h2 > a')
            if links:
                for l in links:
                    urls.append(l.get('href'))
        return urls, http_code


    @staticmethod
    def scraper_info(url):
        """Get all information of a game
        :param url: game link
        :return: class with all info
        """
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        product = MicorplayInfo()

        name = html.cssselect('#contenido > div.ficha > h1')
        if name:
            name = name[0].text_content().strip()
            product.name = tools.clear_name(name)

        platform = html.cssselect('#contenido > div.titulo-seccion.prod > h2')
        if platform:
            platform = platform[0].text_content()
            product.platform = tools.clear_platform(platform).upper()

        price = html.cssselect('#contenido > div.ficha > div.informacion > div > div.precios > strong')
        if price:
            product.price = price[0].text_content().split('$')[1].replace('.', '').strip()

        ## TODO: analizar como clasificar el stock de esta tienda
        #stock = page.cssselect('')
        product.stock = ''
        product.url = url
        product.image_url = Microplay.get_image(url, html)

        return product, http_code


    @staticmethod
    def get_image(url, html):
        """
        :param url:
        :return:
        """
        if html is None:
            http = tools.get_html(url)
            html = http[2]
            #http_code = http[1]
                 #image = data.find('div', id='imagen_producto').img['src']
        image_url = html.cssselect('#contenido > div.ficha > div.img-portada > img')
        if image_url:
            image_url = image_url[0].get('src')

        if image_url == []:
            image_url = ''
        return image_url

################################## TEST #######################################################
#Microplay.scraper_dealer('http://www.microplay.cl/juegos/lista/playstation-4/')
#Microplay.scraper_links('http://www.microplay.cl/juegos/lista/playstation-4//page:1')
#Microplay.scraper_info('http://www.microplay.cl/producto/the-witcher-3-wild-hunt-ps4/')
#Microplay.get_image('http://www.microplay.cl/producto/the-witcher-3-wild-hunt-ps4/')
##############################################################################################

#from urllib2 import urlopen
#from bs4 import BeautifulSoup
#from Scrapers.dealer import tools


# class Microplay:
#     """ Scrapping for www.microplay.cl """
#     dealer = 'Microplay'
#     URL = "http://www.microplay.cl/juegos/"
#     sleep = 0
#     category_ids = [
#         'playstation-4/',
#         #'xbox-one/',
#         #'playstation-3/',
#         #'xbox-360/',
#         #'ps-vita/',
#         #'psp/',
#         #'nintendo-wiiu/',
#         #'nintendo-wii/',
#         #'nintendo-3ds/',
#         #'nintendo-ds/',
#         #'pc/'
#         ]
#
#     def __init__(self):
#         pass
#
#     def get_all_idurl(self):
#         ids = []
#         for i in self.category_ids:
#             URL = self.URL + str(i) + 'page:1'
#             soup = BeautifulSoup(urlopen(URL))
#             data = soup.find('div', class_='ficha')
#             pages = data.find('div', class_='box_interior_pag').find_all('a')[-2].string
#             for page in range(1, int(pages) + 1):
#                 ## Cambia paginas
#                 url = self.URL + str(i) + 'page:' + str(page)
#                 soup = BeautifulSoup(urlopen(url))
#                 data = soup.find('div', class_='ficha')
#                 products = data.find_all('a', class_='fotos')
#                 for product in products:
#                     product_id = "http://www.microplay.cl" + product['href']
#                     if product_id not in ids:
#                         ids.append(product_id)
#         return ids
#
#
#
#     @staticmethod
#     def get_plataform(data):
#         #plataform = idurl.split('/')[4]
#         #plataform = tools.clean_plataform(plataform)
#         plataform = tools.table_ul_to_list(data, 'Consola')
#         #if plataform is '':
#             #plataform = data.find('h1').string.strip().split()[-1]
#         plataform = tools.clean_plataform(plataform)
#         return plataform
#
#
#     @staticmethod
#     def get_name(data):
#         name = data.find('h1').string
#         name = tools.clean(name)
#         return name
#
#
#     @staticmethod
#     def get_price(data):
#         try:
#             price = data.find('div', class_='precios').strong.string.split('$')[1].strip()
#         except IndexError:
#             price = ''
#         return price
#
#
#     @staticmethod
#     def get_price_normal(data):
#         try:
#             price = data.find('div', class_='precios').find('span', class_='oferta').s.split('$')[1].strip()
#             print price
#         except (IndexError, AttributeError):
#             price = ''
#         return price
#
#
#     @staticmethod
#     def get_stock(data):
#         """ PreVenta - Agotado - Disponible - Proximamente """
#         stock = tools.table_ul_to_list(data, 'Código')
#         if 'PV' in stock:
#             return 'PreVenta'
#
#         stock_box = data.find('div', class_='comprar')
#         if "Agregar al carro" in str(stock_box):
#             return 'Disponible'
#         elif 'Sin Stock en Web' in str(stock_box):
#             return 'Agotado'
#         elif 'Consulta por disponibilidad en tiendas' in str(stock_box):
#             return 'Disponible'
#         else:
#             return ''
#
#
#     @staticmethod
#     def get_publisher(data):
#         return ''
#
#     @staticmethod
#     def get_developer(data):
#         developer = tools.table_ul_to_list(data, 'Fabricante')
#         if developer:
#             return developer
#         else:
#             return ''
#
#     @staticmethod
#     def get_esrb(data):
#         esrb_box = data.find('div', class_='caracteristicas').a.img['src']
#         if 'edad_50.jpg' in esrb_box:
#             return 'EC'
#         elif 'edad_51.jpg' in esrb_box:
#             return 'E'
#         elif 'edad_52.jpg' in esrb_box:
#             return 'E10'
#         elif 'edad_53.jpg' in esrb_box:
#             return 'T'
#         elif 'edad_54.jpg' in esrb_box:
#             return 'M'
#         elif 'edad_55.jpg' in esrb_box:
#             return 'AO'
#         elif 'edad_56.jpg' in esrb_box:
#             return 'RP'
#         else:
#             return ''
#
#     @staticmethod
#     def get_released(data):
#         try:
#             released = data.find('small', class_='fecha-lan').strong.string
#             return released
#         except:
#             return ''
#
#     @staticmethod
#     def get_category(data):
#         category = tools.table_ul_to_list(data, 'Género')
#         return category
#
#
#
#     @staticmethod
#     def get_image(data):
#         image = data.find('div', class_='img-portada').img['src']
#         image = 'http://www.microplay.cl' + image
#         return image
#
# #----------------------------------------
#
#
#
#     ## MAIN
#     def scrap(self, url):
#         product = {}
#         data = tools.get_minimal_data_class(self, url, 'ficha')
#         plataform = self.get_plataform(data)
#         #if plataform == 'BLU-RAY':
#         #    pass
#         #else:
#         name = self.get_name(data)
#
#         product['name'] = name
#         product['url'] = url
#         product['plataform'] = plataform
#         product['price'] = self.get_price(data)
#         product['price_normal'] = self.get_price_normal(data)
#         product['stock'] = self.get_stock(data)
#         product['publisher'] = self.get_publisher(data)
#         product['developer'] = self.get_developer(data)
#         product['esrb'] = self.get_esrb(data)
#         product['category'] = self.get_category(data)
#         product['released'] = self.get_released(data)
#         product['dealer'] = self.dealer
#
#         image = self.get_image(data)
#         print image
#         image_local = tools.download_image_local(image, name, plataform, self.dealer)
#     #    tools.push_image_to_s3(image_local)
#         print product
#         return product
#
#
#
#
#
#
#
#
# #m = Microplay()
# #m.scrap("http://www.microplay.cl/producto/the-last-of-us-remastered/")
