import ctypes
from io import StringIO
import time
import threading
import sys


class ExecuteResult:
    stdout: str
    stderr: str
    timed_out: bool


def raise_exception(thread, exc_type):
    tid = thread.ident
    if tid is None:
        return
    ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(exc_type)
    )
    if ret == 0:
        raise ValueError("invalid thread id")
    if ret != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(tid), None
        )
        raise SystemError("PyThreadState failed")


class Sandbox:
    def __init__(
        self,
        config: SandboxConfig
    ):
        self.config = config
        self.exec_globals = dict()

    def connect_mcp(
        self,
        mcp_client: MCPClient
    ):
        self.mcp_client = mcp_client

    
    def execute(
        self,
        code: str,
        timeout: float,
    ):
        result = ExecuteResult()
        or_stdout = sys.stdout
        or_stderr = sys.stdin
        rd_stdout = StringIO()
        rd_stderr = StringIO()
        def execute_thread():
            exec(code, self.exec_globals)
        thread = threading.Thread(target=execute_thread)
        sys.stdout = rd_stdout
        sys.stderr = rd_stderr
        thread.start()
        thread.join(timeout=timeout)
        sys.stdout = or_stdout
        sys.stderr = or_stderr
        if thread.is_alive():
            raise_exception(thread, ValueError)
            result.timed_out = True
            result.stdout = ""
            result.stderr = ""
        else:
            result.timed_out = False
            result.stdout = rd_stdout.getvalue()
            result.stderr = rd_stderr.getvalue()
        return result

