import logging
from decimal import Decimal
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)


class AnchorClient:
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()

    def _make_request(self, method, url, data=None, params=None) -> Optional[dict[str, Any]]:
        headers = {'x-anchor-key': self.api_key}
        try:
            response = self.session.request(
                json=data,
                method=method,
                params=params,
                headers=headers,
                url=url,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.exception(f'Error occurred while making request to {url} with error {e.response.json()}')
            return None

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
    ) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/customers'
        data = {
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
        }
        return self._make_request('POST', url, data)

    def delete_customer(self, customer_id: str) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/customers/{customer_id}'
        return self._make_request('DELETE', url)

    def create_deposit_account(self, customer_id: str) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/accounts'
        data = {
            'data': {
                'type': 'DepositAccount',
                'attributes': {'productName': 'SAVINGS'},
                'relationships': {'customer': {'data': {'id': customer_id, 'type': 'IndividualCustomer'}}},
            },
        }
        return self._make_request('POST', url, data)

    def kyc_tier_two_verification(self, customer_id: str, gender: str, bvn: str, dob: str) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/customers/{customer_id}/verification/individual'
        data = {
            'data': {
                'type': 'Verification',
                'attributes': {'level': 'TIER_2', 'level2': {'bvn': bvn, 'dateOfBirth': dob, 'gender': gender}},
            },
        }
        return self._make_request('POST', url, data)

    def kyc_tier_three_verification(
        self,
        customer_id: str,
        id_number: str,
        id_type: str,
        id_expiry_date: str,
    ) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/customers/{customer_id}/verification/individual'
        data = {
            'data': {
                'type': 'Verification',
                'attributes': {
                    'level': 'TIER_3',
                    'level3': {'idNumber': id_number, 'idType': id_type, 'expiryDate': id_expiry_date},
                },
            },
        }
        return self._make_request('POST', url, data)

    def create_counterparty(
        self,
        account_name: str,
        account_number: str,
        bank_id: str,
        bank_code: str,
    ) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/counterparties'
        data = {
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
        }
        return self._make_request('POST', url, data)

    def initiate_transfer(
        self,
        amount: Decimal,
        reason: str,
        counterparty_id: str,
        account_id: str,
    ) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/transfers'
        data = {
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
        }
        return self._make_request('POST', url, data)

    def get_banks(self) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/banks'
        return self._make_request('GET', url)

    def get_deposit_account_balance(self, deposit_account_id: str) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/accounts/balance/{deposit_account_id}'
        return self._make_request('GET', url)

    def get_deposit_account(self, deposit_account_id: str) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/accounts/{deposit_account_id}'
        return self._make_request('GET', url, params={'include': 'VirtualNuban'})

    def verify_account(self, account_number: str, bank_code: str) -> Optional[dict[str, Any]]:
        url = f'{self.base_url}/api/v1/payments/verify-account/{bank_code}/{account_number}'
        return self._make_request('GET', url)
