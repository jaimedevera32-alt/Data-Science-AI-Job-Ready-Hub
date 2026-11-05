# Reto Día 01: El Bucle ReAct y Despacho Seguro de Herramientas (Tool Calling)

## 📌 Contexto de Entrevista Técnica (AI Engineer / Agentic AI)
En las entrevistas de IA Generativa y Agentes (OpenAI, Anthropic, Google, startups de IA), ya no basta con llamar a la API de un LLM. Se evalúa la comprensión profunda de la arquitectura de un Agente Autónomo:
1. El bucle **ReAct (Reasoning + Acting)**.
2. Despacho dinámico de herramientas (*Tool Dispatching*).
3. Mecanismos de seguridad contra bucles infinitos (*Max Iteration Safety Guard*).
4. Manejo estructurado de errores en ejecución de herramientas sin romper el contexto.

## 🎯 Objetivo
Implementa una clase `ReActAgent` que gestione:
* Un registro de herramientas disponibles (`register_tool(name, func)`).
* Un método de ejecución de un paso (`step(observation)`).
* El bucle de ejecución `run(user_goal, max_iterations=5)` que parsea la intención de llamar a una herramienta, la ejecuta con sus argumentos, inyecta el resultado como nueva observación y termina cuando el agente emite la respuesta final o alcanza el límite de iteraciones.

## ❓ Pregunta de Selección (Minutos 50 - 60)
* ¿Por qué el patrón de tool calling estructurado (JSON Schema / Pydantic) es superior a pedirle al modelo texto libre para parsear con regex?
* *Respuesta esperada:* El parseo por regex es frágil ante variaciones de formato, alucinaciones de comillas o saltos de línea. Los esquemas JSON / Tool Calling nativo imponen restricciones guiadas por gramática (*constrained decoding* / *grammar sampling* a nivel de logits) garantizando que la salida sea sintácticamente válida antes de llegar al intérprete de código.

