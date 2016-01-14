from Scrapers.tools import tools
from lxml.html import tostring

class FalabellaInfo:
    """Model for each elements"""
    def __init__(self):
        self.name = None
        self.platform = None
        self.price = None
        self.stock = None
        self.url = None
        self.image_url = None


class Falabella:
    """Scrapping for www.falabella.cl"""
    def __init__(self):
        pass

    @staticmethod
    def scraper_dealer(url):
        """Get all url index from one platform
        :param url: to scraping
        http://www.falabella.com/falabella-cl/category/cat2660025/Juegos-PS4
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            max_products = html.cssselect('#verProductos')
            #print(tostring(max_products[0]))
            if max_products:
                max_products = max_products[0].text_content().strip()
                if max_products:
                    max_products = max_products.split()[-2]
                    # http://www.falabella.com/falabella-cl/category/cat2660025/Juegos-PS4?No=0&Nrpp=91
                    url_max_prod = '{0}?No=0&Nrpp={1}'.format(url, max_products)
                    urls.append(url_max_prod)
        return urls, http_code


    @staticmethod
    def scraper_links(url):
        """Get url index for ALL product by platform
        :param url: page
        :return: list of links urls
        http://www.falabella.com/falabella-cl/category/cat2660025/Juegos-PS4?No=0&Nrpp=91
        """
        urls = []
        http = tools.get_html(url)
        html = http[2]
        http_code = http[1]
        if html is not None:
            links = html.cssselect('div.cajaLP4x')
            if links:
                for l in links:
                    l = l.cssselect('div.detalle > a')
                    l = l[0].get('href')
                    urls.append(l.replace('?navAction=push','/'))
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
        product = Falabella()

        name = html.cssselect('#productDecription')
        if name:
            name = name[0].text_content().strip()
            name = tools.clear_name(name)
            product.name = name
        else:
            product.name = ''
            http_code = '500'

        platform = url.split('-')[-1].replace('/','')
        product.platform = tools.clear_platform(platform)

        price = html.cssselect('#skuPrice > div.precio1 > span.unitPriceD') #precio Internet
        #price = html.cssselect('#skuPrice > div.precio2 > span.unitPriceD') #precio normal
        if price:
            price = price[0].text_content()
            price = price.replace('.', '').strip()
            product.price = price
        else:
            product.price = None
            product.stock = 'Sin stock'

        # stock = html.cssselect('')
        # if stock:
        #     # disponible
        #     stock = stock[0].text_content()
        #     product.stock = stock.strip()
        #product.stock = ''
        product.url = url
        product.image_url = Falabella.get_image(url, html)
        print(vars(product))
        #TODO: mish
        #print(html.cssselect('#jsonArray')[0].text_content().strip())
        return product, http_code


    @staticmethod
    def get_image(url, html):
        if html is None:
            http = tools.get_html(url)
            html = http[2]
            #http_code = http[1]
        image_url = ''
        sku = html.cssselect('#skuIdPicker > span')
        if sku:
            sku = sku[0].text_content()
            image_url = 'http://falabella.scene7.com/is/image/Falabella/{0}/'.format(sku)
        return image_url

###################################################









#############################################################################################################
# from tienda import ScrapingGeneral
# import datetime
# from urllib.request import urlopen
# import urllib.parse
# import time
#
# class Falabella(ScrapingGeneral):
#     dealer = 'Falabella'
#     dealerid = '4'
#     urlGame = 'http://www.falabella.com/falabella-cl/product/'
#     urlCategory = 'http://www.falabella.com/falabella-cl/category/'
#     sleep = 0
#
#     def GetGame_table_datajuegos(self, data, findName):
#         infoDetalle_box_li = data.find('div', id='contenidoDescripcionPP').find_all('li')
#
#         for li in infoDetalle_box_li:
#             if findName.upper() in str(li).upper():
#                 findName = findName.upper()
#                 try:
#                     output = li.string.upper().split(':')[1].strip()
#                 except:
#                     try:
#                         output = li.string.upper().split(findName)[1].strip()
#                     except:
#                         output = ''
#                 return (output)
#         return ''
#
#     def GetGame_plataform(self, dataBody):
#         dataContenedor = dataBody.find('div', id='contenedorPrincipal')
#         plataform = dataContenedor.find('div', class_='detalle').find('div', class_='marca').string.strip()
#         plataform = self.normalicePlataform(plataform)
#         #print(plataform)
#         ruta = dataBody.find('div', id='ruta')
#         indoDetalle_box = dataContenedor.find('div', id='contenidoDescripcionPP')
#         if 'NINTENDO' == plataform.upper() and 'WII U' in str(indoDetalle_box).upper():
#             plataform = 'WIIU'
#             #print("00:"+plataform)
#         if 'NINTENDO' == plataform.upper() and 'NINTENDO DS' in str(indoDetalle_box).upper():
#             plataform = 'DS'
#             #print("01:"+plataform)
#         if 'NINTENDO' == plataform.upper() and 'WII' in str(indoDetalle_box).upper():
#             plataform = 'WII'
#             #print("02:"+plataform)
#         if plataform not in ['PS4','PS3','PS2','PS VITA','PSP','WIIU','WII','3DS','DS','GC','PC','XBOX 360','XBOX ONE']:
#             plataform = self.GetGame_table_datajuegos(dataContenedor, 'Plataforma')
#             if plataform == '':
#                 plataform = self.GetGame_table_datajuegos(dataContenedor, 'Consola')
#                 if plataform == 'PLAYSTATION DE 250GB' and 'PS VITA' in str(ruta).upper():
#                     plataform = 'PS VITA'
#                 if plataform == 'DE PS3 UTILIZANDO UN CABLE USB' and 'SONY' in str(ruta).upper():
#                     plataform = 'PS3'
#                 if plataform == 'LIBRES DE CABLES' and 'SONY' in str(ruta).upper():
#                     plataform = 'PS3'
#                 #print("no-2:"+plataform)
#             plataform = self.normalicePlataform(plataform)
#             #print("no:"+plataform)
#         if plataform.upper() == 'XBOX': plataform = 'XBOX 360'
#         if 'XBOX' in plataform.upper() and 'PS3' in str(ruta).upper():
#             plataform = ruta.find_all('a')[-2].string.replace('Juegos','').strip()
#             plataform = self.normalicePlataform(plataform)
#             #print("1:"+plataform)
#         if 'WIIU' in plataform.upper() and 'PS3' in str(ruta).upper():
#             plataform = ruta.find_all('a')[-2].string.replace('Juegos','').strip()
#             plataform = self.normalicePlataform(plataform)
#             #print("2:"+plataform)
#         if plataform == 'PS3' and 'XBOX' in str(ruta).upper():
#             plataform = ruta.find_all('a')[-2].string.replace('Juegos','').strip()
#             plataform = self.normalicePlataform(plataform)
#             #print("3:"+plataform)
#         if plataform == '':
#             if 'PS3' in str(ruta).upper():
#                 plataform = 'PS3'
#                 #print("4:"+plataform)
#             if 'DUALSHOCK 3' in str(indoDetalle_box).upper():
#                 plataform = 'PS3'
#                 #print("5:"+plataform)
#             if 'DUALSHOCK 4' in str(indoDetalle_box).upper():
#                 plataform = 'PS4'
#                 #print("6:"+plataform)
#             if 'PLAYSTATION VITA' in str(indoDetalle_box).upper():
#                 plataform = 'PS VITA'
#                 #print("7:"+plataform)
#             if 'CONTROL PS3' in str(indoDetalle_box).upper():
#                 plataform = 'PS3'
#                 #print("8:"+plataform)
#             if 'PLAY STATION 3' in str(indoDetalle_box).upper():
#                 plataform = 'PS3'
#                 #print("9:"+plataform)
#             if 'PSP' in str(indoDetalle_box).upper():
#                 plataform = 'PSP'
#                 #print("10:"+plataform)
#             if 'PLAYSTATION MOVE' in str(indoDetalle_box).upper():
#                 plataform = 'PS3'
#                 #print("11:"+plataform)
#             if 'PS VITA' in str(indoDetalle_box).upper():
#                 plataform = 'PS VITA'
#                 #print("12:"+plataform)
#             if  'PSVITA' in str(indoDetalle_box).upper():
#                 plataform = 'PS VITA'
#                 #print("13:"+plataform)
#             if  'XBOX 360' in str(indoDetalle_box).upper():
#                 plataform = 'XBOX 360'
#                 #print("14:"+plataform)
#             if '22J-00001' in str(indoDetalle_box).upper():
#                 plataform = 'XBOX 360'
#                 #print("15:"+plataform)
#             if 'NINTENDO 3DS' in str(indoDetalle_box).upper():
#                 plataform = '3DS'
#                 #print("15:"+plataform)
#         if plataform not in ['PS4','PS3','PS2','PS VITA','PSP','WIIU','WII','3DS','DS','GC','PC','XBOX 360','XBOX ONE','']:
#             if 'WII' in plataform:
#                 plataform = 'WII'
#             if '3DS' in plataform:
#                 plataform = '3DS'
#         return plataform
#
#     def GetGame_name(self, plataform, data):
#         name = data.find('div', class_='detalle').find('span', id='productDecription').string.strip()
#         return name
#
#     def GetGame_price(self, data):
#         dataPrecios = data.find('div', id='skuPrice')
#         precio1 = dataPrecios.find('div', class_='precio1').get_text(strip=True)
#         precio2 = dataPrecios.find('div', class_='precio2').get_text(strip=True)
#         precio3 = dataPrecios.find('div', class_='precio3').get_text(strip=True)
#
#         if dataPrecios.find('div',class_='opUnica'):
#             #print("Precio Tarjeta CMR: " + precio1.split('$')[-1])
#             #print("Precio Normal: " + precio2.split('$')[-1])
#             return 'tarjeta=' + precio1.split('$')[-1] + ', normal=' + precio2.split('$')[-1]
#         else:
#             if 'Internet' in precio1 and 'Normal' in precio2:
#                 #print ("Precio Internet: " + precio1.split('$')[-1])
#                 #print ("Precio Normal: " + precio2.split('$')[-1])
#                 return 'web=' + precio1.split('$')[-1] + ', normal=' + precio2.split('$')[-1]
#             elif 'Internet' in precio1:
#                 return 'web=' + precio1.split('$')[-1]
#         return '-1'
#
#     def GetGame_imageUrl(self, idGame):
#         imageUrl = 'http://falabella.scene7.com/is/image/Falabella/' + str(idGame) + '_1?$producto308$&iv=avCnJ2&wid=924&hei=924&fit=fit,1'
#         return imageUrl
#
#     def GetGame_category(self, data):
#         category = self.GetGame_table_datajuegos(data, 'Género:')
#         return category
#
# ## Principal Info
#     def GetGame_dictionary(self, idGame):
#         urlGame = self.urlGame + urllib.parse.quote(idGame) + '/' ## urllib.parse.quote, para -> utf-8
#         DataBody = self.GetPrincipalBox_body(urlGame)
#         try:
#             Data = DataBody.find('div', id='contenedorPrincipal')
#         except:
#             return ''
#         if Data:
#             plataform = self.GetGame_plataform(DataBody)
#             dateEntry = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#             name = self.GetGame_name(plataform,Data)
#             price = self.GetGame_price(Data)
#             imageUrl = self.GetGame_imageUrl(idGame)
#             image = self.GetGame_image(imageUrl, self.dealer, self.normalicePlataform(plataform), name)
#             category = self.GetGame_category(Data)
#
#             var = {
#                     'id' : str(idGame),
#                     'plataform' : self.normalicePlataform(plataform),
#                     'name' : str(name),
#                     'price' : str(price),
#                     'imageUrl' : str(imageUrl),
#                     'dealer' : str(self.dealer),
#                     'urlGame' : str(urlGame),
#                     'updated_at' : str(dateEntry),
#                     'stock' : 'Sin Información',
#                     'released' : '',
#                     'developer' : '',
#                     'publisher' : '',
#                     'category': str(category),
#                     'esrb': '',
#                     'image': str(image),
#                     }
#             return var
#
# ## Category
#     def GetConsole_ids(self, idCategory):
#         print("Category: "+str(idCategory))
#         url = self.urlCategory + str(idCategory) + '/'
#         data = self.GetPrincipalBox_id(url, 'contenedorPrincipal')
#         gamesCategory = []
#
#         total_games = data.find('div', id='paginador')
#
#         if total_games:
#             total_games = total_games.find_all('a')[-1].string
#         else:
#             total_games = 1
#         pages = int(total_games)
#
#         for page in range(1, pages + 1):
#             print ("Pagina " + str(page) + " de " + str(pages))
#             ## Cambia paginas
#             if page != 1:
#                 url = "http://www.falabella.com/falabella-cl/browse/productList.jsp?_dyncharset=iso-8859-1&goToPage=" + str(page) + "&pageSize=16&priceFlag=&categoryId="+ str(idCategory) +"&docSort=numprop&docSortProp=bestSeller&docSortOrder=descending&onlineStoreFilter=online&userSelectedFormat=4*4&trail=SRCH%3A" + str(idCategory) + "&navAction=jump&searchCategory=true&question=" + str(idCategory) + "&searchColorGroupFacet=false&qfh_s_s=submit&_D%3Aqfh_s_s=+&qfh_ft=SRCH%3A" + str(idCategory) + "&_D%3Aqfh_ft=+&_DARGS=%2Ffalabella-cl%2Fbrowse%2FfacetsFunctions.jsp.searchFacetsForm"
#                 data = self.GetPrincipalBox_id(url, 'contenedorPrincipal')
#             items = data.find_all('div', class_='cajaLP4x')
#             ## Guarda ID
#             for item in items:
#                 game_id = str(item.find('div', class_='quickView').a['href'].split('/')[3])
#                 if game_id not in self.gamesIds:
#                     self.gamesIds.append(game_id)
#                 if game_id not in gamesCategory:
#                     gamesCategory.append(game_id)
#         print("Category: "+str(idCategory)+", Items Category: "+str(len(gamesCategory))+", Items Total: "+str(len(self.gamesIds)))
#         return gamesCategory
#
# ## All Product id
#     def GetAllGames_id(self):
#         datetime_now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')
#
#         ## PS3 Juegos: cat4106
#         self.GetConsole_ids('cat4106')
#         ## PS3 Consola: cat4126
#         self.GetConsole_ids('cat4126')
#         ## PS4 Consola: cat2450241
#         self.GetConsole_ids('cat2450241')
#         ## PS4 Juegos: cat2660025
#         self.GetConsole_ids('cat2660025')
#         ## Play Station Portables: cat4132
#         self.GetConsole_ids('cat4132')
#         ## PS VITA Consola:
#         self.GetConsole_ids('cat770042')
#         ## PS VITA Juegos:
#         self.GetConsole_ids('cat840022')
#         ## PSP juegos: cat4114
#         self.GetConsole_ids('cat4114')
#         # PS2 Juegos:
#         self.GetConsole_ids('cat4001')
#         # Sony accesorio:
#         self.GetConsole_ids('cat4120')
#
#         ## XBOX 360 Consola : cat4102
#         self.GetConsole_ids('cat4102')
#         ## XBOX 360 Juegos: cat4035
#         self.GetConsole_ids('cat4035')
#         ## XBOX 360 Accesorios: cat4007
#         self.GetConsole_ids('cat4007')
#
#         ## WII Consolas: cat4006
#         self.GetConsole_ids('cat4006')
#         ## 3DS consolas:cat4103
#         self.GetConsole_ids('cat4103')
#         ## Juegos Portables : cat4111
#         self.GetConsole_ids('cat4111')
#         ## WII U Consola: cat1440012
#         self.GetConsole_ids('cat1440012')
#         ## WII: cat4117
#         self.GetConsole_ids('cat4117')
#         ## WII U: cat1440014
#         self.GetConsole_ids('cat1440014')
#         ## 3DS: cat4127
#         self.GetConsole_ids('cat4127')
#         ## DS: cat4133
#         self.GetConsole_ids('cat4133')
#         ## Nintendo Accesorios: cat4136
#         self.GetConsole_ids('cat4136')
#
#         ## Juegos: cat720179
#         #self.GetConsole_ids('cat720179')
#
#         self.gamesIds = sorted(self.gamesIds, key=str.lower) ## ordenar los ID
#         ### Guardar los datos como archivo JSON
#         #self.Diccionary_to_JSONfile(self.gamesIds, str.lower(self.dealer).replace(' ','-') + '_category_' + datetime_now + '.json')
#         return self.gamesIds
#AllGames_Data = falabella.GetAllGames_Data(arg1)
#############################################################################################################
