from AccessControl import Unauthorized

# zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.component import queryUtility

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IType

class IOrderView(Interface):
    """View for order content objects.
    """
    def getCreationDate():
        """Returns the creation date.
        """
        
    def getCustomerFullname():
        """Returns the customer name.        
        It is taken from the invoice address of the order.
        """

    def getEmail():
        """Returns email of the order's customer.
        """
        
    def getItems():
        """Returns the items.
        """

    def getPaymentValues():
        """Returns prices and taxes for selectec payment method.
        """    
        
    def getPaymentMethod():
        """Returns the payment method of the current customer.
        """
        
    def getPaymentMethodType():
        """Returns the type of the payment method.
        """

    def getPriceForCustomer():
        """Returns the total price for the customer.
        """

    def getInvoiceAddress():
        """Returns the invoice address.
        """    
    
    def getShippingAddress():
        """Returns the shipping address.
        """    

    def getShipping():
        """Returns the shipping prices as dict.
        """

    def getState():
        """Returns the workflow state of the order.
        """

    def isRedoPaymentAllowed():
        """Returns True if the redo of a payment is allowed.
        """
            
    def redoPayment():
        """Does the payment process again.

        This is used for payment with paypal, at the moment, when the customer
        knows that something has gone wrong (broken connection, etc.) for the 
        first time.
        """    
        
class OrderView(BrowserView):
    """
    """
    implements(IOrderView)

    def getCreationDate(self):
        """
        """
        date = self.context.created()        
        
        tool = getToolByName(self.context, 'translation_service')
        return tool.ulocalized_time(date, long_format=True)
                
    def getCustomerFullname(self):
        """
        """
        # Todo: Create an adapter Address Management for IOrder         
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getInvoiceAddress()
        
        return address.getName()

    def getEmail(self):
        """
        """                
        customer = self.context.getCustomer()
        
        mtool = getToolByName(self.context, "portal_membership")

        try:
            member = mtool.getMemberById(customer.getId())
        except Unauthorized:
            return None
        else:
            if member is not None:
                return member.getProperty("email")
            
        return None
                
    def getItems(self):
        """
        """    
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
        
        items = []
        item_manager = IItemManagement(self.context)
        for item in item_manager.getItems():

            product_price_net = cm.priceToString(item.getProductPriceNet())
            price_net = cm.priceToString(item.getPriceNet())
            tax_rate = nc.floatToTaxString(item.getTaxRate())
            tax = cm.priceToString(item.getTax())
            price_gross = cm.priceToString(item.getPriceGross())

            temp = {
                "product_title"     : item.getProduct().Title(),
                "product_quantity"  : item.getProductQuantity(),
                "product_price_net" : product_price_net,
                "price_net"         : price_net,
                "tax_rate"          : tax_rate,
                "tax"               : tax,
                "price_gross"       : price_gross,
                "properties"        : item.getProperties(),
            }
            items.append(temp)

        return items

    def getPaymentValues(self):
        """
        """
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)

        price_net = cm.priceToString(self.context.getPaymentPriceNet())
        price_gross = cm.priceToString(self.context.getPaymentPriceGross())
        tax_rate = nc.floatToTaxString(self.context.getPaymentTaxRate())
        tax = cm.priceToString(self.context.getPaymentTax())
        
        return {
            "display" : self.context.getPaymentPriceGross() != 0,
            "price_net" : price_net,
            "price_gross" : price_gross,
            "tax_rate" : tax_rate,
            "tax" : tax, 
            "title" : "Cash on Delivery"
        }
        
    def getPaymentMethod(self):
        """
        """
        customer = self.context.getCustomer()
        pm = IPaymentManagement(customer)                
        return pm.getSelectedPaymentMethod()
        
    def getPaymentMethodType(self):
        """
        """
        pm = self.getPaymentMethod()
        return IType(pm).getType()
        
    def getPriceForCustomer(self):
        """
        """
        p = IPrices(self.context)        
        price = p.getPriceForCustomer()

        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)
        
    def getInvoiceAddress(self):
        """
        """
        # Todo: Create an adapter Address Management for IOrder 
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getInvoiceAddress()
        
        return {
            "name" : address.getName(),
            "company_name" : address.getCompanyName(),
            "address1" : address.getAddress1(),
            "address2" : address.getAddress2(),
            "zipcode" : address.getZipCode(),
            "city": address.getCity(),
            "country" : address.getCountry(),
            "phone" : address.getPhone()            
        }
        
    def getShippingAddress(self):
        """
        """
        # Todo: Create an adapter Address Management for IOrder         
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getShippingAddress()
        
        return {
            "name" : address.getName(),
            "company_name" : address.getCompanyName(),
            "address1" : address.getAddress1(),
            "address2" : address.getAddress2(),
            "zipcode" : address.getZipCode(),
            "city": address.getCity(),
            "country" : address.getCountry(),
            "phone" : address.getPhone(),
        }

    def getShipping(self):
        """
        """
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)

        price_net = cm.priceToString(self.context.getShippingPriceNet())
        price_gross = cm.priceToString(self.context.getShippingPriceGross())
        tax_rate = nc.floatToTaxString(self.context.getShippingTaxRate())
        tax = cm.priceToString(self.context.getShippingTax())
        
        return {
            "price_net" : price_net,
            "price_gross" : price_gross,
            "tax_rate" : tax_rate,
            "tax" : tax,    
        }
    
    def getState(self):
        """
        """
        wftool = getToolByName(self.context, "portal_workflow")
        return wftool.getInfoFor(self.context, "review_state")

    def isRedoPaymentAllowed(self):
        """
        """
        pm = IPaymentManagement(self.context)
        m = pm.getSelectedPaymentMethod()
        
        if IType(m).getType() not in REDO_PAYMENT_PAYMENT_METHODS:
            return False

        wftool = getToolByName(self.context, "portal_workflow")
        state = wftool.getInfoFor(self.context, "review_state")
        
        if state not in REDO_PAYMENT_STATES:
            return False

        return True

    def getOverviewURL(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        customer = ICustomerManagement(shop).getAuthenticatedCustomer()
        return "%s/my-orders" % customer.absolute_url()
        
    def redoPayment(self):
        """
        """
        # ATM only PayPal is allowed, so I haven't to differ and no redirect
        # is needed as the paypal process redirects to paypal.com
        if self.isRedoPaymentAllowed():
            pm = IPaymentManagement(self.context)
            pm.processSelectedPaymentMethod()
