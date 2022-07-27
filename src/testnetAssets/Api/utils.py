
from tabnanny import check
from typing import TypeVar
# from xml.dom import ValidationErr
from stellar_sdk.asset import Asset
from stellar_sdk import TransactionBuilder, Keypair, Server, xdr, Network
# from stellar_sdk.keypair import Keypair
from decouple import config
from stellar_sdk.exceptions import NotFoundError




# TO DO
# Proper error handling



TransactionHash = TypeVar('TransactionHash', str, bytes)
SERVER = Server(horizon_url="https://horizon-testnet.stellar.org")
main_asset_issuer = Keypair.from_secret(config("ASSET_ISSUER")).public_key
ASSET_TRUSTLINE_ACCT = Keypair.from_secret(config("ASSET_TRUSTLINE_ACCT"))


def trustline_operation(asset_code:str) -> TransactionHash:
    src_acct = SERVER.load_account(ASSET_TRUSTLINE_ACCT.public_key)
    fee = SERVER.fetch_base_fee()
    trustlineOp = TransactionBuilder(
        source_account=src_acct,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=fee).append_change_trust_op(Asset(code=asset_code, issuer=main_asset_issuer)).set_timeout(30).build()
    trustlineOp.sign(ASSET_TRUSTLINE_ACCT)
    submitted_trustlineOp = SERVER.submit_transaction(trustlineOp)
    # print(submitted_trustlineOp)
    return submitted_trustlineOp

def is_asset_trusted(asset_code:str) -> bool:
    balance = SERVER.accounts().account_id(ASSET_TRUSTLINE_ACCT.public_key).call()

    asset_check = [i for i in balance["balances"] if i["asset_type"] != "native" and i["asset_code"] == asset_code]
    if len(asset_check) == 1:
        return True
    elif len(asset_check) != 1:
        return False
def list_of_trusted_assets():
    assets = SERVER.accounts().account_id(ASSET_TRUSTLINE_ACCT.public_key).call()

    assets_list = {}
    assets_list["XLM"]  = {"asset_code":"XLM", "asset_issuer":None}
    for i in assets["balances"]:
        if i["asset_type"] != "native":
            assets_list[i["asset_code"]] = {"asset_code":i["asset_code"], "asset_issuer":i["asset_issuer"]}
    return assets_list

def send_payment(asset_code: str, asset_issuer: str, destination_addr: str, amt: str, signer=config("ASSET_ISSUER")) -> str:
    _sender_keypair = Keypair.from_secret(signer)
    src_account = SERVER.load_account(_sender_keypair.public_key)
    paymentOp = TransactionBuilder(
        source_account=src_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=SERVER.fetch_base_fee()
    ).append_payment_op(destination=destination_addr, amount=str(amt), asset=Asset(code=asset_code, issuer=asset_issuer), source=_sender_keypair.public_key
                        ).set_timeout(30).build()
    paymentOp.sign(_sender_keypair)
    submitTx =SERVER.submit_transaction(paymentOp)

    return submitTx


def create_Assets(asset_code:str) -> TransactionHash:
    """
    Create an asset on testnet
    """
    #add trustline to address
    #make payment
    #add trade for the assets
    trustline = trustline_operation(asset_code=asset_code)
    print(trustline)
    return trustline




def reset_main_account(pub_key=Keypair.from_secret(config("ASSET_ISSUER")).public_key):
    import requests
    url = "https://friendbot.stellar.org"
    acc ={}
    acc[1] = main_asset_issuer
    acc[2] = ASSET_TRUSTLINE_ACCT.public_key
    for key, value in acc.items():
        response = requests.get(url, params={"addr": value})
        print(response.status_code)
        print(response.content.decode())
        if response.status_code == 400:
            raise Exception("Account already created")
        elif response.status_code == 200:
            return "account successfully created"



# acc = reset_main_account()
# print(acc)
# adc = trustline_operation("BTC")
# # adc = is_asset_trusted("BTC")
# print(adc
# )