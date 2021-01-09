#!/usr/bin/python3

import pytest

import utils.constants as C
import utils.utils as utils

@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    pass

@pytest.fixture(scope="module")
def mock(TargetMock, accounts, deployer):
    return TargetMock.deploy({'from': deployer})

@pytest.fixture(scope="module")
def deployer(accounts):
    return accounts[1]

@pytest.fixture(scope="module")
def usrs(accounts):
    unsorted = utils.derive_accts(C.MNEMONIC, C.NUM_SIGNERS)
    return sorted(unsorted, key = lambda x: x.address)

@pytest.fixture(scope="module")
def usr_ids(usrs):
    return [ u.address for u in usrs ]

@pytest.fixture
def anyone(accounts):
    return accounts[0]

# @pytest.fixture(scope="module")
# def msig(Minisig, accounts, deployer, usr_ids):
#     return Minisig.deploy(C.THRESHOLD, usr_ids, {'from': deployer})


