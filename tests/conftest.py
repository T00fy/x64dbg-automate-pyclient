import os
import pytest

from x64dbg_automate_pyclient import X64DbgClient

TEST_BITNESS=64
X64DBG_PATH = os.getenv("X64DBG_PATH", f"E:\\re\\x64dbg_dev\\release\\x{TEST_BITNESS}\\x{TEST_BITNESS}dbg.exe")


@pytest.fixture
def client():
    client = X64DbgClient(x64dbg_path=X64DBG_PATH)
    yield client
    client.terminate_session()
