"""CLI reasoning auto-routing tests."""

from cli import (
    _auto_reasoning_decision,
    _parse_reasoning_config,
    _resolve_turn_reasoning_config,
)


def test_cli_parse_reasoning_auto_keeps_auto_sentinel():
    assert _parse_reasoning_config("auto") == {
        "enabled": True,
        "effort": "auto",
        "auto": True,
    }


def test_cli_resolves_auto_before_provider_request_for_simple_prompt():
    parsed = _parse_reasoning_config("auto")

    resolved = _resolve_turn_reasoning_config(parsed, "嗨")

    assert resolved is not None
    assert resolved == {"enabled": True, "effort": "low", "auto_reason": "simple"}
    assert resolved.get("effort") != "auto"
    assert "auto" not in resolved


def test_cli_auto_router_matches_gateway_high_risk_conventions():
    assert _auto_reasoning_decision(
        "TWTS 實盤 Shioaji 下單 partial fill race condition 要怎麼修？"
    ) == {"enabled": True, "effort": "xhigh", "auto_reason": "TWTS/live-trading"}
    assert _auto_reasoning_decision("幫我研究規劃這個 Hermes effort 標註功能") == {
        "enabled": True,
        "effort": "high",
        "auto_reason": "analysis/judgment",
    }


def test_cli_auto_router_uses_low_for_routine_status_checks():
    assert _auto_reasoning_decision("盤前有都正常嗎") == {
        "enabled": True,
        "effort": "low",
        "auto_reason": "status/check",
    }
    assert _auto_reasoning_decision("TWTS runtime 還活著嗎") == {
        "enabled": True,
        "effort": "low",
        "auto_reason": "status/check",
    }


def test_cli_auto_router_uses_medium_for_routine_summaries_and_daily_reviews():
    assert _auto_reasoning_decision("再給一次定錨筆記統整") == {
        "enabled": True,
        "effort": "medium",
        "auto_reason": "routine-summary",
    }
    assert _auto_reasoning_decision("盤點今日遇到的問題") == {
        "enabled": True,
        "effort": "medium",
        "auto_reason": "routine-summary",
    }


def test_cli_auto_router_escalates_routine_requests_when_judgment_is_requested():
    assert _auto_reasoning_decision("再給一次定錨筆記統整，並補你的多空判斷") == {
        "enabled": True,
        "effort": "high",
        "auto_reason": "analysis/judgment",
    }
    assert _auto_reasoning_decision("盤點今日遇到的問題，並分析根因與修復優先順序") == {
        "enabled": True,
        "effort": "high",
        "auto_reason": "analysis/judgment",
    }
