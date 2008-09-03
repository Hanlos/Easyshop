# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from iqpp.easyshop.tests import utils
from iqpp.easyshop.interfaces import ICompleteness
from iqpp.easyshop.interfaces import IPaymentProcessing
from iqpp.easyshop.interfaces import IType

class TestCashOnDeliveryType(EasyShopTestCase):
    """
    """
    def testGetType(self):
        """
        """
        cod = self.shop.paymentmethods["cash-on-delivery"]    
        self.assertEqual(IType(cod).getType(), "generic-payment")

class TestCashOnDeliveryCompleteness(EasyShopTestCase):
    """
    """
    def testIsComplete(self):
        """
        """
        cod = self.shop.paymentmethods["cash-on-delivery"]                
        self.assertEqual(ICompleteness(cod).isComplete(), True)

class TestCashOnDeliveryPaymentProcessor(EasyShopTestCase):
    """
    """
    def testProcess(self):
        """
        """
        cod = self.shop.paymentmethods["cash-on-delivery"]                
        result = IPaymentProcessing(cod).process()        
        self.assertEqual(result.code, "NOT_PAYED")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCashOnDeliveryType))
    suite.addTest(makeSuite(TestCashOnDeliveryCompleteness))        
    suite.addTest(makeSuite(TestCashOnDeliveryPaymentProcessor))        
    return suite
                                               