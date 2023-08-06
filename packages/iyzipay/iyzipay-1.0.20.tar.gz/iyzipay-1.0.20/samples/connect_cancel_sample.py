# coding=utf-8
import unittest
import iyzipay


class ConnectCancelSample(unittest.TestCase):
    def runTest(self):
        self.should_cancel_payment()

    def should_cancel_payment(self):

        options = dict([('base_url', iyzipay.base_url)])
        options['api_key'] = iyzipay.api_key
        options['secret_key'] = iyzipay.secret_key

        request = dict([('locale', 'tr')])
        request['conversationId'] = '123456'
        request['paymentId'] = '1'
        request['ip'] = '85.34.78.112'

        # make request
        cancel = iyzipay.ConnectCancel()
        cancel_response = cancel.create(request, options)

        # print response
        print(cancel_response.read().decode('utf-8'))

