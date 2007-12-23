# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IWeightCriteria
from easyshop.core.interfaces import IShopManagement

class ProductAmountValidity:
    """Adapter which provides IValidity for weight criteria content objects.
    """
    implements(IValidity)
    adapts(IProductAmount)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, cart_item=None):
        """Returns True, if the amount of products of given cart item is greater
        than or equal as the criteria amount of products.
        """
        if cart_item.getAmount() >= self.context.getAmount():
            return True
        else:
            return False
