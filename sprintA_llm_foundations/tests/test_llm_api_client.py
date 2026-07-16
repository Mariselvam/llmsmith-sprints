from llm_api_client import get_response, stream_response

def test_get_response_happy_path(mocker):
    fake_json = { "choices": [{"message": {"content": "This is a test response"}}]}
    mock_post = mocker.patch('llm_api_client.requests.post')
    mock_post.return_value.json.return_value = fake_json
    mock_post.return_value.raise_for_status.return_value = None

    result = get_response("Test prompt", "Test model", {"Authorization": "Bearer test_key"})
    assert result == "This is a test response"
