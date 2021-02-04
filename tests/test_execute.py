import pytest
import brownie

from brownie.network.event import eth_event, EventDict

import utils.utils as utils
import utils.constants as C

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
    call = tx.events[-1]

    assert msig.nonce() == 1
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
