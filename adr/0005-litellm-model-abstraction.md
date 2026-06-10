# LiteLLM is used as the model abstraction layer for all LLM calls

All LLM calls in the Python backend are made through LiteLLM (as a library, not a proxy). This gives a single unified interface across providers (Claude, GPT-4, Gemini, etc.) so the model can be swapped by changing a config string. A tiered approach is used — a more capable model for ExplanationSessions and PerformanceReport narrative generation, a faster/cheaper model for lightweight tasks like RevisionSession Pass 1. We chose LiteLLM over OpenRouter because LiteLLM calls providers directly, keeping student interaction data within our own infrastructure. Routing data through an aggregator's servers creates unnecessary exposure under India's DPDP Act, particularly given that users are minors. The trade-off is separate billing per provider and no built-in usage dashboard — Langfuse is used for LLM observability (see ADR-0013).

## Considered Options

- **OpenRouter**: Single API key, unified billing, automatic failover — but routes all requests through OpenRouter's servers, a third-party dependency for sensitive student data.
- **LiteLLM (library)** ✅: Same unified interface, direct provider calls, no data exposure, no pricing markup. Requires managing 2–3 provider API keys and configuring failover manually.
- **Custom abstraction layer**: More control but significant maintenance burden with no advantage over LiteLLM.
