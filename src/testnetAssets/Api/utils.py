
from typing import TypeVar
# from xml.dom import ValidationErr
from stellar_sdk.asset import Asset
from stellar_sdk import TransactionBuilder, Keypair, Server, xdr, Network
# from stellar_sdk.keypair import Keypair
from decouple import config




# TO DO
# Proper error handling



TransactionHash = TypeVar('TransactionHash', str, bytes)
SERVER = Server(horizon_url="https://horizon-testnet.stellar.org")


def add_trustline(asset_code: str, asset_issuer: str, signer=config("MAIN_KEY")) -> xdr:
    """
        Function to add trustline to an account
    """
    # stablecoin address adds trustline to ALLOWED NGN
    # protocol address adds trustline to NGN
    userKeyPair = Keypair.from_secret(signer)
    fee = SERVER.fetch_base_fee()
    src_account = SERVER.load_account(userKeyPair.public_key)
    trustlineOp = TransactionBuilder(
        source_account=src_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=fee).append_change_trust_op(Asset(code=asset_code, issuer=asset_issuer)).set_timeout(30).build()
    trustlineOp.sign(signer)

    submitted_trustlineOp = SERVER.submit_transaction(trustlineOp)
    return submitted_trustlineOp


def send_payment(asset_code: str, asset_issuer: str, destination_addr: str, amt: str, signer=config("MAIN_KEY")) -> str:
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

    newly_created_asset = Asset(
        code=asset_code, issuer=Keypair.from_secret(config("MAIN_KEY")).public_key)
    #add trustline to address
    trustline_added = add_trustline(newly_created_asset.code, newly_created_asset.issuer)
    if trustline_added:
        # create payments

        #create a
       
        payment_created = send_payment(
            newly_created_asset.code, newly_created_asset.issuer, Keypair.from_secret(config("MAIN_KEY")).public_key, "1")
        # burn_tx = send_payment(
        #     newly_created_asset.code, newly_created_asset.issuer, newly_created_asset.issuer, "1")
        print(payment_created)
        # print(burn_tx)
 
        data={}
        data['payments_hash'] = payment_created["hash"]
        data['burn_tx_hash'] = burn_tx["hash"]
        return data

    return;


def reset_main_account(pub_key=Keypair.from_secret(config("MAIN_KEY")).public_key):
    import requests
    url = "https://friendbot.stellar.org"
    response = requests.get(url, params={"addr": pub_key})
    if response.status_code == 200:
        print(response.json())
        return pub_key
    else:
        pass


