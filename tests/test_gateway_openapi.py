import gateway.app.main as gw_mod  # noqa: E402

def test_gateway_openapi_contains_paths():
    spec = gw_mod.app.openapi()
    assert "openapi" in spec
    assert "/files" in spec["paths"]
    assert "/analysis/{file_id}" in spec["paths"]
    assert "/wordcloud/{key}" in spec["paths"]
