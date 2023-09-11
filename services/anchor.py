import logging
import random
from decimal import Decimal

import requests

logger = logging.getLogger(__name__)


class AnchorClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()

    def create_customer(  # noqa: PLR0913
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        address: str,
        city: str,
        postal_code: int,
        state: str,
    ) -> dict:
        response = self.session.post(
            url=f'{self.base_url}/api/v1/customers',
            headers={'x-anchor-key': self.api_key},
            json={
                'data': {
                    'type': 'IndividualCustomer',
                    'attributes': {
                        'fullName': {'firstName': first_name, 'lastName': last_name},
                        'email': email,
                        'phoneNumber': phone_number,
                        'address': {
                            'addressLine_1': address,
                            'country': 'NG',
                            'city': city,
                            'postalCode': postal_code,
                            'state': state,
                        },
                    },
                },
            },
        )
        if not response.ok:
            logging.warning(f'Error occurred while fetching {response.url} with error {response.json()}')
            response.raise_for_status()

        return response.json()

    def create_deposit_account(self, customer_id: str):
        response = self.session.post(
            url=f'{self.base_url}/api/v1/accounts',
            headers={'x-anchor-key': self.api_key},
            json={
                'data': {
                    'type': 'DepositAccount',
                    'attributes': {'productName': 'SAVINGS'},
                    'relationships': {'customer': {'data': {'id': customer_id, 'type': 'IndividualCustomer'}}},
                },
            },
        )
        if not response.ok:
            logging.warning(f'Error occurred while fetching {response.url} with error {response.json()}')
            response.raise_for_status()

        return response.json()

    def verify_kyc(self, customer_id: str, gender: str):
        bvn = str(random.randint(10000000000, 99999999999))
        dob = '2000-12-24'

        response = self.session.post(
            url=f'{self.base_url}/api/v1/customers/{customer_id}/verification/individual',
            headers={'x-anchor-key': self.api_key},
            json={
                'data': {
                    'type': 'Verification',
                    'attributes': {'level': 'TIER_2', 'level2': {'bvn': bvn, 'dateOfBirth': dob, 'gender': gender}},
                },
            },
        )
        if not response.ok:
            logging.warning(f'Error occurred while fetching {response.url} with error {response.json()}')
            response.raise_for_status()

        return response.json()

    def create_counterparty(self, account_name: str, account_number: int, bank_id: str, bank_code: str):
        response = self.session.post(
            url=f'{self.base_url}/api/v1/counterparties',
            headers={'x-anchor-key': self.api_key},
            json={
                'data': {
                    'type': 'CounterParty',
                    'attributes': {
                        'accountName': account_name,
                        'accountNumber': account_number,
                        'bankCode': bank_code,
                        'verifyName': True,
                    },
                    'relationships': {
                        'bank': {
                            'data': {
                                'id': bank_id,
                                'type': 'Bank',
                            },
                        },
                    },
                },
            },
        )

        response.raise_for_status()
        return response.json()

    def initiate_transfer(self, amount: Decimal, reason: str, counterparty_id: str, account_id: str):
        response = self.session.post(
            url=f'{self.base_url}/api/v1/transfers',
            headers={'x-anchor-key': self.api_key},
            json={
                'data': {
                    'type': 'NIPTransfer',
                    'attributes': {'amount': int(amount * 100), 'currency': 'NGN', 'reason': reason},
                    'relationships': {
                        'counterParty': {
                            'data': {
                                'id': counterparty_id,
                                'type': 'CounterParty',
                            },
                        },
                        'account': {'data': {'id': account_id, 'type': 'DepositAccount'}},
                    },
                },
            },
        )
        if not response.ok:
            logging.warning(f'Error occurred while fetching {response.url} with error {response.json()}')
            response.raise_for_status()

        return response.json()

    def get_banks(self):
        response = self.session.get(
            url=f'{self.base_url}/api/v1/banks',
            headers={'x-anchor-key': self.api_key},
        )
        if not response.ok:
            logging.warning(f'Error occurred while fetching {response.url} with error {response.json()}')
            response.raise_for_status()

        return response.json()

    def get_deposit_account_balance(self, deposit_account_id: str):
        response = self.session.get(
            url=f'{self.base_url}/api/v1/accounts/balance/{deposit_account_id}',
            headers={'x-anchor-key': self.api_key},
        )
        if not response.ok:
            logging.warning(f'Error occurred while fetching {response.url} with error {response.json()}')
            response.raise_for_status()

        return response.json()

    def get_deposit_account(self, deposit_account_id: str):
        response = self.session.get(
            url=f'{self.base_url}/api/v1/accounts/{deposit_account_id}?include=VirtualNuban',
            headers={'x-anchor-key': self.api_key},
        )
        if not response.ok:
            logging.warning(f'Error occurred while fetching {response.url} with error {response.json()}')
            response.raise_for_status()

        return response.json()

    def verify_account(self, account_number: str, bank_code: str):
        response = self.session.get(
            url=f'{self.base_url}/api/v1/payments/verify-account/{bank_code}/{account_number}',
            headers={'x-anchor-key': self.api_key},
        )
        if not response.ok:
            logging.warning(f'Error occurred while fetching {response.url} with error {response.json()}')
            response.raise_for_status()

        return response.json()
