import click
import os
import dotenv
from hexbytes import HexBytes
from web3 import Web3
from src.ttBank import TTBank
from src.token_erc20 import Token

dotenv.load_dotenv()


assert os.getenv(
    "WALLET_ADDRESS") is not None, "You must set WALLET_ADDRESS environment variable"
assert os.getenv("WALLET_ADDRESS").startswith(
    "0x"), "Wallet address must start with 0x hex prefix"

assert os.getenv(
    "PRIVATE_KEY") is not None, "You must set PRIVATE_KEY environment variable"
assert os.getenv("PRIVATE_KEY").startswith(
    "0x"), "Private key must start with 0x hex prefix"

assert os.getenv(
    "GOERLI_PROVIDER") is not None, "You must set GOERLI_PROVIDER environment variable"

w3 = Web3(Web3.HTTPProvider(os.getenv("GOERLI_PROVIDER")))

ttBank = TTBank(os.getenv("WALLET_ADDRESS"), 5,
                os.getenv("GOERLI_PROVIDER"))

token = Token(os.getenv("WALLET_ADDRESS"), 5,
              os.getenv("GOERLI_PROVIDER"))


nonce = w3.eth.get_transaction_count(os.getenv("WALLET_ADDRESS"))


@click.group()
def cli():
    pass


@cli.command()
@click.argument("amount")
def approve_bank(amount: int):

    sign_approve_tx = w3.eth.account.sign_transaction(
        token.approve(ttBank.address, amount), private_key=os.getenv("PRIVATE_KEY"))

    tx_hash = w3.eth.send_raw_transaction(sign_approve_tx.rawTransaction)

    goerli_url = "https://goerli.etherscan.io/tx/" + HexBytes.hex(tx_hash)

    click.echo(
        f"Transaction Hash: {click.style(goerli_url,fg='magenta')}")


if __name__ == '__main__':
    cli()
