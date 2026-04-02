from web.api import _api_segments, is_api_path


def test_is_api_path():
    assert is_api_path("/api")
    assert is_api_path("/api/")
    assert is_api_path("/api/students")
    assert is_api_path("/api/students/1")
    assert not is_api_path("/apiary")
    assert not is_api_path("/students")


def test_api_segments():
    assert _api_segments("/api/students") == ["students"]
    assert _api_segments("/api/students/42") == ["students", "42"]
    assert _api_segments("/api/setup/init") == ["setup", "init"]
    assert _api_segments("/api") == []
