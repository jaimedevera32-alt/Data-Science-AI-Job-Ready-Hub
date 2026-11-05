from typing import Callable, Dict, Any, List, Optional
import json

class ToolExecutionError(Exception):
    pass

class ReActAgent:
    """
    Motor fundamental de un Agente ReAct con Tool Execution y Safety Limits.
    """
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def register_tool(self, name: str, func: Callable):
        """Registra una herramienta ejecutable por el agente."""
        self.tools[name] = func

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Despacha la herramienta de forma segura."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' no existe en el catálogo."
        try:
            return self.tools[tool_name](**arguments)
        except Exception as e:
            return f"Error en la ejecución de la herramienta '{tool_name}': {str(e)}"

    def run_plan(self, steps: List[Dict[str, Any]], max_steps: int = 5) -> Dict[str, Any]:
        """
        Simulación determinista del bucle de ejecución de un agente ReAct.
        Cada paso contiene {'thought': str, 'action': {'tool': str, 'args': dict}} o 'final_answer'.
        """
        iteration = 0
        final_answer = None

        for step in steps:
            iteration += 1
            if iteration > max_steps:
                return {
                    "status": "STOPPED_MAX_ITERATIONS",
                    "history": self.execution_history,
                    "final_answer": "Límite de seguridad de pasos alcanzado."
                }

            if "final_answer" in step:
                final_answer = step["final_answer"]
                self.execution_history.append({"thought": step.get("thought", ""), "final_answer": final_answer})
                break

            action = step.get("action", {})
            tool_name = action.get("tool")
            args = action.get("args", {})
            
            tool_result = self.call_tool(tool_name, args)
            self.execution_history.append({
                "thought": step.get("thought", ""),
                "action": action,
                "observation": tool_result
            })

        return {
            "status": "COMPLETED" if final_answer is not None else "INCOMPLETE",
            "history": self.execution_history,
            "final_answer": final_answer
        }

