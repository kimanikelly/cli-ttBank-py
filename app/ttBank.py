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


@cli.command("approve-bank", help="Allows the connected wallet to approve TTBank for a set amount of Test Tokens before opening an account and depositing ")
@click.argument("amount")
def approve_bank(amount: int):

    sign_approve_tx = w3.eth.account.sign_transaction(
        token.approve(ttBank.address, amount), private_key=os.getenv("PRIVATE_KEY"))

    tx_hash = w3.eth.send_raw_transaction(sign_approve_tx.rawTransaction)

    goerli_url = "https://goerli.etherscan.io/tx/" + HexBytes.hex(tx_hash)

    click.echo(
        f"Transaction Hash: {click.style(goerli_url,fg='magenta')}")


@cli.command("open-account", help="Allows the connected wallet to open an account with TTBank and make an initial deposit")
@click.argument("starting-balance")
def open_account(starting_balance):
    sign_open_account_tx = w3.eth.account.sign_transaction(
        ttBank.open_account(starting_balance), private_key=os.getenv("PRIVATE_KEY")
    )

    tx_hash = w3.eth.send_raw_transaction(sign_open_account_tx.rawTransaction)

    goerli_url = "https://goerli.etherscan.io/tx/" + HexBytes.hex(tx_hash)

    click.echo(
        f"Transaction Hash: {click.style(goerli_url,fg='magenta')}")


@cli.command("deposit", help="Allows the connected wallet with an existing account to deposit Test Tokens")
@click.argument("amount")
def deposit(amount: int):
    sign_deposit_tx = w3.eth.account.sign_transaction(
        ttBank.deposit(amount), private_key=os.getenv("PRIVATE_KEY")
    )
    tx_hash = w3.eth.send_raw_transaction(sign_deposit_tx.rawTransaction)

    goerli_url = "https://goerli.etherscan.io/tx/" + HexBytes.hex(tx_hash)

    click.echo(
        f"Transaction Hash: {click.style(goerli_url,fg='magenta')}")


@cli.command("withdraw", help="Allows the connected wallet to withdraw Test Tokens from their existing account")
@click.argument("amount")
def withdraw(amount):
    sign_withdraw_tx = w3.eth.account.sign_transaction(
        ttBank.withdraw(amount), private_key=os.getenv("PRIVATE_KEY")
    )

    tx_hash = w3.eth.send_raw_transaction(sign_withdraw_tx.rawTransaction)

    goerli_url = "https://goerli.etherscan.io/tx/" + HexBytes.hex(tx_hash)

    click.echo(
        f"Transaction Hash: {click.style(goerli_url,fg='magenta')}")


@cli.command("view-account", help="Allows the connected wallet to view their Account Number, Account Name, and Account Balance")
def view_account():

    click.echo(
        f"Account Number: {click.style(ttBank.fetch_account()[0],fg='magenta')}")
    click.echo(
        f"Account Name: {click.style(ttBank.fetch_account()[1],fg='magenta')}")
    click.echo(
        f"Account Balance: {click.style(w3.from_wei(ttBank.fetch_account()[2],'ether'),fg='magenta')} TT")


@ cli.command("view-account-balance", help="Allows the connected wallet to view their Account Balance")
def view_account_balance():

    click.echo(
        f"The account balance of {click.style(ttBank.account,fg='magenta')} is: {click.style(w3.from_wei(ttBank.fetch_account_balance(), 'ether'),fg='magenta')} TT")


@ cli.command("view-bank-balance", help="Allows the connected wallet to view the TTBank balance")
def view_bank_balance():

    click.echo(
        f"The bank balance is: {click.style(w3.from_wei(ttBank.fetch_bank_balance(), 'ether'),fg='magenta')} TT")


if __name__ == '__main__':
    cli()
