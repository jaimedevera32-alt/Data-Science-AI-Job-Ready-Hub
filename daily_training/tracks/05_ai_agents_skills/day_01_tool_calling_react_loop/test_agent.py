try:
    import pytest
except ImportError:
    pytest = None

from agent import ReActAgent

def test_agent_tool_registration_and_execution():
    agent = ReActAgent()
    
    # Herramienta dummy: sumador
    agent.register_tool("add", lambda a, b: a + b)
    
    result = agent.call_tool("add", {"a": 10, "b": 25})
    assert result == 35

def test_agent_handles_missing_tool():
    agent = ReActAgent()
    res = agent.call_tool("non_existent_tool", {})
    assert "no existe" in res.lower()

def test_agent_handles_tool_exception():
    agent = ReActAgent()
    agent.register_tool("divide", lambda a, b: a / b)
    res = agent.call_tool("divide", {"a": 10, "b": 0})
    assert "error en la ejecución" in res.lower()

def test_agent_react_execution_loop():
    agent = ReActAgent()
    agent.register_tool("fetch_weather", lambda city: f"Soleado en {city}, 22C")
    
    plan = [
        {
            "thought": "Necesito consultar el clima en Madrid.",
            "action": {"tool": "fetch_weather", "args": {"city": "Madrid"}}
        },
        {
            "thought": "Tengo la observación del clima, redacto respuesta final.",
            "final_answer": "El clima en Madrid es soleado con 22C."
        }
    ]
    
    res = agent.run_plan(plan)
    assert res["status"] == "COMPLETED"
    assert res["final_answer"] == "El clima en Madrid es soleado con 22C."
    assert len(res["history"]) == 2
    assert "Soleado en Madrid" in res["history"][0]["observation"]

def test_agent_max_iteration_guard():
    agent = ReActAgent()
    agent.register_tool("ping", lambda: "pong")
    
    # Bucle infinito simulado de 10 pasos
    infinite_plan = [
        {"thought": "Sigo pensando...", "action": {"tool": "ping", "args": {}}}
        for _ in range(10)
    ]
    
    res = agent.run_plan(infinite_plan, max_steps=4)
    assert res["status"] == "STOPPED_MAX_ITERATIONS"
