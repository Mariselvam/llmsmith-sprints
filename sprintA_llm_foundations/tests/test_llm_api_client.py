import requests
import pytest
from llm_api_client import get_response, stream_response


def test_get_response_happy_path(mocker):
    fake_json = { "choices": [{"message": {"content": "This is a test response"}}]}
    mock_post = mocker.patch('llm_api_client.requests.post')
    mock_post.return_value.json.return_value = fake_json
    mock_post.return_value.raise_for_status.return_value = None

    result = get_response("Test prompt", "Test model", {"Authorization": "Bearer test_key"})
    assert result == "This is a test response"

def test_get_response_on_server_error(mocker):
    mock_post = mocker.patch('llm_api_client.requests.post')
    mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Internal Server Error"
    )
    with pytest.raises(requests.exceptions.HTTPError):
        get_response("hi", model='this is a test model', headers={"Authorization": "Bearer test_key"})

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

    mock_post = mocker.patch('llm_api_client.requests.post')
    mock_post.return_value.__enter__.return_value = mock_response
    
    result = list(stream_response("tell me a story", "test-model", {}))
    print("was request.post called?:", mock_post.called)
    print("was iter_lines called?:", mock_response.iter_lines.called)
    assert result == ["Once ", "Upon ", "a time."]
