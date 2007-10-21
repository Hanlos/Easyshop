# zope imports 
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseFolder
from Products.Archetypes.atapi import BaseFolderSchema
from Products.Archetypes.atapi import registerType

# EasyShop imports
from Products.EasyShop.interfaces.carts import ICart
from easyshop.carts.config import PROJECTNAME

class Cart(BaseFolder):
    """A cart is a container for cart items.
    """
    implements(ICart)
    _at_rename_after_creation = True
    schema = BaseFolderSchema.copy()

registerType(Cart, PROJECTNAME)


