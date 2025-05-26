import sys, os, types
import pytest
from fastapi import FastAPI

sys.modules["multipart"] = types.SimpleNamespace()

import gateway.app.main as gw_mod  # noqa:E402

def test_gateway_app_defined():
    assert isinstance(gw_mod.app, FastAPI)
    assert hasattr(gw_mod, "upload_file")
    assert hasattr(gw_mod, "get_file")
    assert hasattr(gw_mod, "trigger_analysis")
