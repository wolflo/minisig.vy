import pytest

import utils.constants as C

@pytest.fixture(scope="module")
def msig(Minisig, deployer, usr_ids):
    return Minisig.deploy(C.THRESHOLD, usr_ids, {'from': deployer})
