import pytest
from groq_client import get_response, stream_response, GroqServerError, GroqAuthError, GroqBadRequestError, GroqRateLimitError


def test_get_response_happy_path(mocker):
    fake_json = { "choices": [{"message": {"content": "This is a test response"}}]}
    mock_post = mocker.patch('groq_client.client.requests.post')
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = fake_json
    mock_post.return_value.raise_for_status.return_value = None

    result = get_response("Test prompt", "Test model", {"Authorization": "Bearer test_key"})
    assert result == "This is a test response"

def test_get_response_on_server_error_on_500(mocker):
    mock_post = mocker.patch('groq_client.client.requests.post')
    mock_post.return_value.status_code = 500
    mock_post.return_value.text = "Internal Server Error"
    with pytest.raises(GroqServerError):
        get_response([{"role": "user", "content": "hi"}], model='this is a test model', headers={"Authorization": "Bearer test_key"})

def test_raises_auth_error_on_401(mocker):
    mock_post = mocker.patch("groq_client.client.requests.post")
    mock_post.return_value.status_code = 401
    mock_post.return_value.text = "Unauthorized"

    with pytest.raises(GroqAuthError):
        get_response([{"role": "user", "content": "hi"}], model="this is a test model", headers={})

def test_raises_bad_req_error_on_400(mocker):
    mock_post = mocker.patch("groq_client.client.requests.post")
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "Bad Request"

    with pytest.raises(GroqBadRequestError):
        get_response([{"role": "user", "content": "hi"}], model="this is a test model", headers={})

def test_raises_ratelimit_error_on_429(mocker):
    mock_post = mocker.patch("groq_client.client.requests.post")
    mock_post.return_value.status_code = 429
    mock_post.return_value.text = "Ratelimit exceeded"

    with pytest.raises(GroqRateLimitError):
        get_response([{"role": "user", "content": "hi"}], model="this is a test model", headers={})


def test_stream_response_yields_chunks(mocker):
    fake_lines = [
        b"",
        b'data: {"choices": [{"delta": {"content": "Once "}}]}',
        b'data: {"choices": [{"delta": {"content": "Upon "}}]}',
        b'data: {"choices": [{"delta": {}}]}',
        b'data: {"choices": [{"delta": {"content": "a time."}}]}',
        b"data: [DONE]",
    ]

    mock_response = mocker.MagicMock()
    mock_response.iter_lines.return_value = fake_lines
    mock_response.raise_for_status.return_value = None
    mock_response.__exit__.return_value = False
    mock_response.status_code = 200

    mock_post = mocker.patch('groq_client.client.requests.post')
    mock_post.return_value.__enter__.return_value = mock_response
    
    result = list(stream_response("tell me a story", "test-model", {}))
    print("was request.post called?:", mock_post.called)
    print("was iter_lines called?:", mock_response.iter_lines.called)
    assert result == ["Once ", "Upon ", "a time."]
