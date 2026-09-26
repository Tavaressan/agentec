# Hermes Academic

Agente acadêmico omnichannel para reduzir o ruído dos ambientes acadêmicos. Permite que um aluno pergunte, em linguagem natural, sobre matérias, tarefas, prazos, avisos e calendário — pelo Telegram, com um LLM (Hermes) chamando ferramentas via MCP (*Model Context Protocol*).

Projeto nascido em um hackathon presencial; o MVP usa dados mockados de uma Fatec fictícia, com arquitetura pensada para trocar o provider mockado por Microsoft Graph/Teams no futuro sem alterar MCP, agente ou interface.

## Arquitetura

```
Aluno → Telegram → Agent Orchestrator → Hermes (LLM) → MCP → AcademicProvider → dados
```

O MCP nunca acessa dados diretamente: depende da interface `AcademicProvider`, hoje implementada por um `MockAcademicProvider` (JSON local) e substituível por um `MicrosoftGraphAcademicProvider` mais adiante, sem tocar em MCP, agente ou Telegram.

## Status atual

- [x] Modelos de domínio tipados em Pydantic (`AcademicClass`, `Assignment`, `Announcement`, `CalendarEvent`, `Student`) — `src/hermes_academic/domain/models.py`
- [ ] `AcademicProvider` + `MockAcademicProvider` + `.env.example` (`MOCK_MODE=true`)
- [ ] Dataset mockado da Fatec (matérias, tarefas, avisos, calendário)
- [ ] MCP Server com as 6 tools semânticas (`listar_materias`, `listar_tarefas`, `buscar_tarefas`, `listar_avisos`, `buscar_avisos`, `consultar_calendario`)
- [ ] Agent Orchestrator com ciclo de tool-calling (`HermesProvider`)
- [ ] Handler do Telegram Bot integrado ao orchestrator

O acompanhamento detalhado de cada etapa está nas issues do repositório.

## Como rodar

Pré-requisitos: Python 3.12+ e [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
```

## Perspectivas

- **Curto prazo (MVP do hackathon):** completar a lista de status acima até o fluxo ponta a ponta funcionar no Telegram com dados mockados.
- **Microsoft Graph / Education APIs:** hoje bloqueado por consentimento administrativo no tenant CPS (`EduRoster.ReadBasic` e `EduAssignments.ReadBasic` exigem aprovação). Quando liberado, basta implementar `MicrosoftGraphAcademicProvider` — a interface já está desenhada para isso.
- **Teams:** extração de prazos informais mencionados em mensagens do Teams.
- **Notificações proativas:** avisos automáticos antes do vencimento de uma tarefa.
- **Dashboard / MCP Apps:** visão web complementar ao bot.

Fora do escopo do MVP por decisão explícita: OAuth real da CPS, Microsoft Entra, Microsoft Graph real, PostgreSQL, Redis, Docker, Kubernetes, multi-tenancy, RAG e vector database.
