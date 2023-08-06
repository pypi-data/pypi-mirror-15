"""
    Zuora Interface Module
    ~~~~~~~~~~~~~~~~~~~~~~

    Current WSDL files are based on Zuora WSDL 48.

    Accounts for our Zuora setup are fetch by either A-user_id (i.e. A-32432)
    or just by the user id (look at the get_account WHERE clause).

    We also use custom fields in some of our queries: CustomField__c that
    could break for people who don't use our custom fields (i.e. ShortCode__c)

    Usage example:
    import zuora

    z = zuora.Zuora(SETTINGS)
    account = z.get_account(23432)
"""
from datetime import datetime, date, timedelta
from os import path
import re
import httplib2

from suds import WebFault
from suds.client import Client
from suds.sax.element import Element
from suds.xsd.doctor import Import, ImportDoctor
from suds.transport.http import HttpAuthenticated, HttpTransport
from suds.transport import Reply
from suds.sax.text import Text

import logging
log = logging.getLogger(__name__)

# Tell suds to stop logging and stfu (it logs noise as errors)
log_suds = logging.getLogger('suds')
log_suds.propagate = False

SOAP_TIMESTAMP = '%Y-%m-%d'


from rest_client import RestClient


class HttpTransportWithKeepAlive(HttpAuthenticated, object):

    def __init__(self, use_cert=False):
        super(HttpTransportWithKeepAlive, self).__init__()
        if use_cert:
            path_to_certs = path.abspath(path.dirname(__file__))
            cert_file = path_to_certs + "/PCA-3G5.pem"
            self.http = httplib2.Http(timeout=20, ca_certs=cert_file)
        else:
            self.http = httplib2.Http(timeout=20,
                                  disable_ssl_certificate_validation=True)

    def open(self, request):
        return HttpTransport.open(self, request)

    def send(self, request):
        headers, message = self.http.request(request.url, "POST",
                                             body=request.message,
                                             headers=request.headers)
        response = Reply(200, headers, message)
        return response


class ZuoraException(Exception):
    """This is our base exception for the Zuora lib"""
    pass


class DoesNotExist(ZuoraException):
    """
    Exception for when objects don't exist in Zuora
    """
    pass


class MissingRequired(ZuoraException):
    """
    Exception for when a required parameter is missing
    """
    pass


# main class
class Zuora:

    def __init__(self, zuora_settings):
        """
        Usage example:

        Required dictionary settings for zuora client:

        username : str : username for logging into Zuora
        password : str : password for logging into Zuora
        wsdl_file : str : path to wsdl file used for suds library

        Optional dictionary settings:

        gateway_name : str : The name of the gateway used for payment
                             authorization
        test_users : str : Used if you only desire to create test user
                           accounts. Adds the custom field Test_Account__c
                           to all created users.
        """
        # Assign settings
        self.username = zuora_settings["username"]
        self.password = zuora_settings["password"]
        self.wsdl_file = zuora_settings["wsdl_file"]
        self.base_dir = path.dirname(__file__)
        self.authorize_gateway = zuora_settings.get("gateway_name")
        self.create_test_users = zuora_settings.get("test_users", None)
        self.use_cert = zuora_settings.get("SSL", False)

        # Build Client
        imp = Import('http://object.api.zuora.com/')
        imp.filter.add('http://api.zuora.com/')
        imp.filter.add('http://fault.api.zuora.com/')
        schema_doctor = ImportDoctor(imp)

        if self.wsdl_file.startswith("/"):
            wsdl_file = 'file://%s' % path.abspath(self.wsdl_file)
        else:
            wsdl_file = 'file://%s' % path.abspath(
                                        self.base_dir + "/" + self.wsdl_file)

        self.client = Client(
                        url=wsdl_file,
                        doctor=schema_doctor,
                        cache=None,
                        transport=HttpTransportWithKeepAlive(self.use_cert))

        # Force No Cache
        self.client.set_options(cache=None)
        
        # Create the rest client
        self.rest_client = RestClient(zuora_settings)

        self.session_id = None

    def reset_transport(self):
        self.client.options.transport = HttpTransportWithKeepAlive(
                                                                self.use_cert)
        self.session_id = None

    # Client Create
    def call(self, fn, *args, **kwargs):
        """
        Wraps the Error handling for the client call.
        :param function fn: function to call (ie., self.client.service.delete)

        :returns: the client response
        """
        last_error = None

        for i in range(0, 3):
            if self.session_id is None or self.session_expiration <= datetime.now():
                self.login()
            try:
                response = fn(*args, **kwargs)
                log.info("Call sent: %s" % self.client.last_sent())
                log.info("Call received: %s" % self.client.last_received())
                # THIS OCCASIONALLY HAPPENS
                # AND ITS BAD WE NEED TO RESET
                if isinstance(response, Text):
                    log.error("Zuora: REALLY Unexpected Response!!!! %s, RESETTING TO RETRY", response)
                    self.reset_transport()
                else:
                    log.debug("Zuora: Successful Response %s", response)
                    return response
            except WebFault as err:
                if err.fault.faultcode == "fns:INVALID_SESSION":
                    log.warn("Zuora: Invalid Session, LOGGING IN")
                    self.session_id = None
                else:
                    log.error("WebFault. %s", err.__dict__)
                    raise ZuoraException("WebFault. %s" % err.__dict__)
            except Exception as error:
                log.error("Zuora: Unexpected Error. %s" % error)
                last_error = error
                self.reset_transport()

        raise ZuoraException("Zuora: Unexpected Error. %s" % last_error)

    # Client Create
    def create(self, z_object):
        """
        Use create() to create one or more objects of a specific type.
        You can specify different types in different create() calls, but
        each create() call must apply to only one type of object.

        :param z_object z_object: object to create

        :returns: the API response
        """

        # Call Create
        fn = self.client.service.create
        log.info("***Zuora Create Request: %s" % z_object)
        response = self.call(fn, z_object)
        log.info("***Zuora Create Response: %s" % response)
        # return the response
        return response

    def amend(self, amendments, amend_options=None):
        """
        Use amend() to to generate an invoice and capture payment
        electronically when amending subscriptions. The call also allows
        you to preview the invoices before amending the subscription.

        :param z_object z_object: object to amend

        :returns: the API response
        """

        # Call Create
        fn = self.client.service.amend
        request = self.client.factory.create("ns0:AmendRequest")
        request.Amendments = amendments
        if amend_options:
            request.AmendOptions = amend_options
        log.info("***Zuora Amend Request: %s" % request)
        response = self.call(fn, request)
        log.info("***Zuora Amend Response: %s" % response)
        # return the response
        return response

    def delete(self, obj_type, id_list=[]):
        """
        Deletes one or more objects of the same type. You can specify different
        types in different deletecalls, but each delete call must only apply to
        one type of object.

        :param str type: The type of object that you are deleting.
        :param list id_list: A list of ids for the objects you want to delete.

        :returns: the API response
        """

        # Call Update
        fn = self.client.service.delete
        response = self.call(fn, obj_type, id_list)

        # return the response
        return response

    # Client Login
    def login(self):
        """
        Creates the SOAP SessionHeader with the correct session_id from Zuora

        TODO: investigate methodology to persist session_id across sessions
        we are currently keeping the session in memory for < 8 hours
        which is the session expiration time of Zuora
        """
        self.session_expiration = datetime.now() + timedelta(hours=7, minutes=55)
        login_response = self.client.service.login(username=self.username,
                                                   password=self.password)
        self.session_id = login_response.Session

        # Define Session Namespace
        session_namespace = ('ns1', 'http://api.zuora.com/')

        # Create a session element to hold the value of result.Session
        # from our login call
        session = Element('session', ns=session_namespace)\
                    .setText(self.session_id)

        # Create a session_header element to enclose the session element
        SessionHeader = Element('SessionHeader', ns=session_namespace)

        # Append the session element inside the session_header element
        SessionHeader.append(session)
        self.client.set_options(soapheaders=[SessionHeader])

    def query(self, query_string):
        """
        Pass the zosql querystring into the query() SOAP method
        TODO: add retry_count to keep loop of doom out of picture
        TODO: investigate faultcodes for different error handling
        TODO: option: everytime you capability.create you check if alive

        :param string query_string: ZQL query string

        :returns: the API response
        """

        # format query string (remove linebreaks, tabs, etc.)
        query_string = ' '.join(query_string.split())

        # Call Query
        fn = self.client.service.query
        response = self.call(fn, queryString=query_string)

        # return the response
        return response

    def query_more(self, query_locator):
        """
        Use queryMore() to request additional results from a previous
        query() call. If your initial query() call returns more
        than 2000 results, you can use queryMore() to query for more
        the additional results

        :param string query_string: ZQL query string

        :returns: the API response
        """

        # Call Query
        fn = self.client.service.queryMore
        response = self.call(fn, queryLocator=query_locator)

        # return the response
        return response

    def update(self, z_object):
        """
        Updates the information in one or more objects of the same type. You
        can specify different types of objects in different update() calls,
        but each specific update() call must apply to one type of object.

        :param z_object z_object: object to create

        :returns: the API response
        """

        # Call Update
        fn = self.client.service.update
        response = self.call(fn, z_object)

        # return the response
        return response

    def amend_new_product(self, name, subscription_id, product_rate_plan_id,
                          product_charge_id, charge_number=None, description=None,
                          status='Completed'):
        """
        Use Amendment to make changes to a subscription. For example, if you
        wish to change the terms and conditions of a subscription, you would
        use an Amendment.

        :param str name: A name for the amendment. (100 chars)
        :param str subscription_id: The identification number for the\
            subscription that is being amended.
        :param str product_rate_plan_id: ProductRatePlanID

        :returns: response
        """
        effective_date = datetime.now().strftime(SOAP_TIMESTAMP)

        zAmendment = self.client.factory.create('ns2:Amendment')
        zAmendment.ContractEffectiveDate = effective_date
        if name:
            zAmendment.Name = name
        else:
            zAmendment.Name = "%s %s" % (name, effective_date)
        zAmendment.Status = status
        zAmendment.SubscriptionId = subscription_id
        zAmendment.Type = "NewProduct"
        if description:
            zAmendment.Description = description
        zAmendment.ServiceActivationDate = effective_date
        # zAmendment.CustomerAcceptance = False
        zRPData = self.client.factory.create('ns0:RatePlanData')
        zRP = self.client.factory.create('ns0:RatePlan')
        zRP.AmendmentType = 'NewProduct'
        zRP.ProductRatePlanId = product_rate_plan_id
        zRP.SubscriptionId = subscription_id
        zRPData.RatePlan = zRP
        zRPCData = self.client.factory.create('ns0:RatePlanChargeData')
        zRPC = self.client.factory.create('ns0:RatePlanCharge')
        if charge_number:
            zRPC.ChargeNumber = charge_number
        zRPC.ProductRatePlanChargeId = product_charge_id
        zRPCData.RatePlanCharge = zRPC

        zRPData.RatePlanChargeData = zRPCData
        zAmendment.RatePlanData = zRPData

        # AmendOptions
        zOptions = self.client.factory.create('ns0:AmendOptions')
        zOptions.ProcessPayments = False

        # Create Amendment
        response = self.amend([zAmendment], zOptions)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error creating Amendment. %s" % response)
        zAmendment.Id = response[0].AmendmentIds[0]
        return zAmendment

    def create_product_amendment(self, effective_date, subscription_id,
                                  name_prepend, amendment_type,
                                  status="Draft", description=None,
                                  name=None):
        """
        Creates a new product amendment and adds an id for the new
        amendment
        """
        # Make Amendment
        zAmendment = self.client.factory.create('ns2:Amendment')
        zAmendment.EffectiveDate = effective_date
        if name:
            zAmendment.Name = name
        else:
            zAmendment.Name = "%s %s" % (name_prepend, effective_date)
        zAmendment.Status = status
        zAmendment.SubscriptionId = subscription_id
        zAmendment.Type = amendment_type
        if description:
            zAmendment.Description = description

        # Create Amendment
        response = self.create(zAmendment)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error creating Amendment. %s" % response)
        zAmendment.Id = response[0].Id

        return zAmendment

    def update_product_amendment(self, effective_date, zAmendment,
                                 status='Completed'):
        """
        Updates a product amendment and returns the update response
        """
        zAmendmentUpdate = self.client.factory.create('ns2:Amendment')
        zAmendmentUpdate.Id = zAmendment.Id
        zAmendmentUpdate.ContractEffectiveDate = effective_date
        zAmendmentUpdate.Status = status
        response = self.update(zAmendmentUpdate)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error update Amendment. %s" % response)

        # return
        return response

    def add_product_amendment(self, name, subscription_id,
                              product_rate_plan_id):
        """
        Use Amendment to make changes to a subscription. For example, if you
        wish to change the terms and conditions of a subscription, you would
        use an Amendment.

        :param str name: A name for the amendment. (100 chars)
        :param str subscription_id: The identification number for the\
            subscription that is being amended.
        :param str product_rate_plan_id: ProductRatePlanID

        :returns: response
        """
        effective_date = datetime.now().strftime(SOAP_TIMESTAMP)

        # Create the new product amendment
        zAmendment = self.create_product_amendment(
                                        effective_date,
                                        subscription_id,
                                        name_prepend="New Product Amendment",
                                        amendment_type='NewProduct')

        # Make Rate Plan
        zRatePlan = self.client.factory.create('ns0:RatePlan')
        zRatePlan.AmendmentType = "NewProduct"
        zRatePlan.AmendmentId = zAmendment.Id
        zRatePlan.ProductRatePlanId = product_rate_plan_id
        response = self.create(zRatePlan)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error creating RatePlan. %s" % response)

        # Update the product amendment
        response = self.update_product_amendment(effective_date, zAmendment)

        # return
        return response

    def cancel_subscription(self, subscription_key, effective_date=None):
        """
        Canceling a Subscription (using Amendment)

        :param str subscription_key: The identification number/name for the
            subscription that is being amended.

        :returns: response
        """
        if not effective_date:
            response = self.rest_client.subscription.cancel_subscription(
                                                             subscription_key)
        else:
            response = self.rest_client.subscription.cancel_subscription(
                    subscription_key,
                    jsonParams={'cancellationEffectiveDate': effective_date})
        return response
    
    def create_payment_method(self, baid=None, user_email=None):
        payment_method = self.client.factory.create('ns2:PaymentMethod')
        if baid:
            payment_method.PaypalBaid = baid
            # Paypal user e-mail required
            payment_method.PaypalEmail = user_email
            payment_method.PaypalType = 'ExpressCheckout'
            payment_method.Type = 'PayPal'

        return payment_method

    def create_active_account(self, zAccount=None, zContact=None,
                              payment_method_id=None, user=None,
                              billing_address=None, shipping_address=None,
                              site_name=None, prepaid=False,
                              gateway_name=None):
        """
        Create an Active Account for use in Subscribe()
        """
        # Create Account if it doesn't exist
        if not zAccount:
            zAccount = self.make_account(user=user, site_name=site_name,
                                         billing_address=billing_address,
                                         gateway_name=gateway_name)

        # Create Bill-To Contact on Account
        if not zContact:
            zContact = self.make_contact(user=user,
                                         billing_address=billing_address,
                                         zAccount=zAccount)
        
        # Add the shipping contact if it exists
        if shipping_address:
            zShippingContact = self.make_contact(user=user,
                                         billing_address=shipping_address,
                                         zAccount=zAccount)
        else:
            zShippingContact = None

        # Create Payment Method on Account
        if payment_method_id:
            zPaymentMethod = self.get_payment_method(payment_method_id)
        else:
            zPaymentMethod = None

        self.activate_account(zAccount, zContact,
                              zShippingContact=zShippingContact,
                              payment_method_id=payment_method_id,
                              prepaid=prepaid)

        return {'account': zAccount, 'contact': zContact,
                'payment_method': zPaymentMethod,
                'shipping_contact': zShippingContact}

    def activate_account(self, zAccount, zContact, zShippingContact=None,
                         payment_method_id=None, prepaid=None):
        # Now Update the Draft Account to be Active
        zAccountUpdate = self.client.factory.create('ns2:Account')
        zAccountUpdate.Id = zAccount.Id
        zAccountUpdate.Status = 'Active'
        zAccountUpdate.BillToId = zContact.Id
        if zShippingContact:
            zAccountUpdate.SoldToId = zShippingContact.Id
        else:
            zAccountUpdate.SoldToId = zContact.Id
        # If we don't require a payment method, AutoPay must be False
        if payment_method_id and not prepaid:
            zAccountUpdate.DefaultPaymentMethodId = payment_method_id
            zAccountUpdate.AutoPay = True
        elif payment_method_id:
            zAccountUpdate.DefaultPaymentMethodId = payment_method_id
            zAccountUpdate.AutoPay = False
        else:
            zAccountUpdate.AutoPay = False
        response = self.update(zAccountUpdate)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error updating Account. %s" % response)

    def get_account(self, user_id, account_id=None, id_only=False):
        """
        Checks to see if the loaded user has an account
        """
        if id_only:
            fields = 'Id'
        else:
            fields = """Id, AccountNumber, AutoPay, Balance, DefaultPaymentMethodId,
                        PaymentGateway, Name, Status, UpdatedDate"""
        # If no account id was specified
        if not account_id:
            qs = """
                SELECT
                    %s
                FROM Account
                WHERE AccountNumber = '%s' or AccountNumber = 'A-%s'
                """ % (fields, user_id, user_id)
        else:
            qs = """
                SELECT
                    %s
                FROM Account
                WHERE Id = '%s'
                """ % (fields, account_id)

        response = self.query(qs)
        if getattr(response, "records") and len(response.records) > 0:
            zAccount = response.records[0]
            return zAccount
        else:
            raise DoesNotExist("Unable to find Account for User ID %s"\
                            % user_id)

    def get_contact(self, email=None, account_id=None):
        """
        Checks to see if the loaded user has a contact
        """
        qs_filter = []

        if account_id:
            qs_filter.append("AccountId = '%s'" % account_id)

        if email:
            qs_filter.append("PersonalEmail = '%s'" % email)

        qs = """
            SELECT
                AccountId, Address1, Address2, City, Country, County,
                CreatedById, CreatedDate, Description, Fax, FirstName,
                HomePhone, Id, LastName, MobilePhone, NickName, OtherPhone,
                OtherPhoneType, PersonalEmail, PostalCode, State, TaxRegion,
                UpdatedById, UpdatedDate, WorkEmail, WorkPhone
            FROM Contact
            WHERE %s
            """  % " AND ".join(qs_filter)

        response = self.query(qs)
        if getattr(response, "records") and len(response.records) > 0:
            zContact = response.records[0]
            return zContact
        else:
            raise DoesNotExist("Unable to find Contact for Email %s"\
                            % email)

    def get_invoice(self, invoice_id=None):
        """
        Gets the Invoice
        """

        # Search for Matching Account
        qs = """
            SELECT
                AccountID, AdjustmentAmount, Amount,
                Balance, CreatedDate, DueDate,
                IncludesOneTime, IncludesRecurring, IncludesUsage,
                InvoiceDate, InvoiceNumber,
                PaymentAmount, RefundAmount, Status,
                TargetDate
            FROM Invoice
            WHERE Id = '%s'
            """ % invoice_id

        response = self.query(qs)
        if getattr(response, "records") and len(response.records) > 0:
            zInvoice = response.records[0]
            return zInvoice
        else:
            raise DoesNotExist("Unable to find Invoice for Id %s"\
                            % invoice_id)

    def get_invoice_pdf(self, invoice_id=None):
        """
        Gets the Invoice PDF (Base64 Encoded String)
        See: http://bit.ly/Pr7sgT
        """

        # Search for Matching Invoice PDF
        qs = """
            SELECT
                Body
            FROM Invoice
            WHERE Id = '%s'
            """ % invoice_id

        response = self.query(qs)
        if getattr(response, "records") and len(response.records) > 0:
            zInvoice = response.records[0]
            return zInvoice.Body
        else:
            raise DoesNotExist("Unable to find Invoice for Id %s"\
                            % invoice_id)

    def get_invoices(self, account_id=None, minimum_balance=None,
                     status=None):
        """
        Gets the Invoices matching criteria.

        :param str account_id: Account ID
        """

        # Defaults
        qs_filter = []

        if account_id:
            qs_filter.append("AccountId = '%s'" % account_id)
        if minimum_balance:
            qs_filter.append("Balance > '%s'" % minimum_balance)
        if status:
            qs_filter.append("Status = '%s'" % status)

        if qs_filter:
            qs = """
                SELECT
                    AccountID, AdjustmentAmount, Amount,
                    Balance, CreatedDate, DueDate,
                    IncludesOneTime, IncludesRecurring, IncludesUsage,
                    InvoiceDate, InvoiceNumber,
                    PaymentAmount, RefundAmount, Status,
                    TargetDate
                FROM Invoice
                WHERE %s
                """ % " AND ".join(qs_filter)

            response = self.query(qs)
            zInvoices = response.records

            # Return the Match
            return zInvoices

        # Return None if Not Found
        return None

    def get_invoice_items(self, invoice_id=None, subscription_id=None):
        """
        Gets the InvoiceItems matching criteria.

        :param str invoice_id: Invoice ID
        :param str subscription_id: Subscription ID
        """

        # Defaults
        qs_filter = []

        if invoice_id:
            qs_filter.append("InvoiceId = '%s'" % invoice_id)

        if subscription_id:
            qs_filter.append("SubscriptionId = '%s'" % subscription_id)

        if qs_filter:
            qs = """
                SELECT
                    AccountingCode, ChargeAmount, ChargeDate,
                    ChargeDescription, ChargeName, ChargeNumber,
                    CreatedById, CreatedDate, InvoiceId,
                    ProcessingType, ProductDescription, ProductId,
                    ProductName, Quantity, RatePlanChargeId,
                    RevRecCode, RevRecStartDate, RevRecTriggerCondition,
                    ServiceEndDate, ServiceStartDate, SKU,
                    SubscriptionId, SubscriptionNumber,
                    TaxAmount, TaxCode, TaxExemptAmount, UnitPrice, UOM,
                    UpdatedById, UpdatedDate
                FROM InvoiceItem
                WHERE %s
                """ % " AND ".join(qs_filter)

            response = self.query(qs)
            zRecords = response.records

            # Return the Match
            return zRecords

        # Return None if Not Found
        return None

    def apply_invoice_adjustment(self, invoice_id, amount):
        InvoiceAdjustment = self.client.factory.create('ns2:InvoiceAdjustment')
        InvoiceAdjustment.InvoiceId = invoice_id
        InvoiceAdjustment.Amount = amount
        InvoiceAdjustment.ReasonCode = 'Write-off'
        if amount > 0.0:
            InvoiceAdjustment.Type = 'Credit'
        else:
            InvoiceAdjustment.Type = 'Debit'
        response = self.create(InvoiceAdjustment)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error within Invoice Adjustment. %s" % response)

        # return
        return response

    def get_invoice_payment(self, invoice_payment_id=None):
        """
        Gets the Invoice Payment

        :param str invoice_payment_id: Invoice Payment ID
        """

        # Search for Matching Account
        qs = """
            SELECT
                Amount, CreatedById, CreatedDate, InvoiceId, PaymentId,
                RefundAmount, UpdatedById, UpdatedDate
            FROM InvoicePayment
            WHERE Id = '%s'
            """ % invoice_payment_id

        response = self.query(qs)
        if getattr(response, "records") and len(response.records) > 0:
            zInvoicePayment = response.records[0]
            return zInvoicePayment
        else:
            raise DoesNotExist("Unable to find InvoicePayment for Id %s"\
                            % invoice_payment_id)

    def get_invoice_payments(self, invoice_id=None, payment_id=None):
        """
        Gets the InvoicePayments matching criteria.

        :param str invoice_id: Invoice ID
        :param str payment_id: Payment ID
        """

        # Defaults
        qs_filter = []

        if invoice_id:
            qs_filter.append("InvoiceId = '%s'" % invoice_id)
        if payment_id:
            qs_filter.append("PaymentId = '%s'" % payment_id)
        if qs_filter:
            qs = """
                SELECT
                    Amount, CreatedById, CreatedDate, InvoiceId, PaymentId,
                    RefundAmount, UpdatedById, UpdatedDate
                FROM InvoicePayment
                WHERE %s
                """ % " AND ".join(qs_filter)
            response = self.query(qs)
            zInvoicePayments = response.records

            # Return the Match
            return zInvoicePayments

        # Return None if Not Found
        return None

    def get_payment(self, payment_id=None):
        """
        Gets the zPayment
        """

        # Search for Matching zPayment
        qs = """
            SELECT
                AccountID, AccountingCode, Amount, AppliedCreditBalanceAmount,
                AuthTransactionId,
                BankIdentificationNumber, CancelledOn, Comment,
                CreatedById, CreatedDate, EffectiveDate, GatewayOrderId,
                GatewayResponse, GatewayResponseCode, GatewayState,
                MarkedForSubmissionOn,
                PaymentMethodID, PaymentNumber, ReferenceId, RefundAmount,
                SecondPaymentReferenceId, SettledOn, SoftDescriptor,
                Status, SubmittedOn, TransferredToAccounting,
                Type, UpdatedById, UpdatedDate
            FROM Payment
            WHERE Id = '%s'
            """ % payment_id

        response = self.query(qs)
        if getattr(response, "records") and len(response.records) > 0:
            zPayment = response.records[0]
            return zPayment
        else:
            raise DoesNotExist("Unable to find Payment for Id %s"\
                            % payment_id)

    def get_payments(self, account_id=None):
        """
        Gets the Payments matching criteria.

        :param str account_id: Account ID
        """

        # Defaults
        qs_filter = []

        if account_id:
            qs_filter.append("AccountId = '%s'" % account_id)

        if qs_filter:
            qs = """
                SELECT
                    AccountID, AccountingCode, Amount,
                    AppliedCreditBalanceAmount, AuthTransactionId,
                    BankIdentificationNumber, CancelledOn, Comment,
                    CreatedById, CreatedDate, EffectiveDate, GatewayOrderId,
                    GatewayResponse, GatewayResponseCode, GatewayState,
                    MarkedForSubmissionOn,
                    PaymentMethodID, PaymentNumber, ReferenceId, RefundAmount,
                    SecondPaymentReferenceId, SettledOn, SoftDescriptor,
                    Status, SubmittedOn, TransferredToAccounting,
                    Type, UpdatedById, UpdatedDate
                FROM Payment
                WHERE %s
                """ % " AND ".join(qs_filter)

            response = self.query(qs)
            zPayments = response.records

            # Return the Match
            return zPayments

        # Return None if Not Found
        return None

    def get_payment_method(self, payment_method_id):
        """
        Gets the Payment Method details.

        :param str payment_method_id: PaymentMethodId
        """
        qs = """
            SELECT
                AccountId, Active,
                CreatedById, CreatedDate,
                CreditCardAddress1, CreditCardAddress2,
                CreditCardCity, CreditCardCountry,
                CreditCardExpirationMonth, CreditCardExpirationYear,
                CreditCardHolderName, CreditCardMaskNumber,
                CreditCardPostalCode, CreditCardState, CreditCardType,
                Email, Name, PaypalBaid, PaypalEmail,
                PaypalPreapprovalKey, PaypalType, Phone, Type
            FROM PaymentMethod
            WHERE Id = '%s'
            """ % payment_method_id

        response = self.query(qs)
        if getattr(response, "records") and len(response.records) > 0:
            zPaymentMethod = response.records[0]
            return zPaymentMethod
        else:
            raise DoesNotExist("Unable to find Payment Method for %s. %s"\
                            % (payment_method_id, response))

    def get_payment_methods(self, account_id=None, account_number=None,
                            email=None, phone=None):
        """
        Gets the Payment Methods matching criteria.

        :optparam str account_number: Account Number to return the default
            payment method
        :optparam str account_id: Account ID
        :optparam str email: Email Address of the Payee
        :optparam str phone: Phone Number of the Payee
        """

        # Defaults
        qs_filter = []

        # Account Number
        if account_number:
            qs = """
                SELECT
                    DefaultPaymentMethodId
                FROM Account
                WHERE AccountNumber = '%s' or AccountNumber = 'A-%s'
                """ % (account_number, account_number)

            response = self.query(qs)
            if getattr(response, "records") and len(response.records) > 0:
                zAccount = response.records[0]
                # Check for a default payment method
                try:
                    payment_method_id = zAccount.DefaultPaymentMethodId
                except:
                    return []

                # Return as a List
                return [self.get_payment_method(payment_method_id)]

        if account_id:
            qs_filter.append("AccountId = '%s'" % account_id)

        if email:
            qs_filter.append("Email = '%s'" % email)

        if phone:
            qs_filter.append("Phone = '%s'" % phone)

        if qs_filter:
            qs = """
                SELECT
                    AccountId, Active,
                    CreatedById, CreatedDate,
                    CreditCardAddress1, CreditCardAddress2,
                    CreditCardCity, CreditCardCountry,
                    CreditCardExpirationMonth, CreditCardExpirationYear,
                    CreditCardHolderName, CreditCardMaskNumber,
                    CreditCardPostalCode, CreditCardState, CreditCardType,
                    Email, Name, PaypalBaid, PaypalEmail,
                    PaypalPreapprovalKey, PaypalType, Phone, Type
                FROM PaymentMethod
                WHERE %s
                """ % " AND ".join(qs_filter)

            response = self.query(qs)
            zPaymentMethods = response.records

            # Return the Match
            return zPaymentMethods
        return []

    def get_products(self, product_id=None, sku=None, name=None):
        """
        Gets the Product.

        :param str product_id: ProductID
        :param str sku: SKU
        :param str name: Product Name
        """
        qs_filter = None

        qs = """
            SELECT
                Description, EffectiveEndDate, EffectiveStartDate,
                Id, SKU, Name
            FROM Product
            """

        # If we're looking for one specific product
        if product_id:
            qs_filter = "Id = '%s'" % product_id
        elif sku:
            qs_filter = "SKU = '%s'" % sku
        elif name:
            qs_filter = "Name = '%s'" % name
        if qs_filter:
            qs += " WHERE %s" % qs_filter

        response = self.query(qs)
        try:
            zProducts = response.records
            return zProducts
        except:
            raise DoesNotExist("Unable to find Product for %s"\
                            % product_id)

    def get_rate_plan_charges(self, rate_plan_id=None,
                                    rate_plan_id_list=None,
                                    product_rate_plan_charge_id=None,
                                    pricing_info="Price"):
        """
        Gets the Rate Plan Charges

        :param str rate_plan_id: RatePlanID
        :param list rate_plan_id_list: list of RatePlanID's
        """
        # Note: Can only use OveragePrice or Price or IncludedUnits or
        # DiscountAmount or DiscountPercentage in one query
        # Note: No clue what that means, but that's the error I get from Zuora
        # if I try to include them all.
        qs = """
            SELECT
                AccountingCode, ApplyDiscountTo,
                BillCycleDay, BillCycleType,
                BillingPeriodAlignment, ChargedThroughDate,
                ChargeModel, ChargeNumber, ChargeType, CreatedById,
                CreatedDate, Description, DiscountLevel,
                DMRC, DTCV, EffectiveEndDate, EffectiveStartDate,
                IsLastSegment, MRR, Name, NumberOfPeriods,
                OriginalId, OverageCalculationOption,
                OverageUnusedUnitsCreditOption, %s,
                PriceIncreasePercentage, ProcessedThroughDate,
                ProductRatePlanChargeId, Quantity, RatePlanId,
                Segment, TCV, TriggerDate, TriggerEvent,
                UnusedUnitsCreditRates, UOM, UpdatedById, UpdatedDate,
                UpToPeriods, UsageRecordRatingOption,
                UseDiscountSpecificAccountingCode, Version
            FROM RatePlanCharge
            """ % pricing_info
        where_id_string = "RatePlanId = '%s'"
        # If only querying with one rate plan id
        if rate_plan_id:
            qs_filter = where_id_string % rate_plan_id
        # Otherwise we're querying with multiple rate plan id's
        else:
            qs_filter = None
            if rate_plan_id_list:
                id_filter_list = [where_id_string % rp_id \
                          for rp_id in rate_plan_id_list]
                # Combine the rate plan ids for the WHERE clause
                qs_filter = " OR ".join(id_filter_list)

        qs += " WHERE %s" % qs_filter
        response = self.query(qs)
        try:
            return response.records
        except:
            raise DoesNotExist(
                            "Unable to find Rate Plan Charges for %s"\
                            % rate_plan_id)

    def get_product_rate_plans(self, product_rate_plan_id=None,
                               product_id_list=None, effective_start=None,
                               effective_end=None):
        """
        Gets the Product Rate Plan.

        :param str product_rate_plan_id: ProductRatePlanID
        :param list prp_id_list: A list of ProductRatePlanID's
        :param datetime effective_start: Effective start date
        :param datetime effective_end: Effective end date
        """
        qs = """
            SELECT
                Description, EffectiveEndDate, EffectiveStartDate,
                Id, Name, ProductId
            FROM ProductRatePlan
            """

        # If only one product is requested
        if product_rate_plan_id:
            qs_filter = "Id = '%s'" % product_rate_plan_id
        # Otherwise multiple products are being requested
        else:
            qs_filter = None
            if product_id_list:
                id_filter_list = ["ProductId = '%s'" % pid \
                          for pid in product_id_list]
                # Combine the product rate plan ids for the WHERE clause
                qs_filter = " OR ".join(id_filter_list)

            if effective_start:
                # If there is an effective start, and not an effective end
                # use the same date for both
                if not effective_end:
                    effective_end = effective_start
                date_where = """EffectiveEndDate >= '%s' AND
                                EffectiveStartDate <= '%s'
                             """ % (effective_end, effective_start)
                # If a previous filter exists, AND them together
                if qs_filter:
                    qs_filter += " AND %s" % date_where
                else:
                    qs_filter = date_where

        qs += " WHERE %s" % qs_filter

        response = self.query(qs)
        try:
            zProductRatePlans = response.records
            return zProductRatePlans
        except:
            raise DoesNotExist("Unable to find Product Rate Plan for %s"\
                            % product_rate_plan_id)

    def get_product_rate_plan_charges(self, product_rate_plan_id=None,
                                      product_rate_plan_id_list=None,
                                      product_rate_plan_charge_id=None):
        """
        Gets the Product Rate Plan Charges.

        :param str product_rate_plan_id: ProductRatePlanID
        :param list product_rate_plan_id_list: list of ProductRatePlanID's
        """
        # Get Product Rate Plan Charges
        qs = """
            SELECT
                AccountingCode, BillCycleDay, BillCycleType, BillingPeriod,
                BillingPeriodAlignment, ChargeModel, ChargeType,
                DefaultQuantity, Description,
                Id,  IncludedUnits, MaxQuantity,
                MinQuantity, Name, NumberOfPeriod, OverageCalculationOption,
                OverageUnusedUnitsCreditOption,
                PriceIncreasePercentage, ProductRatePlanId,
                RevRecCode, RevRecTriggerCondition,
                SmoothingModel, SpecificBillingPeriod,
                TriggerEvent, UOM, UpToPeriods,
                UseDiscountSpecificAccountingCode
            FROM ProductRatePlanCharge
            """
        where_id_string = "ProductRatePlanId = '%s'"
        # If only querying with one product rate plan id
        if product_rate_plan_id:
            qs_filter = where_id_string % product_rate_plan_id
        # if we are pulling a product rate plan charge based on its id
        elif product_rate_plan_charge_id:
            qs_filter = "Id = '%s'" % product_rate_plan_charge_id
        # Otherwise multiple products are being requested
        else:
            qs_filter = None
            if product_rate_plan_id_list:
                id_filter_list = [where_id_string % prp_id \
                          for prp_id in product_rate_plan_id_list]
                # Combine the product rate plan ids for the WHERE clause
                qs_filter = " OR ".join(id_filter_list)

        qs += " WHERE %s" % qs_filter

        response = self.query(qs)
        try:
            return response.records
        except:
            raise DoesNotExist(
                            "Unable to find Product Rate Plan Charges for %s"\
                            % product_rate_plan_id)

    def get_product_rate_plan_charge_tiers(
                                    self,
                                    product_rate_plan_charge_id=None,
                                    product_rate_plan_charge_id_list=None):
        """
        Gets the Product Rate Plan Charges.

        :param str product_rate_plan_charge_id: ProductRatePlanChargeId
        :param list product_rate_plan_charge_id_list: list of
                ProductRatePlanChargeId's
        """
        qs = """
            SELECT
                Currency, EndingUnit, IsOveragePrice,
                Price, PriceFormat, ProductRatePlanChargeId,
                StartingUnit, Tier
            FROM ProductRatePlanChargeTier
            """
        where_id_string = "ProductRatePlanChargeId = '%s'"
        # If only one product is requested
        if product_rate_plan_charge_id:
            qs_filter = where_id_string % product_rate_plan_charge_id
        # Otherwise multiple products are being requested
        else:
            qs_filter = None
            if product_rate_plan_charge_id_list:
                id_filter_list = [where_id_string % prpc_id \
                          for prpc_id in product_rate_plan_charge_id_list]
                # Combine the product rate plan charge ids
                # for the WHERE clause
                qs_filter = " OR ".join(id_filter_list)

        qs += " WHERE %s" % qs_filter

        response = self.query(qs)
        try:
            zProductRatePlanChargeTiers = response.records
            return zProductRatePlanChargeTiers
        except:
            raise DoesNotExist(
                    "Unable to find Product Rate Plan Charges Tiers for %s"\
                    % product_rate_plan_charge_id)

    def get_camel_converted_products(self, product_id=None, shortcodes=None):
        """
        Converts a product query response into a camel case
        dictionary of products
        """
        response = self.get_products(product_id=product_id,
                                         shortcodes=shortcodes)

        product_dict = {}
        for p in response:
            product_dict[p.Id] = {}
            for attr in p:
                key = convert_camel(attr[0].replace("__c", ""))
                product_dict[p.Id][key] = attr[1]
        return product_dict

    def get_camel_converted_product_rate_plans(self,
                                               product_rate_plan_id=None,
                                               product_id_list=None,
                                               effective_start=None,
                                               effective_end=None):
        """
        Converts a product rate plan query response into a camel case
        dictionary of product rate plans
        """
        # Get Product and optionally filter by ShortCode
        response = self.get_product_rate_plans(
                                    product_rate_plan_id=product_rate_plan_id,
                                    product_id_list=product_id_list,
                                    effective_start=effective_start,
                                    effective_end=effective_end)

        product_rate_plan_dict = {}
        for rp in response:
            # If there is more than one product and rate plan
            if not product_rate_plan_id:
                product_rate_plan_dict[rp.ProductId] = \
                        product_rate_plan_dict.get(rp.ProductId, {})
                product_rate_plan_dict[rp.ProductId][rp.Id] = {}
            for attr in rp:
                key = convert_camel(attr[0].replace("__c", ""))
                # If there is only one product/rate plan
                if product_rate_plan_id:
                    product_rate_plan_dict[key] = str(attr[1])
                # There are potentially multiple products/rate plans
                else:
                    product_rate_plan_dict[rp.ProductId][rp.Id][key] = \
                                                            str(attr[1])
        return product_rate_plan_dict

    def get_camel_converted_product_rate_plan_charges(
                                            self,
                                            product_rate_plan_id=None,
                                            product_rate_plan_id_list=None):
        """
        Converts a product rate plan charge query response into a camel case
        dictionary of product rate plan charges
        """
        # Get Product and optionally filter by ShortCode
        response = self.get_product_rate_plan_charges(
                        product_rate_plan_id=product_rate_plan_id,
                        product_rate_plan_id_list=product_rate_plan_id_list)

        product_rate_plan_charge_dict = {}
        for rpc in response:
            product_rate_plan_charge_dict[rpc.ProductRatePlanId] = \
                product_rate_plan_charge_dict.get(rpc.ProductRatePlanId, {})

            product_rate_plan_charge_dict[rpc.ProductRatePlanId][rpc.Id] = {}
            for attr in rpc:
                key = convert_camel(attr[0].replace("__c", ""))
                product_rate_plan_charge_dict[\
                            rpc.ProductRatePlanId][rpc.Id][key] = str(attr[1])
        return product_rate_plan_charge_dict

    def get_camel_converted_product_rate_plan_charge_tiers(
                                    self,
                                    product_rate_plan_charge_id_list=None):
        """
        Converts a product rate plan charge tier query response into a
        camel case dictionary of product rate plan charge tiers
        """
        # Get Product and optionally filter by ShortCode
        response = self.get_product_rate_plan_charge_tiers(
                                            product_rate_plan_charge_id_list=\
                                            product_rate_plan_charge_id_list)

        product_rate_plan_charge_tier_dict = {}
        for rpct in response:

            product_rate_plan_charge_tier_dict[rpct.ProductRatePlanChargeId] =\
                product_rate_plan_charge_tier_dict.get(
                                rpct.ProductRatePlanChargeId, {})

            product_rate_plan_charge_tier_dict[\
                                rpct.ProductRatePlanChargeId][rpct.Id] = {}
            for attr in rpct:
                key = convert_camel(attr[0].replace("__c", ""))
                product_rate_plan_charge_tier_dict[\
                    rpct.ProductRatePlanChargeId][rpct.Id][key] = str(attr[1])
        return product_rate_plan_charge_tier_dict

    def match_product_rate_plans(self, shortcodes=[], filter_={}):
        """
        Get matching rate plans based on the product list filter.  This method
        will get all rate plans matching products matching the short codes
        in `product_list`.  It will then return a dictionary of rate plans and
        rate plan charges where each rate plan is the highest scoring rate plan
        per unique product and term.

        TODO: Investigate pre-caching to preload entire rate plan system then
        use this method to match and score out of the cached master.

        TODO: Investigate mem-cache into suez (JK: add memcache capability)

        The filter can have the following keys:
            site, gender, age_group, activity_level

        :param list shortcodes: list of short codes to filter the products
        :param dict filter: dictionary of filters to try to match the best
            rate plan against

        :return: dictionary of rate plans and their rate plan charges
        :rtype: dict
        """

        # Defaults
        matching_rate_plans = []
        qs_datetime_now = datetime.utcnow().strftime(SOAP_TIMESTAMP)

        # Get Product and optionally filter by ShortCode
        product_dict = self.get_camel_converted_products(shortcodes=shortcodes)

        product_rate_plan_dict = self.get_camel_converted_product_rate_plans(
                                        product_id_list=product_dict.keys(),
                                        effective_start=qs_datetime_now)

        prp_id_list = []
        # Get all of the product rate plan keys for each product
        for product_id, prp_dict in product_rate_plan_dict.items():
            prp_id_list += prp_dict.keys()

        product_rate_plan_charge_dict = \
                self.get_camel_converted_product_rate_plan_charges(
                                        product_rate_plan_id_list=prp_id_list)

        prpc_id_list = []
        # Get all of the product rate plan charge keys
        # for each product rate plan
        for prp_id, prpc_dict in product_rate_plan_charge_dict.items():
            prpc_id_list += prpc_dict.keys()

        product_rate_plan_charge_tier_dict = \
                    self.get_camel_converted_product_rate_plan_charge_tiers(
                                product_rate_plan_charge_id_list=prpc_id_list)

        # Combine Dictionaries
        for product_id, p_dict in product_dict.items():

            # iterate through rate plans
            rp_list = []
            for rate_plan_id, rp_dict in product_rate_plan_dict\
                                            .get(product_id, {}).items():

                # Scoring for Match: Simple increment if regexp matches
                # ie., if filter = {'site': 'mapmyrun.com'} it will score +1
                # if the custom field RatePlan.Site = 'run' or '(run|ride)'
                priority = rp_dict.get("priority", 0)
                rp_dict["score"] = priority
                if filter_:
                    for field, match in filter_.items():
                        if rp_dict.get(field):
                            p = re.compile(rp_dict[field], re.IGNORECASE)
                            if re.match(p, match):
                                rp_dict["score"] += 1

                # iterate through rate plan charges
                rpc_list = []
                for _, rpc_dict in product_rate_plan_charge_dict\
                                            .get(rate_plan_id, {}).items():

                    # get rate plan charge tiers
                    rpct_list = []
                    for (_, rpct_dict) in product_rate_plan_charge_tier_dict\
                                .get(rpc_dict["id"], {}).items():
                        rpct_list.append(rpct_dict)

                    # append rate plan charge tiers
                    rpc_dict["rate_plan_charge_tiers"] = rpct_list
                    rpc_list.append(rpc_dict)

                # append to rate plan dict after sorting by 'sort_order'
                rp_dict["rate_plan_charges"] = \
                    sorted(rpc_list, key=lambda k: k.get('sort_order', 999))

                # append to rp_list
                rp_list.append(rp_dict)

            # Add to Product Dict but sort by score first
            # TODO: only select highest scoring rate plan per unique term
            p_dict["rate_plans"] = sorted(rp_list,
                                          key=lambda k: k.get('score', 0),
                                          reverse=True)

            matching_rate_plans.append(p_dict)

        # Return Product Rate Plans
        return matching_rate_plans

    def get_product_rate_plan_charge_pricing(self, product_rate_plan_id):
        """
        Gets the Product Rate Plan Charges.
        Sums up the Product Rate Plan Charge Tiers

        :param str product_rate_plan_id: ProductRatePlanID
        """

        products_rate_plan_charge_dict = \
                self.get_camel_converted_product_rate_plan_charges(
                            product_rate_plan_id=product_rate_plan_id)

        # Get the rate plan charges for this specific rate plan
        product_rate_plan_charge_dict = \
                        products_rate_plan_charge_dict[product_rate_plan_id]

        product_rate_plan_charges_tier_dict = \
                    self.get_camel_converted_product_rate_plan_charge_tiers(
                                    product_rate_plan_charge_id_list=\
                                    product_rate_plan_charge_dict.keys())

        # Create the list of rate plan charge tiers
        # within the rate plan charge dict
        for rpc_id, rpct_dict in product_rate_plan_charges_tier_dict.items():
            rate_charge_tiers = product_rate_plan_charge_dict[rpc_id]\
                                .get("rate_charge_tiers", [])
            rate_charge_tiers += rpct_dict.values()
            product_rate_plan_charge_dict[rpc_id]["rate_charge_tiers"] =\
                                                        rate_charge_tiers

        # Run Aggregates
        pricing_dict = {}

        for _, rpc in product_rate_plan_charge_dict.items():
            charge_model = rpc["charge_model"].lower()
            charge_type = rpc["charge_type"].lower()
            pricing_dict[charge_model] = pricing_dict.get(charge_model, {})
            pricing_dict[charge_model][charge_type]\
                = pricing_dict[charge_model].get(charge_type, 0)

            # Iterate through Rate Plan Charge Tiers
            price = pricing_dict[charge_model][charge_type]
            for rpct in rpc["rate_charge_tiers"]:
                is_overage_price = rpct["is_overage_price"]
                if is_overage_price in [False, 'False']:
                    price = price + float(rpct["price"])

            pricing_dict[charge_model][charge_type] = price

        # Run Aggregates
        return pricing_dict

    def get_rate_plans(self, product_rate_plan_id=None, subscription_id=None):
        """
        Gets the RatePlan matching criteria.

        :optparam str product_rate_plan_id: Product Rate Plan ID
        :optparam str subscription_id: Subscription ID
        """

        # Defaults
        qs_filter = []

        if product_rate_plan_id:
            qs_filter.append("ProductRatePlanId = '%s'" % product_rate_plan_id)

        if subscription_id:
            qs_filter.append("SubscriptionId = '%s'" % subscription_id)

        # Build Query
        qs = """
            SELECT
                AmendmentId, AmendmentSubscriptionRatePlanId,
                AmendmentType, CreatedById, CreatedDate, Name,
                ProductRatePlanId, SubscriptionId,
                UpdatedById, UpdatedDate
            FROM RatePlan
            """

        if qs_filter:
            qs += "WHERE %s" % " AND ".join(qs_filter)

        response = self.query(qs)
        zRecords = response.records

        # Return the Match
        return zRecords

    def get_subscriptions(self, subscription_id=None, account_id=None,
                          auto_renew=None, status=None, term_type=None,
                          term_end_date=None, term_start_date=None,
                          subscription_number=None):
        """
        Gets the Subscriptions matching criteria.

        :optparam str subscription_id: Subscription ID
        :optparam str subscription_number: Unique Subscription number
        :optparam str account_id: Account ID
        :optparam bool auto_renew: AutoRenew (True, False)
        :optparam str status: Subscription Status. Allowable values: Draft,
            Pending Activation, Pending Acceptance, Active, Cancelled, Expired
        :optparam str term_type: Allowable values: EVERGREEN, TERMED
        :optparam date term_end_date: This is when the subscription term ends
        :optparam date term_start_date: The date on which the sub term begins
        """

        # Defaults
        qs_filter = []

        if subscription_id:
            qs_filter.append("Id = '%s'" % subscription_id)

        if subscription_number:
            qs_filter.append("Name = '%s'" % subscription_number)

        if account_id:
            qs_filter.append("AccountId = '%s'" % account_id)

        if auto_renew:
            qs_filter.append("AutoRenew = %s" % auto_renew.lower())

        if status:
            qs_filter.append("Status = '%s'" % status)

        if term_type:
            qs_filter.append("TermType = '%s'" % term_type)

        if term_end_date:
            qs_filter.append("TermEndDate = '%s'" % term_end_date)

        if term_start_date:
            qs_filter.append("TermStartDate = '%s'" % term_start_date)

        # Build Query
        qs = """
            SELECT
                AccountId, AutoRenew,
                CancelledDate, ContractAcceptanceDate,
                ContractEffectiveDate,
                CreatedById, CreatedDate, InitialTerm,
                IsInvoiceSeparate, Name, Notes, OriginalCreatedDate,
                OriginalId, PreviousSubscriptionId,
                RenewalTerm, ServiceActivationDate, Status,
                SubscriptionEndDate, SubscriptionStartDate,
                TermEndDate, TermStartDate, TermType,
                UpdatedById, UpdatedDate, Version
            FROM Subscription
            """

        if qs_filter:
            qs += "WHERE %s" % " AND ".join(qs_filter)

        response = self.query(qs)
        zRecords = response.records

        # Return the Match
        return zRecords
    
    def set_default_payment_method_id(self, account_id, payment_method_id,
                                      auto_pay=None):
        # Update the default payment method on the account
        account_dict = {'DefaultPaymentMethodId': payment_method_id}
        if auto_pay == True:
            account_dict['AutoPay'] = True
        elif auto_pay == False:
            account_dict['AutoPay'] = False
        self.update_account(account_id, account_dict)

    def gateway_confirm(self, account, user, gateway_name,
                        payment_method):
        """Switches the gateway if the user is purchasing with a different
           gateway.
           
           Returns True or False if the account already exists or not
        """
        # Make sure the account exists already, otherwise the gateway will be
        # specified on account creation
        if not account or not getattr(account, 'PaymentGateway', None):
            try:
                zAccount = self.get_account(user.id)
            except DoesNotExist:
                logging.info("Gateway: Account DNE. user: %s" % (user.id))
                return False
            logging.info("Gateway: Fetched Account. user: %s" % (user.id))
        else:
            logging.info(
                "Gateway: Account and Gateway existed. user: %s" % (user.id))
            zAccount = account
        
        # If the Payment Gateway still isn't specified, set it and change it
        if not getattr(zAccount, 'PaymentGateway', None):
            if gateway_name:
                update_dict = {'PaymentGateway': gateway_name}
            else:
                update_dict = {'PaymentGateway': self.authorize_gateway}
            logging.info("Gateway: switched user: %s update: %s" \
                         % (user.id, update_dict))
            self.update_account(zAccount.Id, update_dict)
            return True
        
        # If no gateway was specified, and the gateway is set
        # to the default gateway
        if not gateway_name \
            and zAccount.PaymentGateway == self.authorize_gateway:
            # Do nothing
            logging.info("Gateway: same default gateway user: %s gateway: %s" \
                         % (user.id, zAccount.PaymentGateway))
            pass
        # If there isn't a gateway specified, and they aren't set to the
        # default gateway
        elif not gateway_name \
            and zAccount.PaymentGateway != self.authorize_gateway:
            # Update the account to the default gateway
            self.update_account_payment(zAccount.Id,
                                        self.authorize_gateway,
                                        payment_method)
            logging.info("Gateway: switched to default user: %s gateway: %s" \
                         % (user.id, self.authorize_gateway))
        # If a gateway was specified, but their account is already
        # set to that gateway
        elif gateway_name and gateway_name == zAccount.PaymentGateway:
            # Do nothing
            logging.info(
                    "Gateway: same specified gateway user: %s gateway: %s" \
                         % (user.id, gateway_name))
            pass
        # If a gateway was specified, but their account is set to a
        # different gateway
        elif gateway_name and gateway_name != zAccount.PaymentGateway:
            # Update the gateway to the specified gateway
            self.update_account_payment(zAccount.Id,
                                        gateway_name,
                                        payment_method)
            logging.info(
                "Gateway: switched to specified gateway user: %s gateway: %s" \
                         % (user.id, gateway_name))
        # We should never see this condition
        else:
            logging.error(
                "Unexpected gateway conditions. gateway: %s acct_gateway: %s" \
                % (gateway_name, zAccount.PaymentGateway))
        
        return True
    
    def update_account_payment(self, account_id, gateway, payment_method):
        # These steps cannot be combined, and have to be executed in this order
        # Update the account gateway
        logging.info(
            "Gateway: Updating Account Gateway. Account id: %s" % account_id)
        gateway_dict = {'PaymentGateway': gateway}
        self.update_account(account_id, gateway_dict)
        # If the payment method hasn't been created yet
        if payment_method and getattr(payment_method, 'Id', None) is None:
            payment_method.AccountId = account_id
            logging.info(
                "Gateway: Creating Payment Method. Account: %s" % account_id)
            response = self.create(payment_method)
            if not isinstance(response, list) or not response[0].Success:
                raise ZuoraException(
                    "Error creating Payment Method. Account id: %s resp: %s" \
                    % (account_id, response))
            payment_method_id = response[0].Id
        # No Payment Method specified
        elif payment_method is None:
            raise ZuoraException(
                "Missing Payment Method. Account id: %s" % account_id)
        # Payment Method exists already
        else:
            payment_method_id = payment_method.Id
        logging.info(
            "Gateway: Updating DefaultPayment Method. Account id: %s" \
            % account_id)
        # Update the default payment method on the account
        dpm_dict = {'DefaultPaymentMethodId': payment_method_id}
        self.update_account(account_id, dpm_dict)

    def make_account(self, user=None, currency='USD', status="Draft",
                     lazy=False, site_name=None, billing_address=None,
                     gateway_name=None):
        """
        The customer's account. Zuora uses the Account object to track all
        subscriptions, usage, and transactions for a single account to be
        billed. Each account is the source of a recurring invoice stream.
        Each account must capture everything Zuora needs in order to bill and
        collect, including "bill to" addresses, payment method and payment
        method details, payment terms (for example, Net 30), and more.
        A new account must be created before a new subscription can be entered.

        :param str currency: currency, defaults to USD
        :param str status: valid values: Draft, Active, (Canceled)

        :returns: zAccount
        """

        # Check User
        if not user:
            raise MissingRequired("No User Selected.")

        # Get Today
        today = date.today()

        # Build Account
        zAccount = self.client.factory.create('ns2:Account')
        zAccount.AccountNumber = "A-%s" % user["id"]
        zAccount.AllowInvoiceEdit = True
        # Zuora requires AutoPay be false at this point. Can be changed later
        zAccount.AutoPay = False
        zAccount.Batch = 'Batch1'
        zAccount.BillCycleDay = today.day
        zAccount.CrmId = str(user["id"])
        zAccount.Currency = currency
        if billing_address and billing_address["last_name"] != '' and \
           billing_address["first_name"] != '':
            zAccount.Name = "%s, %s"[0:50] % \
                        (billing_address["last_name"],
                         billing_address["first_name"])
        else:
            zAccount.Name = "%s, %s"[0:50] % \
                            (name_underscore_fix(user["last_name"]),
                             name_underscore_fix(user["first_name"]))
        zAccount.PaymentTerm = 'Due Upon Receipt'
        zAccount.Status = status

        # Specify what gateway to use for payments for the user
        if gateway_name:
            zAccount.PaymentGateway = gateway_name
            
        # Determine which Payment Gateway to use, if specified
        elif self.authorize_gateway:
            zAccount.PaymentGateway = self.authorize_gateway

        # If specifying a gateway, the account will be created
        # during the subscribe call
        if lazy or gateway_name:
            return zAccount

        response = self.create(zAccount)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error creating Account. %s" % response)
        zAccount.Id = response[0].Id

        # Return
        return zAccount

    def make_contact(self, user=None, billing_address=None, zAccount=None,
                     lazy=False, gateway_name=None):
        """
        This defines the contact (the end user) for the account. There are two
        types of contacts that need to be created as part of the customer
        account creation: the Bill-To and the Sold-To contacts. Contact
        provides the attributes needed to create these.

        This method creates the contact from the loaded User.

        Uses the billing_address dictionary:
            address1 : str : Address #1
            address2 : str : Address #2
            city : str : City
            country_name : str : Country Name (i.e., United States)
            first_name : str : Person living at Address' First Name
            last_name : str : Person living at Address' Last Name
            postal_code : str : Postal Code
            state : str : Billing Postal Full State Name (i.e., Ohio)

        :returns: zContact
        """

        # Check User / Billing Address
        if not user:
            raise ZuoraException("No User Selected.")

        # Build Contact
        # TODO: remove ns2
        zContact = self.client.factory.create('ns2:Contact')

        if billing_address is not None:
            # Make sure the first and last name are never empty
            zContact.FirstName = name_underscore_fix(
                                                billing_address["first_name"])
            zContact.LastName = name_underscore_fix(
                                                billing_address["last_name"])
            zContact.Address1 = billing_address["street_1"]
            zContact.Address2 = billing_address.get("street_2")
            zContact.City = billing_address["city"]
            zContact.State = billing_address.get("state")
            zContact.PostalCode = billing_address.get("postal_code")
            zContact.Country = billing_address["country_code"]
            if billing_address.get("phone"):
                zContact.HomePhone = billing_address["phone"]
        else:
            zContact.FirstName = name_underscore_fix(user['first_name'])
            zContact.LastName = name_underscore_fix(user['last_name'])

        zContact.PersonalEmail = user["email"]

        if zAccount is not None and hasattr(zAccount, 'Id'):
            zContact.AccountId = zAccount.Id

        # If specifying a gateway, the contact will be created
        # during the subscribe call
        if lazy or gateway_name:
            return zContact

        response = self.create(zContact)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error creating Contact. %s" % response)
        zContact.Id = response[0].Id

        # Return
        return zContact

    def make_payment(self, account_id, invoice_id, invoice_amount,
                     payment_method_id, payment_type='External',
                     payment_status='Processed', effective_date=None,
                     dry_run=False):
        if not effective_date:
            effective_date = date.today().strftime(SOAP_TIMESTAMP)
        else:
            effective_date = effective_date.strftime(SOAP_TIMESTAMP)
        # Create the Payment
        zPayment = self.client.factory.create('ns2:Payment')
        zPayment.AccountId = account_id
        zPayment.InvoiceId = invoice_id
        zPayment.AppliedInvoiceAmount = invoice_amount
        zPayment.PaymentMethodId = payment_method_id
        zPayment.Type = payment_type
        zPayment.Status = payment_status
        zPayment.EffectiveDate = effective_date
        
        # If it's not a dry run, create the payment
        if not dry_run:
            response = self.create(zPayment)
            # If the Payment creation failed
            if not isinstance(response, list) or not response[0].Success:
                logging.error("Error creating Payment, account: %s response: %s" \
                              % (account_id, response))
            else:
                zPayment.Id = response[0].Id
                logging.info("Made Payment. Payment: %s Account: %s" % (
                                zPayment.Id, account_id))
        # else, just output the dry run of the payment data
        else:
            logging.info("Dry run Payment. account: %s Payment: %s" % (account_id, zPayment))

        # Return
        return zPayment

    def make_rate_plan_data(self, product_rate_plan_id):
        """
        RatePlanData is used to pass complex data to the subscribe() call.
        Each RatePlanData identifies one RatePlan object and a list of one
        or more RatePlanChargeData objects.

        :param str product_rate_plan_id: Product Rate Plan ID

        """

        # Build Rate Plan
        zRatePlan = self.client.factory.create('ns0:RatePlan')
        zRatePlan.ProductRatePlanId = product_rate_plan_id

        # Build Rate Plan Data
        zRatePlanData = self.client.factory.create('ns0:RatePlanData')
        zRatePlanData.RatePlan = zRatePlan

        # return Rate Plan Data
        return zRatePlanData

    def make_subscription(self, monthly_term, name=None, notes=None,
                          recurring=True, term_type="TERMED",
                          renewal_term=None, order_id=None,
                          start_date=None):
        """
        This object contains the information needed to create a new
        subscription for the account. It is part of the entire subscribe
        process. The subscribe call is a superset of Subscription.

        A subscription represents a customer signing up for a product for a
        certain amount of time. Each subscription can have one or more
        RatePlans. See Invoking The subscribe() Call for more information
        about creating subscriptions.

        :optparam str name: The name of the subscription. This is a unique\
            identifier. If not specified, Zuora will auto-create a name.
        :param int monthly_term: Term of Subscription (in Months) (12 = 1 Year)
        :optparam str notes: Misc Notes

        :returns: zSubscription
        """

        effective_date = datetime.now().strftime(SOAP_TIMESTAMP)
        if start_date is None:
            start_date = effective_date
        else:
            if not isinstance(start_date, basestring):
                start_date = start_date.strftime(SOAP_TIMESTAMP)

        zSubscription = self.client.factory.create('ns2:Subscription')
        if name:
            zSubscription.Name = name
        if notes:
            zSubscription.Notes = notes

        zSubscription.ContractAcceptanceDate = effective_date
        zSubscription.ContractEffectiveDate = effective_date
        zSubscription.ServiceActivationDate = start_date
        zSubscription.TermStartDate = start_date

        zSubscription.InitialTerm = monthly_term
        # Set RenewalTerm to value explicit value if not None (can be 0)
        if renewal_term is not None:
            zSubscription.RenewalTerm = renewal_term
        # Default to monthly term
        else:
            zSubscription.RenewalTerm = monthly_term
        zSubscription.Status = 'Active'
        zSubscription.AutoRenew = recurring
        zSubscription.TermType = term_type

        return zSubscription

    def remove_product_amendment(self, subscription_id, rate_plan_id):
        """
        Use Amendment to make changes to a subscription. For example, if you
        wish to change the terms and conditions of a subscription, you would
        use an Amendment.

        :param str subscription_id: The identification number for the\
            subscription that is being amended.
        :param str rate_plan_id: RatePlanID

        :returns: response
        """
        effective_date = datetime.now().strftime(SOAP_TIMESTAMP)

        # Create the product amendment removal
        zAmendment = self.create_product_amendment(
                                    effective_date,
                                    subscription_id,
                                    name_prepend="Remove Product Amendment",
                                    amendment_type='RemoveProduct')

        # Make Rate Plan
        zRatePlan = self.client.factory.create('ns0:RatePlan')
        zRatePlan.AmendmentType = "RemoveProduct"
        zRatePlan.AmendmentId = zAmendment.Id
        zRatePlan.AmendmentSubscriptionRatePlanId = rate_plan_id
        response = self.create(zRatePlan)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error creating RatePlan. %s" % response)

        # Update the product amendment
        response = self.update_product_amendment(effective_date, zAmendment)

        return response

    def subscribe(self, product_rate_plan_id, monthly_term, zAccount=None,
                  zContact=None, zShippingContact=None,
                  process_payments_flag=True,
                  generate_invoice_flag=True, generate_preview=False,
                  term_type="TERMED", renewal_term=None,
                  account_name=None, subscription_name=None,
                  recurring=True, payment_method=None, order_id=None,
                  user=None, billing_address=None, shipping_address=None,
                  start_date=None, site_name=None,
                  discount_product_rate_plan_id=None,
                  external_payment_method=None, gateway_name=None):
        """
        The subscribe() call bundles the information required to create one
        or more new subscriptions. This is a combined call that you can use
        to perform all of the following tasks in a single call.
            - Create accounts
            - Create contacts
            - Create payment methods
            - Apply the first payment to a subscription

        :param str product_rate_plan_id: Product Rate Plan to subscribe to
        :param int monthly_term: Number of Months Subscription Term
        :param bool generate_invoice_flag: Specifies whether an invoice is to\
            be generated when the subscription is created. If a value is not\
            specified, this defaults to true, which gens and posts an invoice.
        :param bool process_payments_flag: Specifies whether payment should\
            be applied when the subscription is created
        :param str account_name: This is the name of the account.
        :param str subscription_name: The name of the subscription. This is a\
            unique identifier. If not specified, Zuora will auto-create a name.
        """
        if user:
            logging.info("Gateway: confirming gateway user: %s" % (user.id))
            # Get the payment method
            if external_payment_method:
                gateway_pm = external_payment_method
            else:
                gateway_pm = payment_method
            # Account Gateway Check/Switch
            existing_account = self.gateway_confirm(
                            zAccount,
                            user,
                            gateway_name,
                            gateway_pm)
        else:
            existing_account = False
        
        # Get or Create Account
        if not zAccount:
            zAccount = self.make_account(user=user, site_name=site_name,
                                         billing_address=billing_address,
                                         gateway_name=gateway_name)

        if not zContact:
            # Create Contact
            zContact = self.make_contact(user=user,
                                         billing_address=billing_address,
                                         zAccount=zAccount,
                                         gateway_name=gateway_name)
        
        # Add the shipping contact if it exists
        if not zShippingContact and shipping_address:
            zShippingContact = self.make_contact(user=user,
                                         billing_address=shipping_address,
                                         zAccount=zAccount,
                                         gateway_name=gateway_name)
        
        # Get Rate Plan & Build Rate Plan Data
        zRatePlanData = self.make_rate_plan_data(product_rate_plan_id)

        if discount_product_rate_plan_id:
            zDiscountRatePlanData = self.make_rate_plan_data(discount_product_rate_plan_id)
        else:
            zDiscountRatePlanData = None

        # Create Subscription
        zSubscription = self.make_subscription(monthly_term=monthly_term,
                                               recurring=recurring,
                                               order_id=order_id,
                                               start_date=start_date)

        # Attach additional Options
        zSubscriptionOptions = self.client.factory\
                                    .create("ns0:SubscribeOptions")
        zSubscriptionOptions.GenerateInvoice = generate_invoice_flag
        zSubscriptionOptions.ProcessPayments = process_payments_flag
        
        # Attach SubscribeInvoiceProcessingOptions
        SubscribeInvoiceProcessingOptions = self.client.factory\
                            .create("ns0:SubscribeInvoiceProcessingOptions")
        SubscribeInvoiceProcessingOptions.InvoiceTargetDate = \
                                datetime.now().strftime(SOAP_TIMESTAMP)
        SubscribeInvoiceProcessingOptions.InvoiceProcessingScope = \
                                                                "Subscription"
        zSubscriptionOptions.SubscribeInvoiceProcessingOptions = \
                                            SubscribeInvoiceProcessingOptions
        
        log.info("***external_payment_method: %s" % external_payment_method)
        if external_payment_method:
            product_rate_plan_charges = self.get_product_rate_plan_charges(
                                    product_rate_plan_id=product_rate_plan_id)
            product_rate_plan_charge_tiers = \
                self.get_product_rate_plan_charge_tiers(
                product_rate_plan_charge_id=product_rate_plan_charges[0].Id)
            zExternalPaymentOptions = self.client.factory\
                                    .create("ns0:ExternalPaymentOptions")
            zExternalPaymentOptions.PaymentMethodId = \
                                                external_payment_method.Id
            zExternalPaymentOptions.Amount = \
                                    product_rate_plan_charge_tiers[0].Price
            zExternalPaymentOptions.EffectiveDate = datetime.now().strftime(
                                                            SOAP_TIMESTAMP)
            zSubscriptionOptions.ExternalPaymentOptions = \
                                                zExternalPaymentOptions

        # Subscription Data
        zSubscriptionData = self.client.factory.create('ns0:SubscriptionData')
        zSubscriptionData.Subscription = zSubscription
        
        # Apply the discount rate plan if it exists
        if zDiscountRatePlanData:
            zSubscriptionData.RatePlanData = [zRatePlanData, zDiscountRatePlanData]
        else:
            zSubscriptionData.RatePlanData = zRatePlanData

        # Subscribe
        zSubscribeRequest = self.client.factory.create('ns0:SubscribeRequest')
        # If the account already exists, just add the id to the
        # subscribe request
        if existing_account:
            zSubscribeRequest.Account = self.get_account(user.id, id_only=True)
            logging.info("Fetched just the account id, user: %s" % (user.id))
        else:
            zSubscribeRequest.Account = zAccount
        zSubscribeRequest.BillToContact = zContact
        # Add the shipping contact if it exists
        if zShippingContact:
            zSubscribeRequest.SoldToContact = zShippingContact
        # Otherwise default to the billing contact
        else:
            zSubscribeRequest.SoldToContact = zSubscribeRequest.BillToContact
        zSubscribeRequest.SubscriptionData = zSubscriptionData
        zSubscribeRequest.SubscribeOptions = zSubscriptionOptions

        zSubscribeRequest.PaymentMethod = payment_method

        # If Preview
        if generate_preview:
            zPreviewOptions = self.client.factory\
                                    .create("ns0:PreviewOptions")
            zPreviewOptions.EnablePreviewMode = True
            zPreviewOptions.NumberOfPeriods = monthly_term + 3
            zSubscribeRequest.PreviewOptions = zPreviewOptions

        fn = self.client.service.subscribe
        log.info("***Subscribe Request: %s" % zSubscribeRequest)
        response = self.call(fn, zSubscribeRequest)
        log.info("***Subscribe Response: %s" % response)
        
        # If the gateway is paypal, make sure AutoPay is set to True
        if gateway_name and 'paypal' in gateway_name.lower():
            if isinstance(response, list):
                SubscribeResponse = response[0]
            else:
                SubscribeResponse = response
            self.update_account(SubscribeResponse.AccountId, {'AutoPay': True})

        # return the response
        return response

    def update_account(self, account_id, update_dict):
        """
        Update a zAccount record

        :param str account_id: ID of the Account
        :param dict update_dict: Dictionary of Property:Value pairs
        """
        # Now Update the Draft Account to be Active
        zAccountUpdate = self.client.factory.create('ns2:Account')
        zAccountUpdate.Id = account_id
        for k, v in update_dict.items():
            setattr(zAccountUpdate, k, v)
        response = self.update(zAccountUpdate)
        if not isinstance(response, list) or not response[0].Success:
            raise ZuoraException(
                "Unknown Error updating Account. %s" % response)


# helper lib
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def convert_camel(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def zuora_serialize(obj):
    """
    Converts a SUDS Object to a Dictionary
    - Very primative serializer but is able to handle
      the basic Zuora SOAP Objects.
    """
    basic_serializer = [str, int, float, unicode, date, datetime, long]

    if not obj:
        return None

    if isinstance(obj, list):
        obj_list = []
        for item in obj:
            obj_list.append(zuora_serialize(item))
        return obj_list
    else:
        obj_dict = {}
        for attr in obj:
            key = convert_camel(attr[0].replace("__c", ""))

            is_allowed = False
            for allowed in basic_serializer:
                if isinstance(attr[1], allowed):
                    is_allowed = True
            if is_allowed:
                obj_dict[key] = attr[1]
            else:
                obj_dict[key] = zuora_serialize(attr[1])
        return obj_dict


def zuora_serialize_list(response_list):
    """
    Serialize a list of Zuora objects
    """
    serialized_list = []
    if response_list:
        for item in response_list:
            serialized_list.append(zuora_serialize(item))
    return serialized_list


def name_underscore_fix(name_field):
    """
    Make sure the name field has a value, otherwise return an underscore
    """
    if name_field and name_field.strip() != '':
        return name_field
    return '_'
