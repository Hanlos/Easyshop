# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement

class IExportView(Interface):    
    """
    """
    def getProducts():
        """
        """
        
    def getOrders():
        """
        """
       
class ExportView(BrowserView):
    """
    """
    implements(IExportView)
    
    def getProducts(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = "Product"
        )

        result = []

        line = [
            "Title",
            "Url",  
            "Price",          
            "Short Title",
            "Article ID",
            "Description",
            "Weight",
            "Short Text",
            "Text",
            "Image",]

        line = ['"%s"' % field for field in line]
        line = "\t".join(line)
        
        result.append(line)
            
        for brain in brains:
            product = brain.getObject()
            
            # Price 
            price = IPrices(product).getPriceGross()
            text = product.getText()
            text = text.replace("\n", "")
            
            line = [
                product.Title(),
                product.absolute_url(),
                price,
                product.getShortTitle(),
                product.getArticleId(),
                product.Description(),
                product.getWeight(),
                product.getShortText(),
                text,
            ]
                        
            # Images 
            im = IImageManagement(product)
            for image in im.getImages():
                if image.absolute_url() == product.absolute_url():
                    url = image.absolute_url() + "/image"
                else:
                    url = image.absolute_url()
                line.append(url)
                
            line = ['"%s"' % field for field in line]
            line = "\t".join(line)
            
            result.append(line)
            
        self.request.response.setHeader('Content-type', 'text/plain')
        self.request.response.setHeader(
            'Content-disposition',
            'attachment; filename=%s' % "products.txt"
        )

        return "\r\n".join(result)
                
    def getOrders(self):
        """
        """
        om = IOrderManagement(IShopManagement(self.context).getShop())
        
        result = []
        for order in om.getOrders():
            
            # omit closed orders
            wftool = getToolByName(self.context, "portal_workflow")
            if wftool.getInfoFor(order, "review_state") == "closed":
                continue
                
            customer = order.getCustomer()

            # am = IAddressManagement(customer)
            # shipping_address = am.getShippingAddress()
            
            im = IItemManagement(order)
            for item in im.getItems():

                product = item.getProduct()
                
                row = (
                    order.getId(),
                    customer.getId(),
                    # shipping_address.getFirstname() + " " + shipping_address.getLastname(),
                    product.getArticleId(),
                    product.Title(),
                    "%s"   % item.getProductQuantity(),
                    "%.2f" % item.getProductPriceGross(),
                    "%.2f" % item.getProductPriceNet(),
                    "%.2f" % item.getProductTax(),
                    "%.2f" % item.getTax(),
                    "%.2f" % item.getTaxRate(),
                    "%.2f" % item.getPriceGross(),
                    "%.2f" % item.getPriceNet(),
                )
                
                # row = ['"%s"' % field for field in row]
                row = ";".join(row)
                
                result.append(row)

        self.request.response.setHeader('Content-type', 'text/plain')
        self.request.response.setHeader(
            'Content-disposition',
            'attachment; filename=%s' % "orders.csv"
        )

        return "\n".join(result)