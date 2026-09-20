# Module 08 — Agentic Knowledge Graphs

Hands-on material covering knowledge graphs as a reasoning substrate for AI agents — from foundational concepts through production-ready pipelines.

## Structure

```
08-agentic-knowledge-graphs/
├── 08-agentic-knowledge-graphs.ipynb                              # Full lecture notes
├── foundations-of-knowledge-graphs-for-agents-slides.pdf         # Part 1 source slides
├── building-and-integrating-agent-driven-knowledge-graphs-slides.pdf  # Part 2 source slides
└── frameworks-tools-and-best-practices-for-agentic-knowledge-graphs-slides.pdf  # Part 3 source slides
```

## Learning Path

| Part | What you'll learn |
|---|---|
| Part 1 — Foundations | Why agents need structured reasoning, knowledge graph definition, entities / relationships / ontologies / schemas, graph traversal, document vs. vector vs. graph retrieval, explainability in high-stakes domains |
| Part 2 — Building & Integrating | Text-to-graph pipeline, LLM extraction with schema validation, incremental construction and the MERGE/upsert pattern, entity canonicalization and deduplication, LPG vs. RDF storage, Cypher vs. SPARQL queries, LLM + graph integration patterns, hybrid retrieval (routing vs. fusion) |
| Part 3 — Frameworks & Production | Production pipeline (ingestion → extraction → storage → query → answer), Neo4j / RDF / TypeDB / custom comparison, graph querying tips, governance checklist, schema versioning and evolution, graph health monitoring, access control |

## Key Concepts

- **Knowledge graph** — a network of real-world entities connected by typed, directed relationships; turns fragmented data into a connected structure an agent can reason over
- **Triplets** — every fact is `(Subject) --[Predicate]--> (Object)`; the basic unit of graph storage
- **Ontologies** — domain rules about which relationships are valid; the grammar of the graph
- **Schemas** — enforce required fields and type consistency across nodes and edges
- **MERGE / upsert** — insert-or-match pattern that prevents duplicate nodes when ingesting streaming data
- **Entity canonicalization** — normalize entity names before insertion so synonym variants converge on a single node
- **Labeled Property Graph (LPG)** — Neo4j / TigerGraph; flexible schema, fast traversals, Cypher query language
- **RDF Triple Store** — GraphDB / Blazegraph; formal W3C semantics, ontology alignment, SPARQL
- **TypeDB** — strict polymorphic type system with built-in inference rules, TypeQL
- **Graph as tool call** — the agent calls `find_related_issues("Battery Drain")`, receives an evidence subgraph and reasoning path; does not write the query itself
- **Hybrid retrieval** — routing strategy (pick vector *or* graph per query) vs. fusion strategy (combine both)
- **Multi-hop reasoning** — following chains of edges across multiple nodes to reach a causal conclusion
- **Graph health monitoring** — track query latency, node growth by class, orphan node rate, schema drift alerts

## The Orion Running Example

Throughout the module, **Orion** is an AI support agent that handles customer tickets. The knowledge graph domain has four entity types:

| Entity | Description |
|---|---|
| `Customer` | Reports a problem with a product |
| `Product` | The software or hardware involved |
| `Issue` | The problem experienced |
| `Resolution` | The fix that resolves an issue |

Key relationships: `Customer -[:REPORTED]-> Issue -[:AFFECTS]-> Product`, `Issue -[:RESOLVED_BY]-> Resolution`.

## Prerequisites

A working Python environment and an `OPENAI_API_KEY`. Copy `.env.example` to `.env` and fill in your key if a `.env.example` is present in the project root.

## Further Reading

- [Neo4j Documentation](https://neo4j.com/docs/)
- [W3C RDF Primer](https://www.w3.org/TR/rdf11-primer/)
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
- [TypeDB Documentation](https://typedb.com/docs)
- [LangChain × Neo4j Integration](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/)
- [IBM — What is a Knowledge Graph?](https://www.ibm.com/think/topics/knowledge-graph)
