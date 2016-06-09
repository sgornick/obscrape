import re
import json
import js2xml
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from yattag import indent, Doc
from obscrape.items import LVRItem


class LVRSpider(Spider):
    name = "lvr-crawler"
    allowed_domains = ["luisaviaroma.com"]

    def start_requests(self):
        # If need to set location cookie, it is:
        # Cookie-Name: LVR_UserData
        # Cookie-Data: cty=US&curr=USD&vcurr=USD&lang=EN&Ver=4
        designersRequest = \
            Request(
                "http://www.luisaviaroma.com/women/"
                "catalog/designers/lang_EN#DesignerSrv"
                "&listaDesID=&tipoQryDes=0", callback=self.parse_designers)

        return [designersRequest]

    def parse_designers(self, response):
        designers_div = response.xpath('//div[@id="lista_designers"]')
        designer_urls = designers_div.xpath('.//a/@href')
        for designer_url in designer_urls[0:9]:  # This is for education.  Just use the first 10 designers
            yield \
                Request(
                    designer_url.extract(),
                    callback=self.parse_designer)

    def parse_designer(self, response):
        # Grab the json array from javascript code.
        # Match on var event =.
        pattern = \
            re.compile(r".* event\s*=\s*({.*?});", re.MULTILINE | re.DOTALL)
        event = \
            response.xpath(
                '//script[contains(., "var event")]/text()').re(pattern)[0]
        json_data = json.loads(event)
        if 'productList' not in json_data:
            return

        for product in json_data['productList'][0:3]:  # This is for education.  Just use the first 3 products per designer.
            yield \
                Request(product['UrlProductEn'], callback=self.parse_product)

    def parse_product(self, response):
        doc, tag, text = Doc().tagtext()
        product_item = LVRItem()
        image_url_prefix = 'http://images.luisaviaroma.com/Big'
        # Grab the url from html metadata.
        # Even though we know the URL from the request, use the URL in the 
        # product page just in case it comes in different.
        product_item['url'] = \
            response.xpath(
                '/html/head/meta[@property="og:url"]/@content').extract_first()
        # Grab the first (main) image from html metadata.
        product_item['photos'] = [
            response.xpath(
                    '/html/head/meta[@property="og:image"]/@content'
                ).extract_first()]
        assert product_item['photos'][0].startswith(image_url_prefix)
        # Grab breadcrumb list from microdata kept in an ordered list.
        # These will be joined to make the category.
        breadcrumbs = \
            response.xpath(
                '//ol[@itemtype="http://schema.org/BreadcrumbList"]'
                '/li/a/span[@itemprop="name"]/text()').extract()
        # Grab the json from javascript.
        script = \
            response.xpath(
                '//script[contains(., "itemResponse")]/text()').extract_first()
        script_element = js2xml.parse(script)
        # Grab just the itemResponse assignment from the script.
        item_elements = \
            script_element.xpath(
                '//assign[left/identifier[@name="itemResponse"]]/right/*')
        item_dict = js2xml.jsonlike.make_dict(item_elements[0])
        assert item_dict['HasValidDefaultPrice']
        # Item title comes from the
        # (Designer->Description + ShortDescription) elements
        product_item['title'] = \
            u'{} - {}'.format(
                item_dict['Designer']['Description'],
                item_dict['ShortDescription'])
        desc_items = [u'ITEM CODE {}'.format(item_dict['ItemKey']['ItemCode'])]
        desc_items.extend(item_dict['LongtDescription'].strip('|').split('|'))
        if item_dict['Composition']:
            desc_items.append(
                u'Composition: {}'.format(item_dict['Composition']))
        with tag('ul'):
            for desc_item in desc_items:
                with tag('li'):
                    text(desc_item)
        product_item['description'] = doc.getvalue()
        product_item['currency_code'] = \
            item_dict['Pricing'][0]['Prices'][0]['CurrencyId']
        product_item['price'] = \
            item_dict['Pricing'][0]['Prices'][0]['FinalPrice']
        # Add as keywords the breadcrumb, sku, designer name, plus
        # each word in the product name, but total no more than 10
        # keywords.
        product_item['keywords'] = \
            breadcrumbs + [item_dict['Designer']['Description']] + \
            [item_dict['ItemKey']['ItemCode']] +\
            item_dict['ShortDescription'].split()[0:5]
        # Make a category from the breadcrumbs.
        # e.g., WOMEN-> SHOES-> SANDALS to a category:
        #  "WOMEN >> SHOES >> SANDALS"
        product_item['category'] = u' >> '.join(breadcrumbs)
        product_item['sku'] = item_dict['ItemKey']['ItemCode']
        for photo in item_dict['ItemPhotos']:
            photo_url = u''.join([image_url_prefix, photo['Path']])
            # Original photo duplicated in this list so ignore original.
            if photo_url not in product_item['photos']:
                product_item['photos'].append(photo_url)
        return product_item
