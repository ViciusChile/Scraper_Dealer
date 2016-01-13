# -*- coding: utf-8 -*-
from Scrapers.tools import tools
#import tools

class TodoJuegosInfo:
    """Model for each elements"""
    def __init__(self):
        self.name = None
        self.platform = None
        self.price = None
        self.stock = None
        self.url = None
        self.image_url = None


class TodoJuegos:
    """Scrapping for www.todojuegos.cl"""
    def __init__(self):
        pass

    @staticmethod
    def scraper_dealer(url):
        pass

    @staticmethod
    def scraper_links(url):
        """Get url index from ALL
        :param url: page
        :return: list of links urls
        http://www.todojuegos.cl/Productos/listadoProductosListaFull.asp?idFamiliaListadoProd=15&idCategoriaListadoProd=2
        idCategoriaListadoProd
        1 consolas
        2 juegos
        3 accesorios

        idFamiliaListadoProd
        02 DS
        03 PC
        05 PS3
        09 WII
        10 Xbox 360
        15 PSVITA
        16 3DS
        27 WII U
        28 PS4
        32 Xbox ONE
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            links = html.cssselect('table > tr > td > a')
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
        product = TodoJuegosInfo()

        name = html.cssselect('#content > div:nth-child(5) > h1')
        if name:
            name = name[0].text_content().strip()
            product.name = tools.clear_name(name)

        platform = url.split('/')[4]
        if platform:
            product.platform = tools.clear_platform(platform).upper()


        price = html.cssselect('#content > div.info > div:nth-child(1) > h2')
        if price:
            price = price[0].text_content()
            if '$' in price:
                price = price.split('$')[1].replace('.', '').strip()
                product.price = price

        stock = html.cssselect('#content > div.infoLeft > div.infoLeft_footer > div.etiqueta > img')
        if stock:
            stock = stock[0].get('src')
            if 'http://www.todojuegos.cl/images/eti_estreno.jpg' in stock:
                product.stock = 'Disponible'
            elif 'http://www.todojuegos.cl/images/eti_nuevo.jpg' in stock:
                product.stock = 'Disponible'
            elif 'http://www.todojuegos.cl/images/eti_reserva.jpg' in stock:
                product.stock = 'PreVenta'
            elif 'http://www.todojuegos.cl/images/eti_temporal_agotado.jpg' in stock:
                product.stock = 'Agotado'
            elif 'http://www.todojuegos.cl/images/eti_volvio.jpg' in stock:
                product.stock = 'Disponible'
            elif 'http://www.todojuegos.cl/images/eti_anunciado.jpg' in stock:
                product.stock = 'Proximamente'

        product.url = url
        product.image_url = TodoJuegos.get_image(url, html)
        #print(vars(product))
        return product, http_code


    @staticmethod
    def get_image(url, html):
        if html is None:
            http = tools.get_html(url)
            html = http[2]
            #http_code = http[1]
            #image = data.find('div', class_='foto_juego').img['src']
        image_url = html.cssselect('#ImgPrincipalGaleria')
        if image_url:
            image_url = image_url[0].get('style')
            if image_url:
                i = image_url.find('http')
                image_url = image_url[i:]
                if image_url:
                    image_url = image_url.split("'")[0]
            image_url = image_url.replace(' ','%20')
        if image_url == []:
            image_url = ''
        return image_url


###-----------------------------------------------------------------------
#URL="http://www.todojuegos.cl/Productos/PS4/Battlefield-4/"
#TodoJuegos.scraper_info(URL)
#URL='http://www.todojuegos.cl/Productos/listadoProductosListaFull.asp?idFamiliaListadoProd=28&idCategoriaListadoProd=2'
#TodoJuegos.scraper_links(URL)
###-----------------------------------------------------------------------

#http://www.todojuegos.cl/Productos/PS4/Battlefield-4/


#=====================================================================
# from bs4 import BeautifulSoup
# from urllib2 import urlopen, quote
# import Scraper.libs.tools
#
#
# class TodoJuegos:
#     """ Scrapping for www.todojuegos.cl """
#     dealer = 'TodoJuegos'
#     #URL = "http://www.todojuegos.cl/Productos/listadoProductosListaFull.asp?idFamiliaListadoProd=15&idCategoriaListadoProd=2" #TEST URL
#     URL = "http://www.todojuegos.cl/Productos/listadoProductosListaFull.asp"
#     sleep = 0
#
#     def __init__(self):
#         pass
#
#     def get_all_idurl(self):
#         ids = []
#         exclude = ["Productos/BLU", "Productos/SMA", "Productos/COL", "Productos/CAN", "Productos/DVD", "Productos/GUI", "Productos/HD",
#                    "Productos/KIN", "Productos/UNI", ]
#         soup = BeautifulSoup(urlopen(self.URL))
#         for product in soup.find_all('a'):
#             id_url = product.get('href').encode("utf-8")  #fix encoding problem
#             id_url = quote(id_url, safe="%/:=&?~#+!$,;'@()*[]")  #clear url
#             if tools.ignore_url(exclude, id_url):
#                 continue
#             ids.append(id_url)
#         return ids
#
#     @staticmethod
#     def get_name(data):
#         name = data.find('h1', class_='titulo_juego').string
#         name = tools.clean(name)
#         return name
#
#     @staticmethod
#     def get_plataform(idurl):
#         plataform = idurl.split('/')[4]
#         plataform = tools.clean_plataform(plataform)
#         return plataform
#
#     @staticmethod
#     def get_price(data):
#         try:
#             price = data.find('h2', class_='precio_juego').string.split('$')[1].replace('.', '').strip()
#         except (IndexError, ValueError):
#             price = None
#         return price
#
#     @staticmethod
#     def get_stock(data):
#         """ PreVenta - Agotado - Disponible - Proximamente """
#         stock = data.find('div', class_='etiqueta').img['src']
#
#         if 'http://www.todojuegos.cl/images/eti_estreno.jpg' in stock:
#             return 'Disponible'
#         elif 'http://www.todojuegos.cl/images/eti_nuevo.jpg' in stock:
#             return 'Disponible'
#         elif 'http://www.todojuegos.cl/images/eti_reserva.jpg' in stock:
#             return 'PreVenta'
#         elif 'http://www.todojuegos.cl/images/eti_temporal_agotado.jpg' in stock:
#             return 'Agotado'
#         elif 'http://www.todojuegos.cl/images/eti_volvio.jpg' in stock:
#             return 'Disponible'
#         elif 'http://www.todojuegos.cl/images/_.gif' in stock:
#             return u''
#         elif 'http://www.todojuegos.cl/images/eti_anunciado.jpg' in stock:
#             return 'Proximamente'
#         else:
#             return u''
#
#     @staticmethod
#     def get_publisher(data):
#         return ''
#
#     @staticmethod
#     def get_developer(data):
#         table = data.find('table', class_='infoDetalle')
#         try:
#             developer = tools.find_in_table(table, 'Fabricante')[2]
#         except (TypeError, IndexError):
#             developer = ''
#         return developer
#
#     @staticmethod
#     def get_esrb(data):
#         esrb = str(data.find('div', class_='calificacionESRB'))
#         if 'esrb_ratingsymbol_ec.gif' in esrb:
#             return 'EC'
#         elif 'esrb_ratingsymbol_e.gif' in esrb:
#             return 'E'
#         elif 'esrb_ratingsymbol_e10.gif' in esrb:
#             return 'E10'
#         elif 'esrb_ratingsymbol_t.gif' in esrb:
#             return 'T'
#         elif 'esrb_ratingsymbol_m.gif' in esrb:
#             return 'M'
#         elif 'esrb_ratingsymbol_ao.gif' in esrb:
#             return 'AO'
#         elif 'esrb_ratingsymbol_rp.gif' in esrb:
#             return 'RP'
#         else:
#             return ''
#
#     @staticmethod
#     def get_category(data):
#         return ''
#
#     @staticmethod
#     def get_released(data):
#         table = data.find('table', class_='infoDetalle')
#         released = tools.find_in_table(table, 'Fecha de Llegada')
#         return released
#
#     @staticmethod
#     def get_image(data):
#         image = data.find('div', class_='foto_juego').img['src']
#         return image
#
#     ## MAIN
#     def scrap(self, url):
#         product = {}
#         data = tools.get_minimal_data(self, url, 'content')
#         name = self.get_name(data)
#         plataform = self.get_plataform(url)
#
#         product['name'] = name
#         product['url'] = url
#         product['plataform'] = plataform
#         product['price'] = self.get_price(data)
#         product['stock'] = self.get_stock(data)
#         product['publisher'] = self.get_publisher(data)
#         product['developer'] = self.get_developer(data)
#         product['esrb'] = self.get_esrb(data)
#         product['category'] = self.get_category(data)
#         product['released'] = self.get_released(data)
#         product['dealer'] = self.dealer
#         product['image'] = ''
#
#         image = self.get_image(data)
#         image_local = tools.download_image_local(image, name, plataform, self.dealer)
#         if image_local:
#             tools.image_trim(image_local)
#             tools.image_resize(image_local, plataform)
#             #tools.push_image_to_s3(image_local)
#             product['image'] = image_local
#         return product
#
#     def run(self, url):
#         product = self.scrap(url)
#         exclude = ['BLU', 'PS1', 'PS2']
#         if product['plataform'] in exclude:
#             pass
#         else:
#             tools.save_db(product)
#         return product