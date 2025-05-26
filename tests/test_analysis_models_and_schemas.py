import analysis.app.models as m_mod  # noqa: E402
import analysis.app.schemas as s_mod  # noqa: E402

def test_analysis_model_and_schema():
    ar = m_mod.AnalysisResult(
        file_id=42, paragraphs=1, words=2, characters=3, wordcloud_location=None
    )
    assert ar.file_id == 42
    resp = s_mod.AnalysisResponse(ready=True, paragraphs=1, words=2, characters=3, wordcloud_location="k")
    assert resp.ready is True
    assert isinstance(resp.wordcloud_location, str)
