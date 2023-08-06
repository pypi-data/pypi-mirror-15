# coding=utf-8
import unittest
import iyzipay


class InstallmentSample(unittest.TestCase):
    def runTest(self):
        self.should_retrieve_installment_info()
        self.should_retrieve_installment_info_for_all_banks()

    def should_retrieve_installment_info(self):

        options = dict([('base_url', iyzipay.base_url)])
        options['api_key'] = iyzipay.api_key
        options['secret_key'] = iyzipay.secret_key

        request = dict([('locale', 'tr')])
        request['conversationId'] = '123456789'
        request['binNumber'] = '454671'
        request['price'] = '1'

        # make request
        installment_info = iyzipay.InstallmentInfo()
        installment_info_response = installment_info.retrieve(request, options)

        # print response
        print(installment_info_response.read().decode('utf-8'))

    def should_retrieve_installment_info_for_all_banks(self):

        options = dict([('base_url', iyzipay.base_url)])
        options['api_key'] = iyzipay.api_key
        options['secret_key'] = iyzipay.secret_key

        request = dict([('locale', 'tr')])
        request['conversationId'] = '123456789'
        request['price'] = '1'

        # make request
        installment_info = iyzipay.InstallmentInfo()
        installment_info_response = installment_info.retrieve(request, options)

        # print response
        print(installment_info_response.read().decode('utf-8'))
