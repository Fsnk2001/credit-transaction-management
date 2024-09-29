import concurrent
from concurrent.futures import ThreadPoolExecutor

from rest_framework.test import APITestCase

from apps.users.models import UserRoles, User, PhoneNumber
from apps.credits.models import TransactionType, StatusType


def run_concurrent_thread(method, iteration, workers, **kwargs):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for _ in range(iteration):
            futures.append(executor.submit(method, **kwargs, ))
        for future in concurrent.futures.as_completed(futures):
            message = future.result()
            if message is not None:
                pass


class CreditTransactionTestCase(APITestCase):
    DEPOSIT_URL = '/api/credits/deposits/'
    TRANSFER_URL = '/api/credits/transfers/'
    TRANSACTION_URL = '/api/credits/transactions/'

    def setUp(self):
        self.set_up_admin()
        self.set_up_sellers()
        self.set_up_phone_number()

        self.num_deposits = 10
        self.num_transfers = 60
        self.deposit_amount = 100000
        self.transfer_amount = 5000

    def set_up_admin(self):
        self.admin = User.objects.create_user(username='admin', password='password')
        self.admin.add_role(UserRoles.ADMIN)

    def set_up_sellers(self):
        self.seller1 = User.objects.create_user(username='seller1', password='password')
        self.seller2 = User.objects.create_user(username='seller2', password='password')

        self.seller1.add_role(UserRoles.SELLER)
        self.seller2.add_role(UserRoles.SELLER)

    def set_up_phone_number(self):
        self.phone_number = PhoneNumber.objects.create(number="09123456789")

    def deposit_credits(self, user):
        url = self.DEPOSIT_URL
        self.client.force_authenticate(user=user)
        self.client.post(url, {
            'amount': self.deposit_amount,
        }, format='json')

    def get_my_deposits(self, user):
        url = f"{self.DEPOSIT_URL}me/"
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        return response.data.get('data', {}).get('deposits', [])

    def get_pending_deposits(self, user):
        deposits = self.get_my_deposits(user)
        pending_deposits = []
        for deposit in deposits:
            if deposit['status'] == StatusType.PENDING:
                pending_deposits.append(deposit)
        return pending_deposits

    def approve_deposit(self, deposit: dict):
        url = f"{self.DEPOSIT_URL}{deposit['id']}/approve/"
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, {
            'is_approved': True
        }, format='json')
        return response

    def transfer_credits(self, user):
        url = self.TRANSFER_URL
        self.client.force_authenticate(user=user)
        self.client.post(url, {
            'phone_number': self.phone_number.id,
            'amount': self.transfer_amount,
        }, format='json')

    def get_my_transactions(self, user):
        url = f"{self.TRANSACTION_URL}me/"
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        return response.data.get('data', {}).get('transactions', [])

    def calculate_balance_based_on_transactions(self, user):
        transaction_logs = self.get_my_transactions(user)
        deposit_amount = 0
        transfer_amount = 0
        for transaction_log in transaction_logs:
            if transaction_log['transaction_type'] == TransactionType.DEPOSIT:
                deposit_amount += transaction_log['amount']
            elif transaction_log['transaction_type'] == TransactionType.TRANSFER:
                deposit_amount -= transaction_log['amount']
        current_balance = deposit_amount - transfer_amount
        return current_balance

    def test_credit_transaction_operations(self):
        for _ in range(self.num_deposits):
            self.deposit_credits(self.seller1)

        pending_deposits = self.get_pending_deposits(self.seller1)
        for deposit in pending_deposits:
            self.approve_deposit(deposit)

        for _ in range(self.num_transfers):
            self.transfer_credits(self.seller1)

        self.seller1.refresh_from_db()
        expected_balance = self.calculate_balance_based_on_transactions(self.seller1)

        self.assertEqual(self.seller1.balance, expected_balance)

    # def test_parallel_credit_transaction_operations(self):
    #     run_concurrent_thread(
    #         method=self.deposit_credits, iteration=self.num_deposits, workers=10, user=self.seller1
    #     )
    #
    #     pending_deposits = self.get_pending_deposits(self.seller1)
    #     for deposit in pending_deposits:
    #         self.approve_deposit(deposit)
    #
    #     run_concurrent_thread(
    #         method=self.transfer_credits, iteration=self.num_transfers, workers=10, user=self.seller1
    #     )
    #
    #     self.seller1.refresh_from_db()
    #     expected_balance = self.calculate_balance_based_on_transactions(self.seller1)
    #
    #     self.assertEqual(self.seller1.balance, expected_balance)
