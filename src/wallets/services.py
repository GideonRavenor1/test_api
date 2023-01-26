from collections import defaultdict

from src.bases.services import BaseServices
from src.teasers.models import Teaser
from src.wallets.models import Wallet


class UpdateWalletBalanceServices(BaseServices):

    def __init__(self, teasers: list[Teaser]) -> None:
        self.teasers = teasers

    def __call__(self) -> list[Wallet]:
        wallets_dict = defaultdict(int)
        for teaser in self.teasers:
            if teaser.status != teaser.STATUS.paid:
                continue
            wallet: Wallet = teaser.user.wallet
            wallets_dict[wallet] += 1
        wallets = [self._pay_for_work(wallet, multiplier) for wallet, multiplier in wallets_dict.items()]
        Wallet.available_objects.select_for_update().bulk_update(wallets, fields=['balance'])
        return wallets

    @staticmethod
    def _pay_for_work(wallet: Wallet, multiplier: int) -> Wallet:
        wallet.transfer_amount(multiplier)
        return wallet
