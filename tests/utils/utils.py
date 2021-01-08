import brownie
import eth_abi
from eth_account.messages import encode_structured_data
import eth_account

from eth_account._utils.signing import sign_message_hash

import utils.constants as C
web3 = brownie.network.web3

def derive_accts(mnemonic, n):
    return [ web3.eth.account.from_mnemonic(C.MNEMONIC, f"m/44'/60'/0'/0/{i}") for i in range(n) ]

def encode_dom_sep(inst):
    chain_id = brownie.network.chain.id
    preimg = eth_abi.encode_abi(
        [ 'bytes32', 'uint256', 'uint256', 'address' ],
        [
            bytes.fromhex(C.DOMAIN_SEPARATOR_TYPEHASH[2:]),
            chain_id,
            inst.tx.block_number,
            inst.address
        ]
    )
    return web3.keccak(preimg).hex()

def encode_digest(inst, nonce, target, call_type, gas, value, data):
    dom_sep = encode_dom_sep(inst)
    # nonce = inst.nonce()
    hash_data = web3.solidityKeccak(['bytes'], [data])
    struct_preimg = eth_abi.encode_abi(
        ['bytes32', 'address', 'uint8', 'uint256', 'uint256', 'uint256', 'bytes32' ],
        [
            bytes.fromhex(C.EXECUTE_TYPEHASH[2:]),
            target,
            call_type,
            nonce,
            gas,
            value,
            hash_data
        ]
    )
    hash_struct = web3.keccak(struct_preimg)
    digest = web3.solidityKeccak(
        [ 'bytes1', 'bytes1', 'bytes32', 'bytes32' ],
        [ '0x19', '0x01', dom_sep, hash_struct ]
    )
    return digest


def allSign(usrs, digest):
    sigs = [ bytes(u.signHash(digest).signature).hex() for u in usrs ]
    return ''.join(sigs)

def signAndExecute(inst, usrs, target, call_type, gas, value, data, opts={}):
    nonce = inst.nonce()
    digest = encode_digest(inst, nonce, target, call_type, gas, value, data)
    sigs = allSign(usrs, digest)
    return inst.execute(target, call_type, gas, value, data, sigs, opts)



##############################
# def sign(accts, inst, target, call_type, gas, value, data):
#     # digest_live = inst.getDigest(target, call_type, gas, value, data)
#     # print(f'digest_live: {digest_live}')

#     digest = encode_digest(inst, target, call_type, gas, value, data)
#     print(f'digest: {digest.hex()}')


#     # pk = '0x3908956f4fbddaa06f071386fde61473dba589cd1b98464c8afa12fc0aa4d8a0'
#     # pk = accts()
#     # a = web3.eth.account.from_key(pk)

#     # sig = a.signHash(digest)
#     sig = accts[0].signHash(digest)

#     # sigs = eth_abi.encode_abi([ 'bytes' ], [ sig.signature ])
#     # sigs should be the concatenation of all of the signatures
#     sigs = sig.signature

#     print(f'sig: {sig}')
#     # print(f'sig_v: {hex(sig.v)}')
#     # print(f'sig_r: {hex(sig.r)}')
#     # print(f'sig_s: {hex(sig.s)}')
#     # print(f'\nsigner: {a.address}')
#     # print(f'signers: {inst.allSigners()}')
#     return sigs


# def new_encode_digest(inst, target, call_type, gas, value, data):
#     nonce = inst.nonce()
#     chain_id = brownie.network.chain.id
#     eip712_data = {
#         "types": {
#             "EIP712Domain": [
#                 {"name": "chainId", "type": "uint256"},
#                 {"name": "deployBlock", "type": "uint256"},
#                 {"name": "verifyingContract", "type": "address"}
#             ],
#             "Execute": [
#                 {"name": "target", "type": "address"},
#                 {"name": "callType", "type": "uint8"},
#                 {"name": "nonce", "type": "uint256"},
#                 {"name": "txGas", "type": "uint256"},
#                 {"name": "value", "type": "uint256"},
#                 # {"name": "data", "type": "bytes"}
#             ]
#         },
#         "domain": {
#             "chainId": chain_id,
#             "deployBlock": inst.tx.block_number,
#             "verifyingContract": inst.address
#         },
#         "primaryType": "Execute",
#         "message": {
#             "target": target,
#             "callType": call_type,
#             "nonce": nonce,
#             "txGas": gas,
#             "value": value,
#             # "data": data
#         }
#     }

#     return encode_structured_data(eip712_data)

