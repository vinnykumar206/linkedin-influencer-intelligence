# System Walkthrough & Interactive Demo Guide

This guide explains how to evaluate the **LinkedIn Influencer Intelligence System** without needing live LinkedIn session credentials or background API execution.

---

## 1. How the Pipeline Operates (Visual Walkthrough)

### Phase 1: Automated Background Ingestion
Every 48 hours, a scheduled task initiates headless ingestion:
1. Target profile feeds are accessed via Chromium.
2. Timestamp markers are evaluated to enforce a strict **48-hour recency window**.
3. Raw post texts are hashed and deduplicated against historic records.

### Phase 2: Dynamic Intelligence & Quality Gate
Once ingested, posts are sent to the AI Intelligence Engine:
1. **Taxonomy Analysis:** Categorizes topic themes (e.g., *Sales Strategy, Executive Leadership*).
2. **7-Angle Lab Evaluation:** Synthesizes original candidate posts.
3. **De-corporatization Audit:** Scrubs corporate buzzwords, em dashes, and generic hooks.

### Phase 3: Mobile Human-in-the-Loop Approval
Instead of auto-posting, the system issues an interactive push preview to the user's mobile device:

```text
📱 NEW MARKET SIGNAL INGESTED

Author: Industry Thought Leader
Category: Enterprise Sales Strategy
Source: [View Original Feed Signal]

Original Context:
"Rushing to demo software features immediately upon hearing customer complaints degrades seller authority."

👇 Select Action:
[ ✍️ Reframe Post ]   [ 💾 Save for Later ]   [ ⏭️ Skip ]
```

When the user taps **[ ✍️ Reframe Post ]**, the engine generates the refined asset and presents the approval card:

```text
✨ REFRAMED THOUGHT LEADERSHIP DRAFT

Quality Score: 92/100
Human Interest Score: 9.1/10
Selected Angle: Observation / Insight

Reframed Text:
"I've watched good salespeople lose enterprise deals while doing exactly what their playbook taught them..."

👇 Select Action:
[ 🚀 Publish Now ]   [ ✍️ Edit Text ]
[ 🔄 Another Angle ] [ 🖼️ Attach Media ]
[ 💾 Save for Later ] [ ❌ Discard ]
```

---

## 2. Master Repository Tracking

Every decision (Approve, Skip, Re-angle, Save) automatically updates synchronized data files:
* **`repository_list.json`**: Structured dataset for programatic analytics.
* **`repository_list.md`**: Human-readable documentation ledger.
* **`repository_list.xlsx`**: Executive-ready spreadsheet complete with corporate formatting, score metrics, and topic filters.

---

## 3. Key Design Takeaways for Evaluators

1. **Zero Uncontrolled AI Output:** The system prioritizes brand safety through mobile human-in-the-loop validation.
2. **Anti-Slop Quality Focus:** Reframing rules force concrete human language over generic corporate boilerplate.
3. **Executive Dashboard Ready:** Data is logged into reporting-ready spreadsheets for executive overview.
