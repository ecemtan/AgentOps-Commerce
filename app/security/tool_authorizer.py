from typing import Any, Callable


# Hangi agent hangi tool'u kullanabilir?
AGENT_TOOL_PERMISSIONS = {
    "order": {
        "get_order_status"
    },
    "product": {
        "get_product"
    },
    "refund": {
        "check_refund_eligibility"
    },
    "general": set()
}


def authorize_tool(
    agent_name: str,
    tool_name: str
) -> dict:

    allowed_tools = AGENT_TOOL_PERMISSIONS.get(
        agent_name,
        set()
    )

    allowed = tool_name in allowed_tools

    return {
        "allowed": allowed,
        "agent": agent_name,
        "tool": tool_name,
        "reason": (
            None
            if allowed
            else (
                f"{agent_name} agent'ının "
                f"{tool_name} tool'una erişim yetkisi yok."
            )
        )
    }


def execute_authorized_tool(
    agent_name: str,
    tool_name: str,
    tool_function: Callable,
    **kwargs: Any
) -> dict:

    authorization = authorize_tool(
        agent_name=agent_name,
        tool_name=tool_name
    )

    if not authorization["allowed"]:
        return {
            "success": False,
            "authorized": False,
            "data": None,
            "error": authorization["reason"]
        }

    try:
        result = tool_function(**kwargs)

        return {
            "success": True,
            "authorized": True,
            "data": result,
            "error": None
        }

    except Exception:
        return {
            "success": False,
            "authorized": True,
            "data": None,
            "error": "Tool çalıştırılırken hata oluştu."
        }