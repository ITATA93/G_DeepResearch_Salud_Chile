"""Unit tests for search tools."""

from unittest.mock import patch, MagicMock


def test_get_search_tool_returns_configured_tool():
    """Test that get_search_tool returns a properly configured DuckDuckGo tool."""
    from src.core.tools import get_search_tool

    tool = get_search_tool()
    assert tool is not None
    assert tool.name == "ddg_search_chile"


def test_get_search_tool_uses_chile_region():
    """Test that search tool is configured for Chilean region."""
    with patch("src.core.tools.DuckDuckGoSearchAPIWrapper") as MockWrapper:
        with patch("src.core.tools.DuckDuckGoSearchRun") as MockRun:
            mock_wrapper = MagicMock()
            MockWrapper.return_value = mock_wrapper

            from src.core import tools
            # Re-call to use the mocked version
            tools.get_search_tool()

            MockWrapper.assert_called_once_with(
                region="cl-es", time="y", max_results=5
            )
