from src.bases.services import BaseServices
from src.teasers.models import Teaser
from src.wallets.models import Wallet


class UpdateWalletBalanceServices(BaseServices):

    def __init__(self, teasers: list[Teaser]) -> None:
        self.teasers = teasers

    def __call__(self) -> list[Wallet]:
        wallets = []
        for teaser in self.teasers:
            if teaser.status != teaser.STATUS.paid:
                continue
            wallet: Wallet = teaser.user.wallet
            wallet.transfer_amount()
            wallets.append(wallet)

        Wallet.available_objects.select_for_update().bulk_update(wallets, fields=['balance'])
        return wallets
