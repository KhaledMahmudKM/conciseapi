# Concise Book on APIs

A concise, diagram-rich guide to web APIs, with runnable Python examples.

<img src="cover.svg" alt="Cover Image" width="100%" >

Every app on your phone, every website you visit, and most of the software running in companies today talk to each other through **APIs**. A weather widget asks a weather service for a forecast; an online shop asks a payment service to charge a card; a build pipeline asks a cloud provider to start a server. Each of those conversations follows a contract, and that contract is an API.

This book explains how web APIs work, how to design and build good ones, how to secure them, and how to run them in production. It assumes you can write basic Python and know roughly what an IP address and a web server are. It assumes no prior API experience.

Every chapter comes with examples you can run. You will build a small **Library API** with **FastAPI**, call it with **curl** and Python's **requests**, break it on purpose, secure it, and finally rebuild parts of it with GraphQL and gRPC.

---

## How this book is organized

**Part I, Foundations.** What an API is, the lab setup, HTTP from the ground up, and JSON.

**Part II, Building REST APIs.** Designing resources and URLs, building a complete API with validation, errors and pagination, and documenting it with OpenAPI.

**Part III, Securing APIs.** Authentication and authorization with API keys, OAuth 2.0 and JWTs, then the most common API vulnerabilities, demonstrated on a deliberately vulnerable API and fixed.

**Part IV, APIs in Production.** Caching, rate limits, retries and idempotency; versioning, gateways, observability and testing; and alternatives to REST: GraphQL, gRPC, webhooks and streaming.

The **Appendix** is a curl and HTTP cheat sheet, and the **Glossary** defines every term.

---

## How to read it

Read Part I first, then Part II in order. Parts III and IV can be read in any order after that.

Each chapter ends with a short summary and a **Check your understanding** quiz of eight multiple-choice questions; the **Answers to Chapter Questions** chapter, after the Glossary, gives every answer with a short explanation. Sections marked **Hands on** use the example code, which is in the [`code/` folder](https://github.com/khaledmahmudkm/conciseapi/tree/main/code) of this book's repository, together with automated tests for every example.
