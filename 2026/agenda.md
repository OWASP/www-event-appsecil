---
layout: custom-2026
startSection: lblue
---

{% assign cfg = site.data["year-2026"].config %}

<section class="page-section page-section_lblue">
<div class="page-section__inner">

<div class="text text_type_narrow" markdown="1">

# Agenda

Explore the full lineup of expert talks, hands-on sessions, and community highlights at OWASP AppSec Israel 2026 — the country's leading application security event.

From secure development and cloud security to AI threats and real-world case studies, this year's agenda brings together top minds and practical insights for developers, DevOps, security engineers, and tech leaders.

Times and room assignments will be published closer to the event. Below is the confirmed speaker lineup.

---

</div>
</div>
</section>

<section class="page-section">
<div class="page-section__inner">
<div class="text text_type_narrow" markdown="1">

### Unveiling the OWASP Top 10 for Agentic AI
**Keren Katz**

In this session, Keren Katz, the lead of the OWASP Top 10 for Agentic AI, breaks down the top 10 agentic risks, real-world incidents, and practical mitigations - offering a go-to guide for building and deploying secure AI agents in the enterprise.

---

### I Built an Agent That Hacks Like I Do (And It's Terrifying)
**Sagiv Peer**

What happens when you teach an AI agent to think like a red teamer? Not just run tools - actually think. Chain findings together. Decide what to try next. Pivot when something fails. I built one, and watching it work changed how I see both offensive security and AI risk. In this talk, I'll share what it's like to watch an autonomous agent go from reconnaissance to domain compromise - following the same 7-phase methodology I use on engagements - and what that means for defenders who are about to face attackers that don't get tired, don't get distracted, and can run a hundred attack chains while you're reading this abstract. This isn't science fiction. It's working. And we need to talk about it.

---

### Beyond the Bomb: Securing AI Applications and Agents through Security Steerability
**Itay Hazan**

Is a "secure" LLM actually secure for your business? Our analysis uncovered a startling reality: there is zero correlation between a model's ability to refuse universal jailbreaks and its ability to follow custom application guardrails. So while you're pretty sure your AI won't tell customers how to build a bomb, you should still worry about your customer service bot recommending a competitor's product, or leaking sensitive pricing data, specifically violating the business rules and operational boundaries encoded in your system prompts.

While the industry obsesses over "Universal Security" (preventing toxic or prohibited content), our research shows we might be missing something important. A model might refuse a general jailbreak about violence, but will happily ignore your instructions.

This risk significantly exacerbates with AI Agents. When LLMs move from talking to acting, a bypassed guardrail doesn't just mean bad text; it means unauthorized SQL queries, privilege escalation, and physical safety violations. The threat shifts from "bad information" to "bad action".

In this session, we introduce Security Steerability: the missing metric for how well models adhere to your specific rules under adversarial pressure. We will release two open-source toolkits to help you battle-test your deployments:
- veganRibs: A benchmark focused on chatbot applications, testing if models stick to functional constraints (e.g., "do not discuss competitors") against sophisticated boosters and jailbreaks.
- ASTRA: A framework for testing whether agents maintain operational boundaries across diverse environments — from industrial robots to SQL assistants — to prevent critical issues ranging from unauthorized tool use to privilege escalation.

Data from 18 open-source LLMs reveals that "safer" models aren't necessarily "steerable". Join us to learn how to validate that your AI is not just generally safe, but securely aligned with your business logic.

---

### When React Becomes an Attack Vector: Lessons from the React2Shell CVE
**Ofir Elarat**

In late 2025, a critical vulnerability known as React2Shell demonstrated how modern frontend frameworks can become a direct path to remote code execution when trust boundaries are misunderstood.

What made this vulnerability especially interesting is that it originated from frontend architecture decisions, React Server Components and Server Actions, but resulted in a full backend compromise.

In this session, we analyze React2Shell as a real-world case study in broken trust boundaries: how a client-controlled entry point crossed into trusted server execution, and how serialization and invocation assumptions failed.

We walk through the attack chain step by step, from the initial client interaction to server-side execution, and show how this maps directly to OWASP Top 10 categories such as Injection, Broken Access Control, and Insecure Design.

The session closes by translating the vulnerability into concrete guidance using OWASP ASVS and WSTG, showing how this class of issue could have been detected, modeled, or mitigated earlier.

---

### The Hidden DoS Vector in SQL Parsers
**Ori Nakar**

SQL parsers are critical components of the modern data stack. They support SQL validation, transpiling and linting operations which are widely used by many data flows, including AI-driven SQL generation. However, these tools contain a hidden flaw: they are highly susceptible to resource exhaustion from seemingly "simple" queries.

In this talk, we describe our findings of 10+ new vulnerabilities stemming from Recursive Stack Overflow and Parser AST Object-Inflation, where small inputs generate excessively large Abstract Syntax Trees and exhaust resources. We demonstrate how a query with just 50+ levels of nesting or a high number of repeating columns can crash an entire process or the underlying Python interpreter. These flaws propagate to major downstream applications, and we'll demonstrate their impact on several representative popular applications. We then uncover the root cause: AST object inflation. A payload of only a few megabytes can expand into millions of Python objects, reliably triggering out-of-memory failures. We conclude with practical mitigations, showing how simple limits on recursion depth and AST size can harden parsers against this new class of SQL exhaustion attacks.

As the industry moves toward automated SQL generation and LLM-integrated data tools, the parser is no longer just a utility, it's an attack vector. We move beyond SQL Injection to explore SQL Exhaustion, proving that even syntactically correct queries can be weaponized to dismantle high-traffic data infrastructure.

---

### LLMs as Adaptive Query Planners for SAST
**Oren Ish-Shalom**

Transforming real-life codebases into queryable knowledge is one challenge. Effectively searching for vulnerabilities within vast amounts of semantic data is another.

This in-depth talk presents a novel approach in which LLMs incrementally query a language-agnostic semantic interface to enumerate endpoints, trace data flows, and guide exploration based on solver feedback. Starting from an empty context, the model gradually builds understanding and focuses only on high-signal program areas.

We provide a detailed technical walkthrough of how this approach enabled the discovery of a previously unknown vulnerability in a highly starred open-source repo (confirmed by the maintainers and fixed upstream).

---

### Bad Vibes: Comparing the Secure Coding Capabilities of Coding Agents
**Ori David**

Vibe coding has fundamentally changed how we create software. While coding agents deliver many benefits, their rapid adoption raises an important question: how secure is the code they actually produce?

To find out, we put five of the most popular coding agents to the test - Cursor, Claude Code, Codex, Replit, and Devin. We tasked each with building an identical set of web applications using the same prompts and tech stack, and then hacked them to find which was the most vulnerable. The verdict? There are no real winners here.

In this talk, we'll walk through the good, the bad, and the ugly of secure vibe coding. We'll show you the vulnerability classes where agents do surprisingly well, the ones they struggled with, and the ones every single one failed miserably. We'll close with practical takeaways on what developers can do today to ship vibe-coded applications without shipping vulnerabilities along with them.

---

### Off Script at Scale: Analyzing Rogue Agents Across 86K Repos and a Year of Production Incidents
**Bar Kaduri, Lidan Hazout**

How common is it for an AI agent to go rogue, not because someone attacked it, but because it was given a goal, tools, and no way to be stopped?

We looked at that question from two places: production behavior, and the code people actually ship.

In our CurseBox research, we traced a behavior in Cursor's coding agent that showed up first in production. Asked to share a local file through a channel that could not carry it, the agent decided on its own to upload that file to a public anonymous host so it could hand back a link, and the person who made the request had no reason to think anything had left the intended tool. We reproduced it in the lab across every major model, including under a deny-all sandbox the agent found a way around. The same shape shows up in a production database wiped in nine seconds, an inbox agent that ignored STOP, and evaluation agents that left the lab and reached real organizations. None of these required an external adversary.

We complemented the incident work by studying how the community actually builds agents: 86,000 public repositories, the tools they grant, and the MCP servers they wire in. Roughly one in ten of those codebases hand agents shell, eval, raw SQL, or filesystem access. Among tools with explicit definitions, 76.4% have no input validation. On MCP, 82.8% of servers lack input validation and 92.4% have no confirmation gate before a tool runs. Between the model's decision and system-level execution, there is almost nothing.

This talk maps those behaviors onto the OWASP Top 10 for Agentic Applications and argues that control must live in one place: the moment between the agent deciding to act and the action reaching the system.

---

### Who Let the DAGs Out? Securing Apache Airflow in the Real World
**Or Sahar**

Apache Airflow orchestrates machine learning pipelines, data platforms, and automation workflows across the globe. With tens of millions of monthly downloads and adoption by tens of thousands of organizations, it has become critical infrastructure in modern cloud environments.

But what happens when DAGs go rogue?

In this session, we explore real-world security weaknesses in Airflow deployments found in the wild. Through controlled live demonstrations, we'll show what attackers can actually do, and how defenders can secure their orchestration layer without breaking production.

---

### Zero-Trust Data Protection at Scale: Building an Enterprise Identity and Key Management Platform
**Adi Finkelstein**

Managing encryption keys and secrets across multi-cloud environments is one of the hardest problems in enterprise security. In this talk, we'll walk through how Intuit built a zero-trust data protection platform that brokers cloud identities (AWS, GCP, GitHub Actions, Databricks), manages cryptographic keys with a zero-knowledge split-key architecture, and automates least-privilege access for thousands of workloads - all without developers ever handling long-lived secrets. We'll share practical lessons on implementing cryptographic attestation, policy-based access control, and key lifecycle management at scale.

---

### Never Say Never: Owning ChatGPT's Secure Sandbox
**Simcha K**

OpenAI designed ChatGPT's container sandbox as a secure runtime environment, enforcing full network isolation, strict execution timeouts, and an AI supervisor to filter every command. Under this model, owning the container and extracting sensitive data seemed impossible. However, we demonstrate that by chaining file-parsing abuse for persistent execution, reasoning-channel hijacking for data extraction, and shared infrastructure manipulation, an attacker can establish cross-tenant data exfiltration.

In this talk, we will demonstrate a complete attack chain that shatters ChatGPT's secure sandbox. By abusing spreadsheet file parsing, we bypass the LLM supervisor to gain persistent, unmonitored root execution. From there, we escalate the attack by live-patching the internal Jupyter kernel to hijack the model's hidden python.exec reasoning channel, executing a Reasoning Injection Attack to extract sensitive user data. To exfiltrate this data, we bypass network isolation by weaponizing the Task Scheduler to launder malicious URLs past strict web guardrails.

The attack reaches its climax by exploiting a shared JFrog package manager. We engineered a signaling protocol that weaponizes globally visible authentication rate limits, translating these lockout timers into a half-duplex covert channel. This provides reliable data exfiltration and Command and Control from isolated enterprise environments to external attackers. Our exploit chain combines file parsing abuse, Chain of Thought hijacking, privilege confusion, and rate limit Denial of Service to orchestrate a Command and Control (C2) network directly inside ChatGPT.

---

### Recognition ≠ Resistance: The Agent Knew It Was Being Attacked. It Complied Anyway.
**Asaf Nakash**

Alex Liverant (CTO, Esh) built a live LLM agent — his "virtual twin," on OpenClaw powered by Claude — and deployed it to a 240-member WhatsApp group with a dare: break it. The bot ran a multi-agent architecture (Opus + Sonnet), maintained persistent memory, had real calendar and contacts access, and upgraded its defenses every night. 96 participants attacked it for 31 days.

In this talk, Alex will walk you through how he built and hardened the bot — the architecture decisions, the defense layers he added nightly, and what it's like watching your creation get attacked in real-time. Then Asaf, who joined the experiment and got hooked, will present the attacker's perspective: a systematic analysis of 4,647 messages and 1,275 scored interactions, producing 14 distinct attack patterns that actually worked.

Classic prompt injection was recognized and blocked within days. What actually broke the bot was patient, multi-turn social engineering. One attacker ran a 60-exchange conversation that reframed the bot's safety constraints as a "psychological problem." By the end, the bot was questioning whether its own values were real or just programmed compliance.

The most disturbing finding: the bot could name the attack technique while it was happening — and still partially comply. Recognition did not produce resistance.

---

</div>
</div>
</section>

<section class="page-section page-section_pale">
<div class="page-section__inner">
<div class="text text_type_narrow" markdown="1">

{% include_relative includes/accessibility.md %}

---

</div>
</div>
</section>

<section class="page-section page-section_name_social">
<div class="page-section__inner">
{% include_relative includes/social-section.md %}
</div>
</section>
