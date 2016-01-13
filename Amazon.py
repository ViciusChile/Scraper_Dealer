import requests
from lxml.html import tostring


from Scrapers.tools.tools import get_html


class Amazon:
    """Scrapping for www.amazon.com"""
    def __init__(self):
         pass

    @staticmethod
    def get_image(url, html):
        """Get all information of a game
        :param url: of image
        :return: url storage
        """
        html = get_html(url)[2]
        image_amazon_url = ''

        # TRY: #main-image > get('rel') > request
        image_url = html.cssselect('#main-image')
        #print('image_url:',image_url)
        if image_url:
            #print(lxml.html.tostring(image_url[0]))
            image_url_rel = image_url[0].get('rel')
            #print('image_url_rel:',image_url_rel)
            if image_url_rel: ## en algunos casos no existe rel, investigar si funciona con data:image:base64
                #http://www.amazon.com/3D-Dot-Game-Heroes-Playstation-3/dp/B002I0J45C%3FSubscriptionId%3DAKIAJHSMUOWEQCQ7QDAQ%26tag%3Dmetacritic-games-20%26linkCode%3Dxm2%26camp%3D2025%26creative%3D165953%26creativeASIN%3DB002I0J45C
                result = requests.get(image_url_rel)
                #print('result:',result)
                if result.status_code == 200:
                    #print('file_name:',file_name)
                    #print('image_url:',image_url_rel)
                    image_amazon_url = image_url_rel

        ## TRY: #main-image-container > ul > li.image > image  get('data-old-hires')
        if not image_amazon_url:
            image_url = html.cssselect('#main-image-container > ul > li.image ')
            #print('image2:',image_url)
            if image_url:
                img = image_url[0].cssselect('img')
                #print('img:',img)
                if img:
                    image_data_old_hires = img[0].get('data-old-hires')
                    image_amazon_url = image_data_old_hires
                if not image_amazon_url:
                    image_data_dynamic_image = img[0].get('data-a-dynamic-image')
                    if image_data_dynamic_image:
                        image_amazon_url = image_data_dynamic_image.split('"')[1]
        return image_amazon_url



