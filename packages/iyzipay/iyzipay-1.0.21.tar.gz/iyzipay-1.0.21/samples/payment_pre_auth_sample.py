# coding=utf-8
import unittest
import iyzipay


class PaymentPreAuthSample(unittest.TestCase):
    def runTest(self):
        self.should_create_payment_with_physical_and_virtual_item_for_standard_merchant()
        self.should_create_payment_with_physical_and_virtual_item_for_market_place()
        self.should_create_payment_with_physical_and_virtual_item_for_listing_or_subscription()
        self.should_retrieve_payment()

    def should_create_payment_with_physical_and_virtual_item_for_standard_merchant(self):
        options = dict([('base_url', iyzipay.base_url)])
        options['api_key'] = iyzipay.api_key
        options['secret_key'] = iyzipay.secret_key

        request = dict([('locale', 'tr')])
        request['conversationId'] = '123456789'
        request['price'] = '1'
        request['paidPrice'] = '1.1'
        request['installment'] = '1'
        request['basketId'] = 'B67832'
        request['paymentChannel'] = 'WEB'
        request['paymentGroup'] = 'PRODUCT'
        request['callbackUrl'] = 'https://www.merchant.com/callback'
        request['currency'] = 'TRY'

        payment_card = dict([('cardHolderName', 'John Doe')])
        payment_card['cardNumber'] = '5528790000000008'
        payment_card['expireMonth'] = '12'
        payment_card['expireYear'] = '2030'
        payment_card['cvc'] = '123'
        payment_card['registerCard'] = '0'
        request['paymentCard'] = payment_card

        buyer = dict([('id', 'BY789')])
        buyer['name'] = 'John'
        buyer['surname'] = 'Doe'
        buyer['gsmNumber'] = '+905350000000'
        buyer['email'] = 'email@email.com'
        buyer['identityNumber'] = '74300864791'
        buyer['lastLoginDate'] = '2015-10-05 12:43:35'
        buyer['registrationDate'] = '2013-04-21 15:12:09'
        buyer['registrationAddress'] = 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1'
        buyer['ip'] = '85.34.78.112'
        buyer['city'] = 'Istanbul'
        buyer['country'] = 'Turkey'
        buyer['zipCode'] = '34732'
        request['buyer'] = buyer

        address = dict([('address', 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1')])
        address['zipCode'] = '34732'
        address['contactName'] = 'Jane Doe'
        address['city'] = 'Istanbul'
        address['country'] = 'Turkey'
        request['shippingAddress'] = address
        request['billingAddress'] = address

        basket_items = []
        basket_item_first = dict([('id', 'BI101')])
        basket_item_first['name'] = 'Binocular'
        basket_item_first['category1'] = 'Collectibles'
        basket_item_first['category2'] = 'Accessories'
        basket_item_first['itemType'] = 'PHYSICAL'
        basket_item_first['price'] = '0.3'
        basket_items.append(basket_item_first)

        basket_item_second = dict([('id', 'BI102')])
        basket_item_second['name'] = 'Game code'
        basket_item_second['category1'] = 'Game'
        basket_item_second['category2'] = 'Online Game Items'
        basket_item_second['itemType'] = 'VIRTUAL'
        basket_item_second['price'] = '0.5'
        basket_items.append(basket_item_second)

        basket_item_third = dict([('id', 'BI103')])
        basket_item_third['name'] = 'Usb'
        basket_item_third['category1'] = 'Electronics'
        basket_item_third['category2'] = 'Usb / Cable'
        basket_item_third['itemType'] = 'PHYSICAL'
        basket_item_third['price'] = '0.2'
        basket_items.append(basket_item_third)

        request['basketItems'] = basket_items

        # make request
        payment_pre_auth = iyzipay.PaymentPreAuth()
        payment_pre_auth_response = payment_pre_auth.create(request, options)

        # get and print response
        print(payment_pre_auth_response.read().decode('utf-8'))

    def should_create_payment_with_physical_and_virtual_item_for_market_place(self):
        options = dict([('base_url', iyzipay.base_url)])
        options['api_key'] = iyzipay.api_key
        options['secret_key'] = iyzipay.secret_key

        request = dict([('locale', 'tr')])
        request['conversationId'] = '123456789'
        request['price'] = '1'
        request['paidPrice'] = '1.1'
        request['installment'] = '1'
        request['basketId'] = 'B67832'
        request['paymentChannel'] = 'WEB'
        request['paymentGroup'] = 'PRODUCT'
        request['callbackUrl'] = 'https://www.merchant.com/callback'
        request['currency'] = 'TRY'

        payment_card = dict([('cardHolderName', 'John Doe')])
        payment_card['cardNumber'] = '5528790000000008'
        payment_card['expireMonth'] = '12'
        payment_card['expireYear'] = '2030'
        payment_card['cvc'] = '123'
        payment_card['registerCard'] = '0'
        request['paymentCard'] = payment_card

        buyer = dict([('id', 'BY789')])
        buyer['name'] = 'John'
        buyer['surname'] = 'Doe'
        buyer['gsmNumber'] = '+905350000000'
        buyer['email'] = 'email@email.com'
        buyer['identityNumber'] = '74300864791'
        buyer['lastLoginDate'] = '2015-10-05 12:43:35'
        buyer['registrationDate'] = '2013-04-21 15:12:09'
        buyer['registrationAddress'] = 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1'
        buyer['ip'] = '85.34.78.112'
        buyer['city'] = 'Istanbul'
        buyer['country'] = 'Turkey'
        buyer['zipCode'] = '34732'
        request['buyer'] = buyer

        address = dict([('address', 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1')])
        address['zipCode'] = '34732'
        address['contactName'] = 'Jane Doe'
        address['city'] = 'Istanbul'
        address['country'] = 'Turkey'
        request['shippingAddress'] = address
        request['billingAddress'] = address

        basket_items = []
        basket_item_first = dict([('id', 'BI101')])
        basket_item_first['name'] = 'Binocular'
        basket_item_first['category1'] = 'Collectibles'
        basket_item_first['category2'] = 'Accessories'
        basket_item_first['itemType'] = 'PHYSICAL'
        basket_item_first['price'] = '0.3'
        basket_item_first['subMerchantKey'] = 'sub merchant key'
        basket_item_first['subMerchantPrice'] = '0.27'
        basket_items.append(basket_item_first)

        basket_item_second = dict([('id', 'BI102')])
        basket_item_second['name'] = 'Game code'
        basket_item_second['category1'] = 'Game'
        basket_item_second['category2'] = 'Online Game Items'
        basket_item_second['itemType'] = 'VIRTUAL'
        basket_item_second['price'] = '0.5'
        basket_item_second['subMerchantKey'] = 'sub merchant key'
        basket_item_second['subMerchantPrice'] = '0.42'
        basket_items.append(basket_item_second)

        basket_item_third = dict([('id', 'BI103')])
        basket_item_third['name'] = 'Usb'
        basket_item_third['category1'] = 'Electronics'
        basket_item_third['category2'] = 'Usb / Cable'
        basket_item_third['itemType'] = 'PHYSICAL'
        basket_item_third['price'] = '0.2'
        basket_item_third['subMerchantKey'] = 'sub merchant key'
        basket_item_third['subMerchantPrice'] = '0.18'
        basket_items.append(basket_item_third)

        request['basketItems'] = basket_items

        # make request
        payment_pre_auth = iyzipay.PaymentPreAuth()
        payment_pre_auth_response = payment_pre_auth.create(request, options)

        # get and print response
        print(payment_pre_auth_response.read().decode('utf-8'))

    def should_create_payment_with_physical_and_virtual_item_for_listing_or_subscription(self):
        options = dict([('base_url', iyzipay.base_url)])
        options['api_key'] = iyzipay.api_key
        options['secret_key'] = iyzipay.secret_key

        request = dict([('locale', 'tr')])
        request['conversationId'] = '123456789'
        request['price'] = '1'
        request['paidPrice'] = '1.1'
        request['installment'] = '1'
        request['basketId'] = 'B67832'
        request['paymentChannel'] = 'WEB'
        request['paymentGroup'] = 'SUBSCRIPTION'
        request['callbackUrl'] = 'https://www.merchant.com/callback'
        request['currency'] = 'TRY'

        payment_card = dict([('cardHolderName', 'John Doe')])
        payment_card['cardNumber'] = '5528790000000008'
        payment_card['expireMonth'] = '12'
        payment_card['expireYear'] = '2030'
        payment_card['cvc'] = '123'
        payment_card['registerCard'] = '0'
        request['paymentCard'] = payment_card

        buyer = dict([('id', 'BY789')])
        buyer['name'] = 'John'
        buyer['surname'] = 'Doe'
        buyer['gsmNumber'] = '+905350000000'
        buyer['email'] = 'email@email.com'
        buyer['identityNumber'] = '74300864791'
        buyer['lastLoginDate'] = '2015-10-05 12:43:35'
        buyer['registrationDate'] = '2013-04-21 15:12:09'
        buyer['registrationAddress'] = 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1'
        buyer['ip'] = '85.34.78.112'
        buyer['city'] = 'Istanbul'
        buyer['country'] = 'Turkey'
        buyer['zipCode'] = '34732'
        request['buyer'] = buyer

        address = dict([('address', 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1')])
        address['zipCode'] = '34732'
        address['contactName'] = 'Jane Doe'
        address['city'] = 'Istanbul'
        address['country'] = 'Turkey'
        request['shippingAddress'] = address
        request['billingAddress'] = address

        basket_items = []
        basket_item_first = dict([('id', 'BI101')])
        basket_item_first['name'] = 'Binocular'
        basket_item_first['category1'] = 'Collectibles'
        basket_item_first['category2'] = 'Accessories'
        basket_item_first['itemType'] = 'PHYSICAL'
        basket_item_first['price'] = '0.3'
        basket_items.append(basket_item_first)

        basket_item_second = dict([('id', 'BI102')])
        basket_item_second['name'] = 'Game code'
        basket_item_second['category1'] = 'Game'
        basket_item_second['category2'] = 'Online Game Items'
        basket_item_second['itemType'] = 'VIRTUAL'
        basket_item_second['price'] = '0.5'
        basket_items.append(basket_item_second)

        basket_item_third = dict([('id', 'BI103')])
        basket_item_third['name'] = 'Usb'
        basket_item_third['category1'] = 'Electronics'
        basket_item_third['category2'] = 'Usb / Cable'
        basket_item_third['itemType'] = 'PHYSICAL'
        basket_item_third['price'] = '0.2'
        basket_items.append(basket_item_third)

        request['basketItems'] = basket_items

        # make request
        payment_pre_auth = iyzipay.PaymentPreAuth()
        payment_pre_auth_response = payment_pre_auth.create(request, options)

        # get and print response
        print(payment_pre_auth_response.read().decode('utf-8'))

    def should_retrieve_payment(self):
        options = dict([('base_url', iyzipay.base_url)])
        options['api_key'] = iyzipay.api_key
        options['secret_key'] = iyzipay.secret_key

        request = dict([('locale', 'tr')])
        request['conversationId'] = '123456789'
        request['paymentId'] = '1'
        request['paymentConversationId'] = '123456789'

        # make request
        payment_pre_auth = iyzipay.PaymentPreAuth()
        payment_pre_auth_response = payment_pre_auth.retrieve(request, options)

        # print response
        print(payment_pre_auth_response.read().decode('utf-8'))
