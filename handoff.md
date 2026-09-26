# HANDOFF DE IMPLEMENTAÇÃO
# Hackathon: Agente Acadêmico Omnichannel
# Codename: Hermes Academic

Você está assumindo a implementação de um MVP de hackathon.

IMPORTANTE:
- Estamos em um hackathon presencial e precisamos priorizar uma demo funcional.
- NÃO tente implementar integração real com o tenant Microsoft da CPS neste momento.
- A conta institucional @aluno.cps.sp.gov.br foi testada no Microsoft Graph Explorer.
- GET /v1.0/me funciona.
- Ao solicitar EduRoster.ReadBasic, o Microsoft Entra retorna "Necessidade de aprovação de administrador".
- GET /education/classes retorna AccessDenied / Required scp claim values are not provided.
- Portanto, o acesso às Education APIs está bloqueado por consentimento administrativo no tenant CPS.
- NÃO tente contornar essa restrição.
- O MVP usará dados mockados.
- A arquitetura DEVE permitir trocar o provider mockado por Microsoft Graph posteriormente sem alterar o MCP, o agente ou a interface do usuário.

==================================================
1. VISÃO DO PRODUTO
==================================================

Nome provisório:
Hermes Academic

Objetivo:

Criar um agente acadêmico omnichannel que reduz o ruído dos ambientes acadêmicos e permite que um aluno pergunte, em linguagem natural, sobre:

- matérias;
- tarefas;
- prazos;
- avisos;
- calendário acadêmico.

Canal principal do MVP:
Telegram Bot.

Cérebro:
Modelo Hermes, através de uma camada de abstração de LLM.

Ferramentas:
MCP Server.

Fonte de dados do MVP:
MockAcademicProvider.

Fonte de dados futura:
Microsoft Graph / Teams / Education APIs.

Fluxo:

Aluno
  ↓
Telegram
  ↓
Backend / Agent Orchestrator
  ↓
Hermes LLM
  ↓
MCP
  ↓
Academic Provider
  ↓
Mock Data

Futuro:

Academic Provider
  ↓
Microsoft Graph
  ↓
Microsoft Teams / Education

==================================================
2. PRINCÍPIO ARQUITETURAL
==================================================

O MCP NÃO deve acessar arquivos JSON diretamente.

Criar uma abstração:

AcademicProvider

Implementação atual:

MockAcademicProvider

Implementação futura:

MicrosoftGraphAcademicProvider

Exemplo conceitual:

AcademicProvider
├── MockAcademicProvider
└── MicrosoftGraphAcademicProvider (stub/futuro)

O MCP depende da interface AcademicProvider, não da implementação concreta.

Isso é obrigatório.

Queremos poder fazer:

MOCK_MODE=true

e posteriormente:

MOCK_MODE=false

sem modificar as ferramentas MCP.

==================================================
3. STACK
==================================================

Backend:
Python 3.12+

Package manager:
uv

MCP:
Official MCP Python SDK v2

Telegram:
python-telegram-bot

LLM:
Hermes através de uma camada LLMProvider.

Não acople o sistema diretamente a um fornecedor específico de LLM.

Criar:

LLMProvider
├── HermesProvider
└── MockLLMProvider (opcional para testes)

Banco:
Não introduzir PostgreSQL inicialmente.

Para o MVP:
- dados mockados em JSON;
- estado efêmero em memória se necessário.

Se persistência realmente for necessária:
SQLite.

Não adicionar Redis, PostgreSQL, Docker, Kubernetes ou cloud neste primeiro momento.

==================================================
4. MVP OBRIGATÓRIO
==================================================

O MVP deve conseguir demonstrar:

1. Usuário abre o bot Telegram.
2. Bot apresenta o agente.
3. Usuário pergunta:

   "O que eu tenho para entregar esta semana?"

4. Agente usa uma ferramenta MCP.
5. MCP consulta MockAcademicProvider.
6. Hermes interpreta os dados.
7. Telegram responde com os próximos prazos.

Também deve funcionar:

"Quais são minhas matérias?"

"Tenho alguma tarefa de Banco de Dados?"

"O que o professor de Banco de Dados avisou?"

"Qual é o próximo prazo?"

"Resuma o último aviso de Desenvolvimento Web."

==================================================
5. FERRAMENTAS MCP
==================================================

Implementar inicialmente exatamente estas ferramentas:

1. listar_materias()

Descrição:
Lista as matérias/turmas do aluno.

Retorno estruturado.

2. listar_tarefas(
    materia: string | null = null,
    periodo: string | null = null
)

Exemplos:

listar_tarefas()

listar_tarefas(materia="Banco de Dados")

listar_tarefas(periodo="esta_semana")

3. buscar_tarefas(
    query: string
)

Exemplo:

buscar_tarefas("projeto")

4. listar_avisos(
    materia: string | null = null,
    periodo: string | null = null
)

5. buscar_avisos(
    query: string
)

6. consultar_calendario(
    inicio: string | null = null,
    fim: string | null = null
)

NÃO criar dezenas de tools.

Queremos poucas ferramentas semânticas e fáceis de entender pelo LLM.

==================================================
6. DADOS MOCKADOS
==================================================

Criar:

data/
├── user.json
├── classes.json
├── assignments.json
├── announcements.json
└── calendar.json

Os dados devem parecer plausíveis para uma Fatec.

Não usar dados reais sensíveis.

Aluno fictício:

Nome:
Vitor Tavares Chaves

Curso:
Desenvolvimento de Software Multiplataforma

Semestre:
6º

Criar pelo menos 5 matérias.

Exemplo:

- Banco de Dados
- Desenvolvimento Web
- Engenharia de Software
- Inteligência Artificial
- Projeto Integrador

Criar pelo menos:

10 tarefas

10 avisos

5 eventos de calendário

Os dados devem conter situações úteis para demonstrar inteligência.

IMPORTANTE:

Criar pelo menos dois avisos que alterem ou contextualizem tarefas.

Exemplo:

Assignment:
"Projeto de Modelagem"

dueDate:
2026-09-28

Announcement posterior:
"A entrega do projeto foi prorrogada para 30/09."

O agente deverá conseguir perceber essa relação quando os dados forem recuperados.

==================================================
7. MODELO DE DADOS
==================================================

Usar modelos tipados.

Preferencialmente Pydantic.

Criar modelos como:

AcademicClass
Assignment
Announcement
CalendarEvent
Student

Assignment deve possuir pelo menos:

id
class_id
subject
title
description
due_date
status

Announcement:

id
class_id
subject
author
created_at
content

CalendarEvent:

id
subject
title
description
start
end
location

Não tentar reproduzir 100% do schema Microsoft Graph.

Criar somente o subconjunto necessário ao produto.

==================================================
8. MCP SERVER
==================================================

Criar algo como:

src/
└── mcp_server/
    ├── server.py
    ├── tools.py
    └── dependencies.py

O MCP deve expor as tools.

Usar o SDK MCP oficial atual.

Preferir saída estruturada quando apropriado.

As docstrings das tools devem ser extremamente claras porque serão utilizadas como descrição das ferramentas pelo modelo.

Exemplo conceitual:

@mcp.tool()
def listar_tarefas(...):
    """
    Lista tarefas acadêmicas do aluno.

    Use esta ferramenta quando o usuário perguntar sobre:
    - trabalhos;
    - provas;
    - entregas;
    - prazos;
    - tarefas pendentes.
    """

Não colocar lógica de LLM dentro das tools.

Não colocar Telegram dentro das tools.

==================================================
9. AGENT ORCHESTRATOR
==================================================

Criar:

src/
└── agent/
    ├── agent.py
    ├── prompts.py
    └── llm.py

Responsabilidades:

- receber mensagem do usuário;
- enviar contexto para Hermes;
- permitir tool calling;
- executar tools MCP;
- devolver resultado ao LLM;
- gerar resposta final.

O agente deve seguir este ciclo:

USER
 ↓
LLM
 ↓
tool call
 ↓
MCP
 ↓
tool result
 ↓
LLM
 ↓
final answer

Não fazer uma cadeia rígida de if/else para cada pergunta.

Queremos demonstrar agentic tool use.

==================================================
10. PROMPT DO AGENTE
==================================================

Criar um system prompt com estes princípios:

Você é Hermes Academic, um assistente acadêmico pessoal.

Sua função é ajudar o aluno a entender sua rotina acadêmica.

Regras:

1. Nunca invente tarefas, datas ou avisos.
2. Use as ferramentas acadêmicas quando a resposta depender de dados acadêmicos.
3. Diferencie claramente:
   - tarefa;
   - aviso;
   - evento de calendário.
4. Quando houver conflito entre um aviso mais recente e uma data anterior, destaque a atualização.
5. Quando não houver informação suficiente, diga isso.
6. Não transforme uma inferência em fato.
7. Seja conciso no Telegram.
8. Priorize datas e ações importantes.
9. Não exponha detalhes internos do MCP.
10. Não diga que os dados são mockados ao usuário final durante a demo, a menos que isso seja relevante.
11. Nunca invente uma fonte.

==================================================
11. TELEGRAM BOT
==================================================

Criar:

src/
└── telegram/
    ├── bot.py
    ├── handlers.py
    └── formatters.py

Comandos mínimos:

/start
/help
/prazos
/materias

Mas a principal interação deve ser linguagem natural.

Exemplo:

Usuário:
/start

Bot:

🎓 Hermes Academic

Seu assistente acadêmico.

Posso ajudar você a encontrar:
• próximos prazos
• tarefas
• avisos
• eventos
• informações das matérias

Experimente:

"O que tenho para entregar esta semana?"

==================================================
12. FORMATAÇÃO TELEGRAM
==================================================

Não usar tabelas Markdown densas.

Priorizar:

📚 Banco de Dados
📅 30/09
📌 Projeto de Modelagem

⚠️ Prazo atualizado pelo professor.

Usar InlineKeyboard quando fizer sentido.

Exemplo:

[ 📅 Próximos prazos ]

[ 📚 Minhas matérias ]

[ 📢 Últimos avisos ]

==================================================
13. ESTRUTURA DO PROJETO
==================================================

Propor inicialmente:

hermes-academic/
│
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── data/
│   ├── user.json
│   ├── classes.json
│   ├── assignments.json
│   ├── announcements.json
│   └── calendar.json
│
├── src/
│   ├── main.py
│   │
│   ├── domain/
│   │   ├── models.py
│   │   └── providers.py
│   │
│   ├── providers/
│   │   └── mock_provider.py
│   │
│   ├── mcp_server/
│   │   ├── server.py
│   │   └── tools.py
│   │
│   ├── agent/
│   │   ├── agent.py
│   │   ├── llm.py
│   │   └── prompts.py
│   │
│   └── telegram/
│       ├── bot.py
│       ├── handlers.py
│       └── formatters.py
│
└── tests/
    ├── test_provider.py
    ├── test_mcp_tools.py
    └── test_agent.py

Pode ajustar a estrutura se houver uma razão técnica forte.

Não criar complexidade arquitetural sem necessidade.

==================================================
14. CONFIGURAÇÃO
==================================================

Criar .env.example:

TELEGRAM_BOT_TOKEN=

HERMES_API_KEY=

HERMES_BASE_URL=

HERMES_MODEL=

MOCK_MODE=true

LOG_LEVEL=INFO

Nunca colocar secrets no Git.

==================================================
15. TESTES
==================================================

Antes do Telegram funcionar, testar:

1. MockAcademicProvider

2. MCP tools

3. Agent tool calling

4. Telegram handler

Criar testes para:

- listar matérias;
- listar tarefas;
- filtrar por matéria;
- buscar avisos;
- identificar tarefa próxima;
- lidar com ausência de resultados.

==================================================
16. DEMO PRINCIPAL
==================================================

A demo oficial deve ser preparada para esta sequência:

1.

Usuário:

"Quais são minhas matérias?"

↓

Hermes chama listar_materias()

↓

Resposta.

2.

Usuário:

"O que tenho para entregar esta semana?"

↓

Hermes chama listar_tarefas(periodo="esta_semana")

↓

Resposta organizada por prazo.

3.

Usuário:

"O professor de Banco de Dados mudou o prazo?"

↓

Hermes chama listar_avisos()

↓

Relaciona aviso + tarefa.

↓

Resposta:

"Sim. O prazo do Projeto de Modelagem foi alterado de 28/09 para 30/09."

4.

Usuário:

"Tem alguma prova chegando?"

↓

Hermes consulta calendário/tarefas.

↓

Resposta.

==================================================
17. CRITÉRIO DE SUCESSO
==================================================

O projeto está pronto para demo quando:

[ ] Bot Telegram inicia.
[ ] /start funciona.
[ ] Perguntas em linguagem natural funcionam.
[ ] Hermes consegue chamar ferramentas.
[ ] MCP funciona.
[ ] Dados mockados são recuperados pelo MCP.
[ ] O agente não inventa dados.
[ ] Próximos prazos são identificados.
[ ] Avisos podem contextualizar tarefas.
[ ] Pelo menos 3 perguntas diferentes funcionam end-to-end.
[ ] Nenhum secret está commitado.
[ ] README explica arquitetura e execução.

==================================================
18. FORA DO ESCOPO DO MVP
==================================================

NÃO implementar agora:

- OAuth real da CPS;
- Microsoft Entra;
- Microsoft Graph real;
- refresh tokens;
- banco PostgreSQL;
- Redis;
- Docker;
- Kubernetes;
- notificações 48h;
- dashboard web;
- MCP Apps;
- geração de imagens;
- RAG;
- vector database;
- multi-tenancy;
- autenticação complexa;
- sistema de permissões;
- scraping do Teams;
- leitura real de mensagens do Teams.

Tudo isso pode aparecer como roadmap.

==================================================
19. ROADMAP FUTURO
==================================================

Documentar no README:

FASE 1 - Hackathon
Mock Provider
↓
MCP
↓
Hermes
↓
Telegram

FASE 2
Microsoft Entra OAuth
↓
Microsoft Graph
↓
Education APIs

FASE 3
Teams messages
↓
extração de prazos informais

FASE 4
notificações proativas

FASE 5
dashboard / MCP Apps

==================================================
20. MICROSOFT GRAPH
==================================================

Não implementar ainda.

Porém, criar uma interface que permita futuramente:

class MicrosoftGraphAcademicProvider(AcademicProvider):
    ...

O provider futuro deverá consumir Microsoft Graph.

Permissões atualmente relevantes para o cenário Education incluem:

EduRoster.ReadBasic
EduAssignments.ReadBasic

A documentação atual da Microsoft indica que essas permissões delegadas requerem consentimento administrativo.

O teste realizado durante o hackathon confirmou isso no tenant CPS.

Não tentar contornar essa restrição.

==================================================
21. QUALIDADE DO CÓDIGO
==================================================

Prioridades:

1. Demo funcionando.
2. Código simples.
3. Separação clara de responsabilidades.
4. Tipagem.
5. Testes mínimos.
6. Fácil substituição do MockProvider.
7. README executável.

Evitar:

- overengineering;
- abstrações sem uso;
- microserviços;
- filas;
- Docker obrigatório;
- arquitetura distribuída;
- padrões enterprise desnecessários.

Preferir um monólito modular.

==================================================
22. PRIMEIRA TAREFA
==================================================

NÃO comece escrevendo tudo de uma vez.

Primeiro:

1. Inspecione o diretório atual.
2. Verifique se já existe código.
3. Identifique stack existente.
4. Não sobrescreva arquivos existentes sem entender o projeto.
5. Proponha a estrutura mínima.
6. Implemente primeiro:
   - domain models;
   - AcademicProvider;
   - MockAcademicProvider;
   - dataset.
7. Rode os testes.
8. Depois implemente MCP.
9. Depois Agent.
10. Depois Telegram.
11. Só então faça o fluxo end-to-end.

Após cada etapa:
- execute testes;
- corrija erros;
- mantenha o projeto executável.

Comece agora pela inspeção do repositório e pela implementação da camada de domínio + MockAcademicProvider.