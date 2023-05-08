
import scrapy
from itemloaders.processors import MapCompose as ILMapCompose, TakeFirst as ILTakeFirst
from w3lib.html import remove_tags
import re

##### add country #######
def get_country(value):
    if 'Jumia' in value:
        country = value.replace('Jumia', '').strip()
        return country

## title setting
def clean_title(title_value):
    title = title_value.strip()
    return title

### SKU settings
def clean_sku(sku_value):
    sku = sku_value.replace(': ', '')
    return sku

### Stars settings
def clean_stars(star_value):
    if star_value:
        star = str(star_value[0]).replace('out of 5', '')
        star = remove_tags(star)
        star = float(star)
        return star
    else :   
        return None

#### brand Settings
def add_brand(value_brand):
    if value_brand:
        brand = value_brand
        return brand
    else :
        return 'N/A'

#### category and  subcategory
def clean_category(value):
    if value :
        category = value.replace('/', '')
        return category
    
    
#### filter french and englis web site 
def clean_advice(advice_value):
    if "verified ratings" in advice_value or "verified rating" in advice_value or "avis vérifiés" in advice_value or "avis vérifié" in advice_value:
        advice = re.findall(r'\d+', advice_value)
        if advice:
            advice = int(advice[0])
            return advice
    elif "No ratings available" in advice_value or "Pas d'avis disponibles" in advice_value:
        advice = advice_value.replace("(", "").replace(")", "")
        return advice
    else:
        return 'N/A'

### refurbished status product
def clean_refurbished(refurbished_value):
    if refurbished_value:
        return 'True'
    else :
        return 'False'
    
## clean price from device appelation
def clean_price(price_value):
    currencies = ['KSh', '₦', 'UGX', 'Dhs', 'DA', 'TND', 'FCFA']  
    price = None
    if '-' in price_value:
        price_values = price_value.split('-')
        price = price_values[0].strip()
    else:
        price = price_value.strip()
    for currency in currencies:
        if currency in price:
            price = float(price.replace(currency, '').replace(',', ''))
            break
    return price

#### clean  french-senegalese product value
def clean_sen_price(value):
    if '-' in value :
        price = value.split('-')
        price = price[0].strip()
        price = price.replace('FCFA', '')
        price = price.replace(' ', '')
        price = float(price)
        return price
    elif value :
        price = value.replace('FCFA', '')
        price = price.replace(' ', '')
        price = float(price)
        return price
    else :
        return 'N/A'

## clean stock value
def clean_stock(value):
    if value:
        stock = value.strip()
        return stock
    else:
        return 'N/A'
    
    

####### convert to price value to dollars with exchange rate ######

### Senegalese price to dollar
def convert_sen_dollard(value):
    exchange_rate = 0.00170909
    if value :
        price = clean_sen_price(value)
        dollar_price = price * exchange_rate
        return round(dollar_price, 2)
    else:
        return 'N/A'
        
# prices to dollar
def convert_to_dollars(value):
    if value:
        price = clean_price(value)
        if 'KSh' in value:
            exchange_rate = 0.00732726
            dollar_price = price * exchange_rate
            return round(dollar_price, 2)
        elif '₦' in value:
            exchange_rate = 0.00217233
            dollar_price = price * exchange_rate
            return round(dollar_price, 2)
        elif 'UGX' in value:
            exchange_rate = 0.000268904
            dollar_price = price * exchange_rate
            return round(dollar_price, 2)
        elif 'Dhs' in value:
            exchange_rate = 0.100086
            dollar_price = price  * exchange_rate
            return round(dollar_price, 2)
        elif 'DA' in value:
            exchange_rate = 0.00735692
            dollar_price = price * exchange_rate
            return round(dollar_price, 2)
        elif 'TND' in value:
            exchange_rate = 0.328407
            dollar_price = price * exchange_rate
            return round(dollar_price, 2)
        elif 'CFA' in value:
            exchange_rate = 0.00170909
            dollar_price = price * exchange_rate
            return round(dollar_price, 2)
        else :
            'N/A'
    return 'N/A'
        

### add device name precision
def clean_device(device_value):
    if 'KSh' in device_value:
        return 'Kenyan Shilling'
    elif '₦' in device_value:
        return 'Naira'
    elif 'UGX' in device_value:
        return 'Uganda Shilling'
    elif 'Dhs' in device_value:
        return 'Moroccan dirham'
    elif 'DA' in device_value:
        return 'Algerian dinar'
    elif 'TND' in device_value:
        return 'Tunisian dinar'
    elif 'FCFA' in device_value:
        return 'Cfa Francs'
    else :
        return 'N/A'

### ADD currency sigle precision   
def clean_currency(currency_value):
    if 'KSh' in currency_value:
        return 'KSh'
    elif '₦' in currency_value:
        return '₦'
    elif 'UGX' in currency_value:
        return 'UGX'
    elif 'Dhs' in currency_value:
        return 'Dhs'
    elif  'DA' in currency_value:
        return 'DA'
    elif 'TND' in currency_value:
        return 'TND'
    elif 'FCFA' in currency_value:
        return 'CFA'
    else :
        return 'N/A'


###### discount status #####
# add precision to discount status
def add_discount(discount_value):
    if discount_value:
        return 'True'
    else:
        return 'False'

# add discount rate
def clean_discountrate(discountrate_value):
    if discountrate_value:
        discountrate = discountrate_value
        discountrate = discountrate[0]
        return discountrate
    else:
        return '0%'
   
####### Flash Sales status #####


def is_flashsales(value):
    if value:
        return 'True'
    else :
        return 'False'

def flash_remaintime(value):
    if value :
        flash_remain_time = value
    else : 
        flash_remain_time = 'N/A'
    return flash_remain_time

def remain_items(value):
    if value:
        items = value
        return items
    else :
        return '0'


##### seller informations ######
def get_seller(value):
    if value :
        seller = value
        return seller
    else:
        return 'N/A'

def get_sellerfollowers(value):
    if value :
        seller_follower = value
        seller_follower = seller_follower[0].strip()
        seller_follower = str(seller_follower)
        return seller_follower
    else:
        return 'no follower'
    
def get_sellerOrderRate(value):
    if value :
        sellerorder_rate = value
        return sellerorder_rate
    else:
        return 'N/A'
def get_sellerscore(value):
    if value:
        sellerscore = value
        return sellerscore
    else:
        return 'N/A'

## Breadcumbs list #####
def get_breadlist(value):
    breadcumbs = list(value)
    if len(breadcumbs) > 0:
        breadcumbs.pop(0)
    return breadcumbs


## Get product descriptiion ######
def clean_description(value):
    description = re.sub(r'[\n\r\t\xa0\\]', ' ', value)
    description = re.sub(r'\s+', ' ', description)
    return description

class JumiaInterItem(scrapy.Item):
    
    siteName = scrapy.Field(
        input_processor = ILMapCompose(),
        output_processor = ILTakeFirst()
        )
    country = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, get_country),
        output_processor = ILTakeFirst()  
    )
    ### spider mapcompose
    language = scrapy.Field(
        input_processor = ILMapCompose(),
        output_processor = ILTakeFirst()
    )
    title = scrapy.Field(
        input_processor = ILMapCompose(clean_title, remove_tags),
        output_processor = ILTakeFirst()   
    )
    ### spider mapcompose
    url = scrapy.Field(
        input_processor = ILMapCompose(),
        output_processor = ILTakeFirst()
    )
    category = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_category),
        output_processor = ILTakeFirst() 
    )
    subCategory = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_category),
        output_processor = ILTakeFirst()    
    )
    SKU = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_sku),
        output_processor = ILTakeFirst()
    )
    ### spider mapcompose
    brand = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst()
        
    )
    stars = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_stars),
        output_processor = ILTakeFirst()
    )
    ratings = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_advice),
        output_processor = ILTakeFirst()
    )
    refurbished = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_refurbished),
        output_processor = ILTakeFirst()
    )
    currentPrice_value = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_price),
        output_processor = ILTakeFirst()
     )
    # Item only availale for Jumia Senegal 
    CurrentPrice_value = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_sen_price),
        output_processor = ILTakeFirst()  
    )
    originalPrice_value = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_price),
        output_processor = ILTakeFirst() 
    )
    # Item only availale for Jumia Senegal 
    OriginalPrice_value = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_sen_price),
        output_processor = ILTakeFirst()  
    )
    ### spider mapcompose
    stock = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst(),
        #serializer=clean_stock   
    )
    
    priceUSD = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, convert_to_dollars),
        output_processor = ILTakeFirst()   
    )
    # Item only availale for Jumia Senegal 
    PriceUSD = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, convert_sen_dollard),
        output_processor = ILTakeFirst()   
    )
    originalPriceUSD = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, convert_to_dollars),
        output_processor = ILTakeFirst()   
    )
    # Item only availale for Jumia Senegal 
    OriginalPriceUSD = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, convert_sen_dollard),
        output_processor = ILTakeFirst()   
    )
    device = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_device),
        output_processor = ILTakeFirst()
    )
    currency = scrapy.Field(
      input_processor = ILMapCompose(remove_tags, clean_currency),
      output_processor = ILTakeFirst()  
    )
    isDiscount = scrapy.Field(
      input_processor = ILMapCompose(remove_tags),
      output_processor = ILTakeFirst()  
    ) 
    discountRate = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst()
     
    )
     ### spider mapcompose
    isFlashsales = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst()  
    )
    ### spider mapcompose
    Flashtime = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, flash_remaintime ),
        output_processor = ILTakeFirst() 
    )
    FlashRemainItems = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, remain_items),
        output_processor = ILTakeFirst()   
    )
    ### spider mapcompose
    seller = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst()     
    )
    sellerScore = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst()
        
    )
    ### spider mapcompose
    sellerFollowers = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst() 
    )
    # ### spider mapcompose
    sellerOrderFulfillmentRate = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst()   
    )
    ### spider mapcompose
    sellerQualityScore = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst()  
    )
    ### spider mapcompose
    sellerCustomerRating = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst()   
    )
    picture = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        output_processor = ILTakeFirst()   
    )
    ### spider mapcompose
    breadcumbs = scrapy.Field(
        input_processor = ILMapCompose(remove_tags),
        
    )
    description = scrapy.Field(
        input_processor = ILMapCompose(remove_tags, clean_description),
        output_processor = ILTakeFirst() 
        
    )