import os
import subprocess
from tests.conftest import TEST_BITNESS, X64DBG_PATH
from x64dbg_automate import X64DbgClient


def test_connect(client: X64DbgClient):
    client.start_session()


def test_reconnect(client: X64DbgClient):
    sid = client.start_session()
    client.detach_session()
    client.attach_session(sid)


def test_compat_version(client: X64DbgClient):
    client.start_session()
    client._assert_connection_compat()


def test_bitness(client: X64DbgClient):
    client.start_session()
    assert client.debugee_bitness() == TEST_BITNESS


def test_debugger_version(client: X64DbgClient):
    client.start_session()
    assert client.get_debugger_version() > 18 # TODO: what is the lowest version we support?


def test_dbg_is_elevated(client: X64DbgClient):
    client.start_session()
    assert client.debugger_is_elevated() == False


def test_dbg_is_debugging(client: X64DbgClient):
    client.start_session()
    assert client.is_debugging() == False
    assert client.load_executable(r'c:\Windows\system32\winver.exe') == True
    assert client.is_debugging() == True


def test_dbg_is_running(client: X64DbgClient):
    client.start_session(r'c:\Windows\system32\winver.exe')
    assert client.is_running() == False
    assert client.cmd_sync('g') == True
    assert client.is_running() == True


def test_dbg_load_cwd(client: X64DbgClient):
    client.start_session(r'winver.exe', "", r'c:\Windows\system32')
    assert client.is_running() == False
    assert client.cmd_sync('g') == True
    assert client.is_running() == True


def test_dbg_load_shortpath(client: X64DbgClient):
    os.chdir(r'c:\Windows\system32')
    client.start_session(r'winver.exe')
    assert client.is_running() == False
    assert client.cmd_sync('g') == True
    assert client.is_running() == True


def test_config_get_set(client: X64DbgClient):
    client.start_session()
    assert client.get_setting_str('Shortcuts', 'ActionFind') == 'Ctrl+F'
    assert client.set_setting_str('Shortcuts', 'ActionFind', 'Ctrl+G') == True
    assert client.get_setting_str('Shortcuts', 'ActionFind') == 'Ctrl+G'
    assert client.get_setting_int('Deleted Tabs', 'BreakpointsTab') == 0
    assert client.set_setting_int('Deleted Tabs', 'BreakpointsTab', 9000) == True
    assert client.get_setting_int('Deleted Tabs', 'BreakpointsTab') == 9000


def test_attach(client: X64DbgClient):
    proc = subprocess.Popen([X64DBG_PATH])
    client.wait_for_session(proc.pid)
    client.attach_session(proc.pid)
    assert client.is_debugging() == False
