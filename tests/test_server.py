"""
Tests for MCP M365 Teams Server
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from mcp_m365_teams.server import M365TeamsServer


@pytest.fixture
def server():
    """Create a test server instance"""
    return M365TeamsServer()


@pytest.mark.asyncio
async def test_server_initialization(server):
    """Test server initializes correctly"""
    assert server.app is not None
    assert server.client is None


@pytest.mark.asyncio
async def test_list_tools(server):
    """Test that tools are properly registered"""
    # Get the list_tools handler
    tools = await server.app._tool_manager.list_tools()
    
    # Check that expected tools are present
    tool_names = [tool.name for tool in tools]
    
    assert "list_teams" in tool_names
    assert "get_team_channels" in tool_names
    assert "send_channel_message" in tool_names
    assert "get_channel_messages" in tool_names
    assert "create_team" in tool_names
    assert "add_team_member" in tool_names
    assert "create_channel" in tool_names
    assert "get_user_presence" in tool_names
    assert "search_messages" in tool_names


@pytest.mark.asyncio
async def test_initialize_client_missing_env_vars(server):
    """Test that client initialization fails with missing env vars"""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="Missing required environment variables"):
            await server._initialize_client()


@pytest.mark.asyncio
async def test_list_teams(server):
    """Test listing teams"""
    # Mock the Graph client
    mock_client = AsyncMock()
    mock_teams_response = Mock()
    mock_teams_response.value = [
        Mock(id="team1", display_name="Team 1", description="Description 1"),
        Mock(id="team2", display_name="Team 2", description="Description 2"),
    ]
    mock_client.me.joined_teams.get.return_value = mock_teams_response
    
    server.client = mock_client
    
    result = await server._list_teams()
    
    assert result["count"] == 2
    assert len(result["teams"]) == 2
    assert result["teams"][0]["id"] == "team1"
    assert result["teams"][0]["display_name"] == "Team 1"


@pytest.mark.asyncio
async def test_list_teams_empty(server):
    """Test listing teams when user has no teams"""
    mock_client = AsyncMock()
    mock_teams_response = Mock()
    mock_teams_response.value = []
    mock_client.me.joined_teams.get.return_value = mock_teams_response
    
    server.client = mock_client
    
    result = await server._list_teams()
    
    assert result["count"] == 0
    assert len(result["teams"]) == 0


@pytest.mark.asyncio
async def test_get_team_channels(server):
    """Test getting channels for a team"""
    mock_client = AsyncMock()
    mock_channels_response = Mock()
    mock_channels_response.value = [
        Mock(
            id="channel1",
            display_name="General",
            description="General channel",
            email="general@team.com"
        ),
    ]
    mock_client.teams.by_team_id.return_value.channels.get.return_value = mock_channels_response
    
    server.client = mock_client
    
    result = await server._get_team_channels("team1")
    
    assert result["count"] == 1
    assert result["channels"][0]["id"] == "channel1"
    assert result["channels"][0]["display_name"] == "General"


@pytest.mark.asyncio
async def test_send_channel_message(server):
    """Test sending a message to a channel"""
    mock_client = AsyncMock()
    mock_message_response = Mock()
    mock_message_response.id = "message123"
    mock_message_response.created_date_time = None
    
    mock_client.teams.by_team_id.return_value.channels.by_channel_id.return_value.messages.post.return_value = mock_message_response
    
    server.client = mock_client
    
    result = await server._send_channel_message("team1", "channel1", "Hello, World!")
    
    assert result["success"] is True
    assert result["message_id"] == "message123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
