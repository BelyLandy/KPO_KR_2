from fastapi import FastAPI
import gateway.app.main as gw_mod  # noqa: E402

def test_gateway_app_and_routes():
    assert isinstance(gw_mod.app, FastAPI)
    paths = {r.path for r in gw_mod.app.routes}
    expected = {
        "/files", "/files/{file_id}",
        "/analysis/{file_id}", "/wordcloud/{key}"
    }
    assert expected.issubset(paths)
