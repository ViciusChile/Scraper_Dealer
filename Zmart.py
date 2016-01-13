# coding=utf-8
from Scrapers.tools import tools
from lxml.html import tostring


class ZmartInfo:
    """Model for each elements"""
    def __init__(self):
        self.name = None
        self.platform = None
        self.price = None
        self.stock = None
        self.url = None
        self.image_url = None


class Zmart:
    """Scrapping for www.zmart.cl"""

    def __init__(self):
        pass

    @staticmethod
    def scraper_dealer(url):
        """Get url index from one platform an letter
        :param url: to scraping
        http://www.zmart.cl/scripts/prodList.asp?idCategory=420
        """
        url_pages = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            pages = html.cssselect('#contenidos > div.paginador > form > select > option')
            if pages:
                for link in pages:
                    i = link.get('value')
                    if i:
                        url_pages.append('http://www.zmart.cl/scripts/{0}'.format(i))
        return url_pages, http_code

    @staticmethod
    def scraper_links(url):
        """Get all links
        :param url: page with many links
        :return: list of links urls
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            links = html.cssselect('#busqueda > div.caja_minihome > div.caja_secundaria > h3 > a')
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
        product = ZmartInfo()

        name = html.cssselect('#producto > h1 > a')
        if name:
            name = name[0].text_content().strip()
            product.name = tools.clear_name(name)

        #platform = page.cssselect('#imagen_producto > div:nth-child(4) > span.txValueInfoGral')
        platform = html.cssselect('#imagen_producto > div > span')
        if platform:
            platform_list = [i.text_content().strip() for i in platform ] # create list + text + strip
            platform_dict = {k:v for k,v in zip(*[iter(platform_list)]*2)} # create dict
            platform = platform_dict['Plataforma:']
            product.platform = tools.clear_platform(platform).upper()
        else:
            platform = html.cssselect('#imagen_producto > a:nth-child(4) > img')
            if platform:
                platform = platform[0].get('src')
            if not '.gif' in platform:
                platform = html.cssselect('#imagen_producto > a:nth-child(5) > img')
                if platform:
                    platform = platform[0].get('src')
                    if 'boton_PS4.gif' in platform:
                        platform = 'PS4'
                    elif 'boton_XBONE.gif' in platform:
                        platform = 'XONE'
                    #elif 'boton_XB360.gif' in platform:
                    #    platform = 'XBOX 360'
                    #elif 'boton_XBOX.gif' in platform:
                    #    platform = 'XBOX'
                    #elif 'boton_PSV.gif' in platform:
                    #    platform = 'PS Vita'
                    #elif 'boton_PS3.gif' in platform:
                    #    platform = 'PS3'
                    #elif 'boton_NDS.gif' in platform:
                    #    platform = 'DS'
                    #elif 'boton_3DS.gif' in platform:
                    #    platform = '3DS'
                    #elif 'boton_WiiU.gif' in platform:
                    #    platform = 'Wii U'
                    #elif 'boton_WIIU.gif' in platform:
                    #    platform = 'Wii U'
                    #elif 'boton_WII.gif' in platform:
                    #    platform = 'Wii'
                    #elif 'boton_PCMAC.gif' in platform:
                    #    platform = 'PC/MAC'
                    #elif 'boton_PC.gif' in platform:
                    #    platform = 'PC'
                    #elif 'boton_BLR.gif' in platform:
                    #    platform = 'BLU-RAY'
                    #elif 'boton_PSP.gif' in platform:
                    #    platform = 'PSP'
                    #elif 'boton_PSX.gif' in platform:
                    #    platform = 'PS1'
                    else:
                        platform = None
                    product.platform = platform

        #price = page.cssselect('#ficha_producto > table > form > tr > td > div > h2')
        price = html.cssselect('#PriceProduct')
        if price:
            product.price = price[0].text_content().split('$')[1].replace('.', '').strip()


        stock = html.cssselect('#ficha_producto > table > form > div > b')
        if stock:
            # disponible
            stock = stock[0].text_content()
            product.stock = stock.strip()
        else:
            # preventa
            stock = html.cssselect('#ficha_producto > table > form > tr > td > div')
            if stock:
                stock = stock[0].text_content().split()[0]
                product.stock = stock.strip()

        product.url = url
        product.image_url = Zmart.get_image(url, html)
        return product, http_code


    @staticmethod
    def get_image(url, html):
        if html is None:
            http = tools.get_html(url)
            html = http[2]
            #http_code = http[1]
            #image = data.find('div', id='imagen_producto').img['src']
        image_url = html.cssselect('#imagen_producto > img')
        if image_url:
            image_url = image_url[0].get('src')
        if image_url == []:
            image_url = ''
        return image_url

###-----------------------------------------------------------------------
#URL = 'http://www.zmart.cl/scripts/prodView.asp?idProduct=41364'
#URL2 = 'http://www.zmart.cl/scripts/prodView.asp?idProduct=43665'
#Zmart.scraper_info(URL2)

###-----------------------------------------------------------------------


    #


    #
    #
    #
    # URL = "http://www.zmart.cl/scripts/prodList.asp?idCategory="
    # urlGame = 'http://www.zmart.cl/scripts/prodView.asp?idProduct='
    # urlCategory = 'http://www.zmart.cl/scripts/prodList.asp?idCategory='
    # sleep = 0
    #
    # category_ids = {
    #     'X360': 159,
    #     'XONE': 421,
    #     'PS3': 187,
    #     'PS4': 420,
    #     'WIIU': 394,
    #     'WII': 183,
    #     'PSVita': 367,
    #     'DS': 180,
    #     'PC niños': 81,
    #     'PC Deportes': 65,
    #     'PC Rol/RPG': 64,
    #     'PC Accion/FPS': 63,
    #     '3DS': 334,
    #     'PC Estrategia/RTS': 62,
    #     'PC Ofertas 3000': 221,
    #     'PC Ofertas 5000': 222,
    #     'PC Ofertas 8000 ': 223,
    #     'PC Ofertas 10000': 224,
    #     'PC Ofertas 15000': 225,
    #     'PC Ofertas 20000': 226
    # }
    # ## NO CONSIDERAR --> 'PC LOL': 426 , 'PC Pre Venta': 92,
    #
    # def __init__(self):
    #     pass

    #
    # @staticmethod
    # def get_name(data, plataform):
    #     name = data.find('h1').a.string
    #     name = name.replace(plataform, '').strip()
    #     name = name.replace(u'en Español', '').strip()
    #     name = tools.clean(name)
    #     return name
    #
    # @staticmethod
    # def get_plataform(data):
    #     try:
    #         img = data.find('div', id='imagen_producto').a.img['src']
    #         if 'boton_PSV.gif' in img:
    #             plataform = 'PS Vita'
    #         elif 'boton_PS3.gif' in img:
    #             plataform = 'PS3'
    #         elif 'boton_PS4.gif' in img:
    #             plataform = 'PS4'
    #         elif 'boton_XB360.gif' in img:
    #             plataform = 'XBOX 360'
    #         elif 'boton_XBOX.gif' in img:
    #             plataform = 'XBOX'
    #         elif 'boton_XBONE.gif' in img:
    #             plataform = 'XBOX ONE'
    #         elif 'boton_NDS.gif' in img:
    #             plataform = 'DS'
    #         elif 'boton_3DS.gif' in img:
    #             plataform = '3DS'
    #         elif 'boton_WiiU.gif' in img:
    #             plataform = 'Wii U'
    #         elif 'boton_WIIU.gif' in img:
    #             plataform = 'Wii U'
    #         elif 'boton_WII.gif' in img:
    #             plataform = 'Wii'
    #         elif 'boton_PCMAC.gif' in img:
    #             plataform = 'PC/MAC'
    #         elif 'boton_PC.gif' in img:
    #             plataform = 'PC'
    #         elif 'boton_BLR.gif' in img:
    #             plataform = 'BLU-RAY'
    #         elif 'boton_PSP.gif' in img:
    #             plataform = 'PSP'
    #         elif 'boton_PSX.gif' in img:
    #             plataform = 'PS1'
    #         else:
    #             plataform = data.find('div', id='producto').h1['class'][0].upper()
    #             if plataform in "0":
    #                 plataform = data.find('div', id='producto').h1.a.string.split()[-1]
    #                 if 'ONE' == plataform:
    #                     plataform = 'XBOX ONE'
    #                 elif '360' == plataform:
    #                     plataform = 'XBOX 360'
    #                 elif 'U' == plataform:
    #                     plataform = 'Wii U'
    #                 elif 'Vita' == plataform:
    #                     plataform = 'PS Vita'
    #         plataform = tools.clean_plataform(plataform)
    #     except AttributeError:
    #         plataform = data.find('em').b.string
    #         if 'PC' in plataform:
    #             plataform = 'PC'
    #     return plataform
    #
    # @staticmethod
    # def get_price(data):
    #     try:
    #         price = data.find('div', id='ficha_producto').h2.string.split('$')[1].replace('.', '').strip()
    #     except (IndexError, AttributeError):
    #         price = None
    #     return price
    #
    # @staticmethod
    # def get_stock(data):
    #     """ PreVenta - Agotado - Disponible - Proximamente """
    #     stock = str(data.find('div', id='ficha_producto').b)
    #     if 'PRE VENTA' in stock:
    #         return 'PreVenta'
    #     elif 'PRODUCTO DISPONIBLE' in stock:
    #         return 'Disponible'
    #     elif 'PRODUCTO AGOTADO' in stock:
    #         return 'Agotado'
    #     elif 'PRÓXIMO LANZAMIENTO' in stock:
    #         return 'Proximamente'
    #     else:
    #         stock = ''
    #     return stock
    #
    # @staticmethod
    # def get_publisher(data):
    #     return ''
    #
    # @staticmethod
    # def get_developer(data):
    #     developer = ''
    #     text_box_imagen_producto = data.find('div', id='imagen_producto').get_text().split('\n')
    #     for line in text_box_imagen_producto:
    #         if 'Desarrollador' in line:
    #             developer = line.split(':')[1].strip()
    #     return developer
    #
    # @staticmethod
    # def get_esrb(data):
    #     try:
    #         esrb = data.find('div', class_='sticker3').img['src'].split('/')[-1]
    #         if esrb in ['RT1.gif', 'RT2.gif', 'RT3.gif', 'RT4.gif', 'RT5.gif']:
    #             return 'EC'
    #         elif esrb in ['RT6.gif', 'RT7.gif', 'RT8.gif', 'RT9.gif']:
    #             return 'E'
    #         elif esrb in ['RT10.gif', 'RT11.gif', 'RT12.gif']:
    #             return 'E10'
    #         elif esrb in ['RT13.gif', 'RT14.gif', 'RT15.gif', 'RT16.gif']:
    #             return 'T'
    #         elif esrb in 'RT17.gif':
    #             return 'M'
    #         elif esrb in 'RT18.gif':
    #             return 'AO'
    #         #elif esrb_image in '':
    #         #    return 'rp'
    #         else:
    #             return ''
    #     except AttributeError:
    #         return ''
    #
    # @staticmethod
    # def get_category(data):
    #     return ''
    #
    # @staticmethod
    # def get_released(data):
    #     return ''
    #
    # @staticmethod
    # def get_image(data):
    #     image = data.find('div', id='imagen_producto').img['src']
    #     if not '.' in image:
    #         image = data.find('div', id='imagen_producto').img['onerror'].split('\'')[1]
    #     return 'http://www.zmart.cl' + image
    #
    # ## MAIN
    # def scrap(self, url):
    #     product = {}
    #
    #     #start_time = dt.datetime.now()
    #     data = tools.get_minimal_data(self, url, 'producto')
    #     #print "data", time.time() - dt.datetime.now()
    #
    #     #start_time = time.time()
    #     plataform = self.get_plataform(data)
    #     #print "plataform", time.time() - start_time
    #
    #     #start_time = time.time()
    #     name = self.get_name(data, plataform)
    #     #print "name", time.time() - start_time
    #
    #     product['name'] = name
    #     product['url'] = url
    #     product['plataform'] = plataform
    #
    #     #start_time = time.time()
    #     product['price'] = self.get_price(data)
    #     #print "price", time.time() - start_time
    #
    #     #start_time = time.time()
    #     product['stock'] = self.get_stock(data)
    #     #print "stock", time.time() - start_time
    #
    #     #start_time = time.time()
    #     product['publisher'] = self.get_publisher(data)
    #     #print "publisher", time.time() - start_time
    #
    #     #start_time = time.time()
    #     product['developer'] = self.get_developer(data)
    #     #print "developer", time.time() - start_time
    #
    #     #start_time = time.time()
    #     product['esrb'] = self.get_esrb(data)
    #     product['category'] = self.get_category(data)
    #     product['released'] = self.get_released(data)
    #     product['dealer'] = self.dealer
    #     product['image'] = ''
    #
    #     image = self.get_image(data)
    #
    #     #start_time = time.time()
    #     image_local = tools.download_image_local(image, name, plataform, self.dealer)
    #     if image_local:
    #         tools.image_trim(image_local)
    #         tools.image_resize(image_local, plataform)
    #     #tools.push_image_to_s3(image_local)
    #     #print "plataform", time.time() - start_time
    #         product['image'] = image_local
    #     return product
    #
    # def run(self, url):
    #     product = self.scrap(url)
    #     exclude = ['BLU-RAY', 'PS1', 'PS2']
    #     if product['plataform'] in exclude:
    #         pass
    #     else:
    #         tools.save_db(product)
    #     return product
