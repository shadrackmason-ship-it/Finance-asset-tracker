from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from .models import Asset, Transaction, TradeJournal, Watchlist


def make_user(username='testuser', password='TestPass123!'):
    return User.objects.create_user(username=username, password=password, email=f'{username}@test.com')


def get_jwt(client, username='testuser', password='TestPass123!'):
    res = client.post(reverse('token_obtain_pair'), {'username': username, 'password': password}, format='json')
    return res.data['access']


def auth_client(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


# ---------------------------------------------------------------------------
# Authentication tests
# ---------------------------------------------------------------------------
class AuthTests(TestCase):

    def setUp(self):
        self.user = make_user()
        self.client = APIClient()

    def test_obtain_jwt_token(self):
        res = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser', 'password': 'TestPass123!'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_refresh_jwt_token(self):
        res = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser', 'password': 'TestPass123!'
        }, format='json')
        refresh = res.data['refresh']
        res2 = self.client.post(reverse('token_refresh'), {'refresh': refresh}, format='json')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertIn('access', res2.data)

    def test_invalid_credentials_rejected(self):
        res = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser', 'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_api_access_rejected(self):
        res = self.client.get(reverse('api-assets-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------------------------------------------
# Scheme 1: Assets API
# ---------------------------------------------------------------------------
class AssetAPITests(TestCase):

    def setUp(self):
        self.user = make_user()
        self.other = make_user('other', 'TestPass123!')
        token = get_jwt(APIClient(), 'testuser', 'TestPass123!')
        self.client = auth_client(token)

    def test_create_asset(self):
        res = self.client.post(reverse('api-assets-list'), {
            'name': 'BTC', 'asset_type': 'crypto', 'current_price': '67000.00', 'tv_symbol': 'BINANCE:BTCUSDT'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'BTC')

    def test_list_assets_only_own(self):
        Asset.objects.create(user=self.user, name='BTC', asset_type='crypto', current_price='67000')
        Asset.objects.create(user=self.other, name='ETH', asset_type='crypto', current_price='3500')
        res = self.client.get(reverse('api-assets-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        names = [a['name'] for a in res.data['results']]
        self.assertIn('BTC', names)
        self.assertNotIn('ETH', names)

    def test_update_asset(self):
        asset = Asset.objects.create(user=self.user, name='BTC', asset_type='crypto', current_price='67000')
        res = self.client.patch(reverse('api-assets-detail', args=[asset.pk]), {
            'current_price': '70000.00'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(str(res.data['current_price']), '70000.00000000')

    def test_delete_asset(self):
        asset = Asset.objects.create(user=self.user, name='BTC', asset_type='crypto', current_price='67000')
        res = self.client.delete(reverse('api-assets-detail', args=[asset.pk]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_access_other_users_asset(self):
        asset = Asset.objects.create(user=self.other, name='ETH', asset_type='crypto', current_price='3500')
        res = self.client.get(reverse('api-assets-detail', args=[asset.pk]))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------------------------
# Scheme 2: Transactions API
# ---------------------------------------------------------------------------
class TransactionAPITests(TestCase):

    def setUp(self):
        self.user = make_user()
        self.asset = Asset.objects.create(user=self.user, name='BTC', asset_type='crypto', current_price='67000')
        token = get_jwt(APIClient(), 'testuser', 'TestPass123!')
        self.client = auth_client(token)

    def test_create_transaction(self):
        res = self.client.post(reverse('api-transactions-list'), {
            'asset': self.asset.pk,
            'transaction_type': 'buy',
            'quantity': '0.5',
            'price_at_time': '67000.00',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['transaction_type'], 'buy')

    def test_list_transactions(self):
        Transaction.objects.create(user=self.user, asset=self.asset, transaction_type='buy',
                                   quantity='1', price_at_time='60000')
        res = self.client.get(reverse('api-transactions-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_delete_transaction(self):
        txn = Transaction.objects.create(user=self.user, asset=self.asset, transaction_type='buy',
                                         quantity='1', price_at_time='60000')
        res = self.client.delete(reverse('api-transactions-detail', args=[txn.pk]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Scheme 3: Trade Journal API
# ---------------------------------------------------------------------------
class TradeJournalAPITests(TestCase):

    def setUp(self):
        self.user = make_user()
        token = get_jwt(APIClient(), 'testuser', 'TestPass123!')
        self.client = auth_client(token)

    def test_create_journal_entry(self):
        res = self.client.post(reverse('api-journal-list'), {
            'symbol': 'EURUSD',
            'direction': 'long',
            'entry_price': '1.0850',
            'outcome': 'open',
            'lot_size': '1.0',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['symbol'], 'EURUSD')

    def test_list_journal_entries(self):
        TradeJournal.objects.create(user=self.user, symbol='BTCUSDT', direction='long',
                                    entry_price='65000', outcome='win', lot_size='1')
        res = self.client.get(reverse('api-journal-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_update_journal_entry(self):
        entry = TradeJournal.objects.create(user=self.user, symbol='BTCUSDT', direction='long',
                                            entry_price='65000', outcome='open', lot_size='1')
        res = self.client.patch(reverse('api-journal-detail', args=[entry.pk]), {
            'outcome': 'win', 'pnl': '500.00'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['outcome'], 'win')


# ---------------------------------------------------------------------------
# Scheme 4: Watchlist API
# ---------------------------------------------------------------------------
class WatchlistAPITests(TestCase):

    def setUp(self):
        self.user = make_user()
        token = get_jwt(APIClient(), 'testuser', 'TestPass123!')
        self.client = auth_client(token)

    def test_add_to_watchlist(self):
        res = self.client.post(reverse('api-watchlist-list'), {
            'symbol': 'XAUUSD', 'tv_symbol': 'OANDA:XAUUSD', 'notes': 'Watching for breakout'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['symbol'], 'XAUUSD')

    def test_list_watchlist(self):
        Watchlist.objects.create(user=self.user, symbol='XAUUSD')
        res = self.client.get(reverse('api-watchlist-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_remove_from_watchlist(self):
        item = Watchlist.objects.create(user=self.user, symbol='XAUUSD')
        res = self.client.delete(reverse('api-watchlist-detail', args=[item.pk]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Scheme 5: Portfolio Summary API
# ---------------------------------------------------------------------------
class PortfolioAPITests(TestCase):

    def setUp(self):
        self.user = make_user()
        token = get_jwt(APIClient(), 'testuser', 'TestPass123!')
        self.client = auth_client(token)

    def test_empty_portfolio(self):
        res = self.client.get(reverse('api-portfolio'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['total_value'], 0)

    def test_portfolio_calculates_pnl(self):
        asset = Asset.objects.create(user=self.user, name='BTC', asset_type='crypto', current_price='70000')
        Transaction.objects.create(user=self.user, asset=asset, transaction_type='buy',
                                   quantity='1', price_at_time='60000')
        res = self.client.get(reverse('api-portfolio'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['holdings']), 1)
        self.assertEqual(float(res.data['total_pnl']), 10000.0)
