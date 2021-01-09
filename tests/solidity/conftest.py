#!/usr/bin/python3

import pytest

import utils.constants as C

@pytest.fixture(scope="module")
def msig(Minisig, accounts, deployer, usr_ids):
    return Minisig.deploy(C.THRESHOLD, usr_ids, {'from': deployer})
