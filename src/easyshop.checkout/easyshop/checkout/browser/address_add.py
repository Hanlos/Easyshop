# zope imports
from zope.formlib import form
from zope.component import queryUtility

from Products.Five.browser import pagetemplatefile
from Products.CMFPlone.utils import safe_unicode

# plone imports
from plone.app.form import base
from plone.i18n.normalizer.interfaces import IIDNormalizer

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement

class AddressAddForm(base.AddForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile("address_form.pt")
    form_fields = form.Fields(IAddress)

    label = _(u"Add Address")
    form_name = _(u"Add Address")

    @form.action(_(u"label_next", default=u"Next"), condition=form.haveInputWidgets, name=u'next')
    def handle_next_action(self, action, data):
        """
        """
        self.createAndAdd(data)
        ICheckoutManagement(self.context).redirectToNextURL("ADDED_ADDRESS")

    def createAndAdd(self, data):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        am = IAddressManagement(customer)

        # Set firstname and lastname of the superior customer object.
        if len(customer.firstname) == 0:
            customer.firstname = data.get("firstname")
            customer.lastname  = data.get("lastname")

        # Set email of the superior customer object.
        if len(customer.email) == 0:
            customer.email = data.get("email", u"")

        # Reset country selection.
        shop = IShopManagement(self.context).getShop()
        for country in shop.getCountries():
            if queryUtility(IIDNormalizer).normalize(safe_unicode(country)) == data.get("country"):
                customer.selected_country = country

        am.addAddress(data)

    def getAddressType(self):
        """
        """
        return self.request.get("address_type", "shipping")

    def isShippingAddress(self):
        """
        """
        return self.getAddressType() == "shipping"
