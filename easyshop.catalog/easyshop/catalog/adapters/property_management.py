# Zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes


class ProductPropertyManagement:
    """Provides IPropertyManagement for product content objects.
    """
    implements(IPropertyManagement)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context

    def getPriceForCustomer(self, property_id, option_name):
        """
        """
        # Get the tax rate for the product to which the property belongs.
        # Note: That means, the tax rate for the product's properties is the
        # same as for the product.
        tax_rate_for_customer = ITaxes(self.context).getTaxRateForCustomer()
        
        price_net = self.getPriceNet(property_id, option_name)
        price_for_customer =  price_net * ((tax_rate_for_customer + 100) / 100)

        return price_for_customer
        
    def getPriceGross(self, property_id, option_name):
        """
        """
        shop     = IShopManagement(self.context).getShop()
        tax_rate = ITaxes(self.context).getTaxRate()
        price    = self._calcPrice(property_id, option_name)


        # The price entered is considered as gross price, so we simply
        # return it.
        
        if shop.getGrossPrices() == True:
            return price

        # The price entered is considered as net price. So we have to calculate 
        # the gross price first.
        else:
            return price * ((tax_rate + 100) / 100)
        
    def getPriceNet(self, property_id, option_name):
        """
        """
        # Get the tax rate for the product to which the property belongs.
        # Note: That means, the tax rate for the product's properties is the
        # same as for the product.
        shop     = IShopManagement(self.context).getShop()
        tax_rate = ITaxes(self.context).getTaxRate()
        price    = self._calcPrice(property_id, option_name)


        # The price entered is considered as gross price. So we have to 
        # calculate the net price first.
        
        if shop.getGrossPrices() == True:
            return price * (100 / (tax_rate + 100))
            
        # The price entered is considered as net price, so we simply
        # return it.            
        else:
            return price
                
    def getProperties(self):
        """Returns all Properties for a Product.
                
           Properties from the Product have higher precedence than Properties
           from a Group.
        """
        groups = IGroupManagement(self.context).getGroups()

        # Get all Properties from Groups
        result = {}
        for group in groups:
            for property in group.objectValues("ProductProperty"):
                result[property.getId()] = property
        
        # Overwrite with Properties from Product
        for property in self.context.objectValues("ProductProperty"):
            result[property.getId()] = property
            
        return result.values()

    def getProperty(self, id):
        """
        """
        for property in self.getProperties():
            if property.getId() == id:
                return property
        
        return None
        
    def _calcPrice(self, property_id, option_name):
        """
        """
        found = False
        for property in self.getProperties():
            if property.getId() == property_id:
                found = True
                break

        if found == False:
            return 0.0
                    
        found = False
        for option in property.getOptions():
            if option["name"] == option_name:
                found = True
                break
                
        if found == False:
            return 0.0
                    
        try:
            price = float(option["price"])
        except ValueError:
            price = 0.0

        return price
        
