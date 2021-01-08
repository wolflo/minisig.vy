# import brownie
# from eth_account.messages import SignableMessage
# from hexbytes import HexBytes

# digest = '0x888ea8f5f07a24f8cae848c8b85c1273ce2d44efe1abf249ca02c41ce28840c8'
# pk = '0x3908956f4fbddaa06f071386fde61473dba589cd1b98464c8afa12fc0aa4d8a0'

# web3 = brownie.network.web3

# def test_success():
#     signer = web3.eth.account.from_key(pk)

#     sig_signHash = signer.signHash(digest)
#     sig_sign_message = signer.sign_message(
#         SignableMessage(
#             HexBytes('0x01'),
#             b'',
#             bytes.fromhex(digest[2:])
#         )
#     )


#     # print(f'sig_signHash: {sig_signHash.signature}')
#     # print(f'sig_sign_message: {sig_sign_message.signature}')
#     print(f'sig_signHash: {sig_signHash}')
#     print(f'sig_sign_message: {sig_sign_message}')
