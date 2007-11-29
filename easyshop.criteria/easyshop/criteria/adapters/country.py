# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICountryCriteria
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class CountryCriteriaValidity:
    """Adapter which provides IValidity for country criteria content
    objects.
    """    
    implements(IValidity)
    adapts(ICountryCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True if the selected country of the current customer has one
        of the selected countries.
        """
        shop            = IShopManagement(self.context).getShop()
        customer        = ICustomerManagement(shop).getAuthenticatedCustomer()
        invoice_address = IAddressManagement(customer).getInvoiceAddress()
        
        if invoice_address is not None:
            country = invoice_address.country
        else:
            country = customer.selected_country
            
        if country in self.context.getCountries():
            return True
        else:
            return False        