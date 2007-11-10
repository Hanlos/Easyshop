# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# plone imports
from plone.app.content.container import Container
from plone.app.content.item import Item

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomer

from OFS.OrderSupport import OrderSupport

class Customer(OrderSupport, Container):
    """A customer can buy products from a shop. A customer has addresses and 
    payment methods.

    A customer exists additionally to the members of Plone.  Whenever a member 
    wants to buy something a customer content object is added for this member. 
    This is intended to be changed to remember in future.
    """    
    implements(ICustomer)
    portal_type = "Customer"
    
    firstname = FieldProperty(ICustomer["firstname"])
    lastname  = FieldProperty(ICustomer["lastname"])
    email     = FieldProperty(ICustomer["email"])

    selected_invoice_address  = u""
    selected_shipping_address = u""
    selected_payment_method   = u""
    selected_shipping_method  = u""
    
    def Title(self):
        """
        """
        if self.firstname and self.lastname:
            return self.firstname + " " + self.lastname
        else:
            return self.getId()
    
    def SearchableText(self):
        """
        """
        text = []
        
        text.append(self.firstname)
        text.append(self.lastname)
        text.append(self.email)
        
        am = IAddressManagement(self)
        for address in am.getAddresses():
            text.append(address.firstname)
            text.append(address.lastname)
            text.append(address.address_1)
            text.append(address.zip_code)            
            text.append(address.city)
            text.append(address.country)
                        
        return " ".join(text)