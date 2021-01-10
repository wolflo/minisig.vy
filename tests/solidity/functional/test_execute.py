import pytest
import brownie
# import eth_event

from brownie.network.event import eth_event, EventDict

import utils.utils as utils
import utils.constants as C

# TODO: can't seem to send actually empty data
def test_empty_call(msig, mock, usrs):
    call_type = 0
    call_gas = 3000
    value = 0
    data = '0x00'

    tx = utils.signAndExecute(
        msig,
        usrs,
        mock.address,
        call_type,
        call_gas,
        value,
        data
    )

    assert msig.nonce() == 1
    call = tx.events[-1]
    assert call['src'] == msig.address
    assert call['context'] == mock.address
    assert call['gas'] <= call_gas
    assert call['val'] == value
    assert call['data'] == data

def test_call_w_value(msig, mock, usrs):
    call_type = 0
    call_gas = 3000
    value = 1
    data = '0xabababab'
    tx_value = 10

    tx = utils.signAndExecute(
        msig,
        usrs,
        mock.address,
        call_type,
        call_gas,
        value,
        data,
        {'value': tx_value}
    )
    call = tx.events[-1]

    assert msig.nonce() == 1
    assert call['src'] == msig.address
    assert call['context'] == mock.address
    assert call['gas'] <= call_gas + 2300
    assert call['val'] == value
    assert call['data'] == data
    assert msig.balance() == tx_value - value

def test_call_no_value(msig, mock, usrs, anyone):
    call_type = 0
    call_gas = 3000
    value = 2
    data = '0xabababab'

    anyone.transfer(msig.address, 10)
    bal0 = msig.balance()

    tx = utils.signAndExecute(
        msig,
        usrs,
        mock.address,
        call_type,
        call_gas,
        value,
        data
    )
    call = tx.events[-1]

    # print(f'type: {type(call)}')

    assert msig.nonce() == 1
    assert call['src'] == msig.address
    assert call['context'] == mock.address
    assert call['gas'] <= call_gas + 2300
    assert call['val'] == value
    assert call['data'] == data
    assert msig.balance() == bal0 - value

# TODO: can't seem to send actually empty data
def test_empty_delegatecall(msig, mock, usrs):
    call_type = 1
    call_gas = 3000
    value = 0
    data = '0x00'

    tx = utils.signAndExecute(
        msig,
        usrs,
        mock.address,
        call_type,
        call_gas,
        value,
        data
    )
    logs = eth_event.decode_logs(tx.logs, eth_event.get_topic_map(mock.abi))
    events = EventDict(logs)
    call = events[-1]

    assert msig.nonce() == 1
    assert call['src'] == tx.sender
    # to checksum address
    assert brownie.convert.to_address(call['context']) == msig.address
    assert call['gas'] <= call_gas
    assert call['val'] == 0
    assert call['data'] == data



# def test_success(msig, mock, accounts, usrs):
#     call_type = 0
#     call_gas = 3000
#     value = 1
#     data = '0xabab'

#     tx = utils.signAndExecute(
#         msig,
#         usrs,
#         mock.address,
#         call_type,
#         call_gas,
#         value,
#         data,
#         {'value': 10}
#     )

#     call = tx.events[-1]
#     print(f'call: {call}')

#     assert call['src'] == msig.address
#     assert call['context'] == mock.address
#     assert call['gas'] <= call_gas + 2300
#     assert call['val'] == value
#     assert call['data'] == data

    # tx = utils.signAndExecute(
    #     msig,
    #     usrs,
    #     '0xffffffffffffffffffffffffffffffffffffffff',
    #     call_type,
    #     tx_gas,
    #     value,
    #     data,
    #     {'value': 10}
    # )

    # print(f'modified_state: {dir(tx.modified_state)}\n')
    # print(f'subcalls: {dir(tx.subcalls)}\n')
    # print(f'call_trace: {dir(tx.call_trace())}\n')
    # print(f'trace: {dir(tx.trace)}\n')
    # print(f'traceback: {dir(tx.traceback)}\n')

    # print(f'modified_state: {(tx.modified_state)}\n')
    # print(f'subcalls: {(tx.subcalls)}\n')
    # print(f'call_trace: {(tx.call_trace(True))}\n')
    # print(f'events: {tx.events}\n')
    # print(f'trace: {(tx.trace)}\n')
    # print(f'traceback: {(tx.traceback)}\n')

    # digest = utils.encode_digest(
    #     msig,
    #     mock.address,
    #     call_type,
    #     tx_gas,
    #     value,
    #     data
    # )
    # sigs = utils.allSign(usrs, digest)

    # msig.execute(
    #     mock.address,
    #     call_type,
    #     tx_gas,
    #     value,
    #     data,
    #     sigs
    # )


    # print(f'modified_state: {dir(tx.modified_state)}\n')
    # print(f'subcalls: {dir(tx.subcalls)}\n')
    # print(f'call_trace: {dir(tx.call_trace())}\n')
    # # print(f'trace: {dir(tx.trace)}\n')
    # # print(f'traceback: {dir(tx.traceback)}\n')

    # print(f'modified_state: {(tx.modified_state)}\n')
    # print(f'subcalls: {(tx.subcalls)}\n')
    # print(f'call_trace: {(tx.call_trace(True))}\n')
    # print(f'trace: {(tx.trace)}\n')
    # print(f'traceback: {(tx.traceback)}\n')

    # digest = utils.encode_digest(
    #     msig,
    #     mock.address,
    #     call_type,
    #     tx_gas,
    #     value,
    #     data
    # )
    # sigs = utils.allSign(usrs, digest)

    # msig.execute(
    #     mock.address,
    #     call_type,
    #     tx_gas,
    #     value,
    #     data,
    #     sigs
    # )

