<div align="center">

<a href="https://portfolio-khaki-ten-24.vercel.app"><img src="assets/hero.svg" width="100%" alt="Vaibhav Dangaich: AI agents, knowledge graphs, systems that finish the job" /></a>

<a href="https://portfolio-khaki-ten-24.vercel.app"><img src="https://img.shields.io/badge/Portfolio-0a0618?style=for-the-badge&logo=vercel&logoColor=ff2d55" alt="Portfolio" /></a>
<a href="https://linkedin.com/in/vaibhav-dangaich"><img src="https://img.shields.io/badge/LinkedIn-0a0618?style=for-the-badge&logo=linkedin&logoColor=2f6bff" alt="LinkedIn" /></a>
<a href="mailto:vaibhavdangaich@gmail.com"><img src="https://img.shields.io/badge/Email-0a0618?style=for-the-badge&logo=gmail&logoColor=ff2d55" alt="Email" /></a>
<a href="https://arxiv.org/search/?query=Dangaich&searchtype=author"><img src="https://img.shields.io/badge/arXiv-2%20preprints-0a0618?style=for-the-badge&logo=arxiv&logoColor=2f6bff&labelColor=0a0618&color=1a0f33" alt="arXiv" /></a>
<a href="https://www.npmjs.com/package/@vaibhav_dangaich/mnex"><img src="https://img.shields.io/npm/v/@vaibhav_dangaich/mnex?style=for-the-badge&logo=npm&logoColor=ff2d55&label=mnex&labelColor=0a0618&color=1a0f33" alt="mnex on npm" /></a>

</div>

## Hey, I'm Vaibhav 👋

Final-year **B.Tech in AI & ML at BIT Mesra** (CGPA 8.4). I work on the parts that sit
**between an LLM and a real system**: memory, state, audit trails, and turning messy
documents into **knowledge graphs you can query**. I ship end to end, from extension
to worker to graph DB to UI, not just the demo.

- 📄 **2 arXiv preprints** on knowledge-graph construction from real government documents
- 📦 **[mnex](https://www.npmjs.com/package/@vaibhav_dangaich/mnex)**, my terminal coding agent, is live on npm
- 🏆 **Top 5 of 200+ teams** at the IEEE CTF · **400+ DSA problems** solved
- 🔭 **Open to** internships and new-grad roles

## 💼 Experience

**123 of AI** · *Software Development Engineer Intern* · May 2026 – Jul 2026<br/>
Cohort learning platform on Next.js and Node/TypeScript over Azure. Owned monetization
(Razorpay orders, subscriptions and webhooks, idempotent entitlements, a ledger-based
credits system) and built a recommendation engine on vector embeddings with Azure OpenAI.

**Konect U** · *Artificial Intelligence Intern* · Feb 2026 – May 2026<br/>
Real-time document ingestion with Apache NiFi and Kafka for a defence-oriented government
intelligence project. LangChain LLM workflows and Neo4j knowledge graphs lifted
entity-search recall from **70% to 95% with zero false merges**.

**Konect U** · *Full Stack Intern* · Oct 2025 – Dec 2025<br/>
Full-stack delivery in an agile team, from client requirements to shipped features.

## 📄 Research

- **[Curate Before You Connect: Identity and Ontology Tagging in a Production Knowledge Graph](https://arxiv.org/abs/2608.10644)**<br/>
  <sub>arXiv:2608.10644 · Aug 2026 · Dangaich, Lewis, Pundalik</sub><br/>
  98,795 government documents → a graph of 537,157 entities and 2.2M relationships, matched
  through a record-identity ladder instead of name similarity. Anchored-evidence tagging cut
  spurious role assignments from 36 to 4.

- **[An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction from Heterogeneous Documents](https://arxiv.org/abs/2607.28662)**<br/>
  <sub>arXiv:2607.28662 · Jul 2026 · Dangaich, Lewis, Pundalik</sub><br/>
  Two-pass extraction with a self-hosted Qwen3.5-9B over a Kafka stream. Ontology-slice
  retrieval cut catalog overhead ~94%; a six-algorithm dedup pipeline raised recall
  70% → 95% with zero false merges.

## 🕸️ Featured builds

<table>
<tr>
<td width="50%" valign="top">

### [mnex](https://github.com/VaibhavDangaich/MNEX)
An AI coding agent that lives in your terminal. A stateful LangGraph
**planner → executor → critic** loop, 5-tier memory on SQLite WAL with sub-50ms recall,
and a local-first Ollama → cloud router that cuts inference cost ~40%.

`LangGraph` `Node.js` `SQLite` `Ollama`

```console
npm i -g @vaibhav_dangaich/mnex
```

</td>
<td width="50%" valign="top">

### [Orbit](https://github.com/VaibhavDangaich/Orbit)
A distributed job scheduler in Go, built from scratch: etcd leader election, a
transactional outbox into Kafka, `SKIP LOCKED` claiming in Postgres. Each run fires
**exactly once** and a crash loses no work. A 1,000-job load test on Kubernetes:
**1,000/1,000 in 97s**.

`Go` `etcd` `Kafka` `Postgres` `Redis` `K8s`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [FOIAtlas](https://github.com/VaibhavDangaich/foiatlas)
Turns released FOIA records into a queryable knowledge graph. Every **redaction is a
node** carrying its legal exemption code, so what was hidden becomes a lead. A LangGraph
ReAct agent handles search and graph edits. [Live demo ↗](https://foiatlas-499486403320.asia-southeast1.run.app)

`GraphRAG` `Kùzu` `Gemini` `Cloud Run`

</td>
<td width="50%" valign="top">

### [Servicing Agent](https://github.com/VaibhavDangaich/Codestreet_2026)
Card-servicing agent where **the LLM never decides**, it only proposes. A versioned
policy-as-code engine rules and cites the exact rule, and every step lands in a
**tamper-evident hash-chained audit trail**.

`Python` `Policy-as-code` `LLM agents`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [Context Graph](https://github.com/VaibhavDangaich/Context_graph)
Captures everything your AI coding agent did (messages, tool calls, files, errors) as
a Neo4j graph, then exports the compact context a new session needs to
**resume exactly where the last one stopped**.

`Python` `Neo4j` `FastAPI`

</td>
<td width="50%" valign="top">

### [Visual Activity Agent](https://github.com/VaibhavDangaich/visual-activity-agent)
A privacy-conscious Chrome MV3 extension that ships browsing signals and downscaled
screenshots to the server, where **Gemini vision** explains what you were doing.
Perceptual-hash dedup drops near-identical frames.

`Chrome MV3` `Node` `Gemini Vision`

</td>
</tr>
</table>

<sub>More: [Order Supervisor](https://github.com/VaibhavDangaich/Sagepilot) (durable AI supervisor on Temporal) · [PushMuse](https://github.com/VaibhavDangaich/ai-commit-cli) (AI commit messages) · [AI Resume Builder](https://github.com/VaibhavDangaich/AI-resume-builder) · [Portfolio](https://github.com/VaibhavDangaich/Portfolio)</sub>

## 🧰 Tech stack

<p>
  <img src="https://skillicons.dev/icons?i=py,ts,js,go,cpp&theme=dark" alt="Python, TypeScript, JavaScript, Go, C++" /><br/>
  <img src="https://skillicons.dev/icons?i=react,nextjs,nodejs,express,fastapi,tailwind,threejs&theme=dark" alt="React, Next.js, Node.js, Express, FastAPI, Tailwind, Three.js" /><br/>
  <img src="https://skillicons.dev/icons?i=postgres,mongodb,redis,sqlite,supabase,kafka&theme=dark" alt="PostgreSQL, MongoDB, Redis, SQLite, Supabase, Kafka" /><br/>
  <img src="https://skillicons.dev/icons?i=docker,kubernetes,azure,gcp,githubactions,vercel,git&theme=dark" alt="Docker, Kubernetes, Azure, GCP, GitHub Actions, Vercel, Git" />
</p>

**AI & graphs:** LangGraph · LangChain · Temporal · Ollama · Gemini · Azure OpenAI · Neo4j · Kùzu · vector search

## 🐍 Contributions

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/VaibhavDangaich/VaibhavDangaich/output/github-snake-dark.svg" />
  <img alt="A snake eating my GitHub contribution graph" src="https://raw.githubusercontent.com/VaibhavDangaich/VaibhavDangaich/output/github-snake.svg" />
</picture>

<div align="center">

<sub>Got an idea worth building? → **[vaibhavdangaich@gmail.com](mailto:vaibhavdangaich@gmail.com)** · <img src="https://komarev.com/ghpvc/?username=VaibhavDangaich&style=flat-square&color=ff2d55&label=views" alt="profile views" /></sub>

</div>
