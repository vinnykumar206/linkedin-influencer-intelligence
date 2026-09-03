# Architecture Overview: LinkedIn Influencer Intelligence System

## 1. Executive Summary

The **LinkedIn Influencer Intelligence System** is an enterprise-grade content intelligence pipeline. It continuously monitors target industry thought leadership feeds, extracts high-value business concepts, applies structured B2B framing models, and presents strategic content candidates for human approval and multi-channel publication.

---

## 2. End-to-End Signal Pipeline

```
┌───────────────────────────┐
│     LinkedIn Signals      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     Signal Collection     │  Headless web automation ingests market activity
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     Recency Filtering     │  48-hour timestamp verification gate
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       Deduplication       │  URN tracking prevents duplicate ingestion
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       Categorization      │  Dynamic LLM taxonomy classification
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│    Strategic Reframing    │  De-corporatization & idea extraction
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  Multiple Content Angles │  7-Angle Lab candidate competition
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       Human Review        │  Human-in-the-Loop mobile review & edits
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      Approved Output      │  Multi-format sync (Excel/JSON) & Publishing
└───────────────────────────┘
```

---

## 3. Major System Components & Roles

### 3.1 Signal Collection Engine
* **Role:** Navigates to targeted industry profile feeds and extracts raw post content.
* **Mechanism:** Employs headless browser session management with state preservation to navigate public and authenticated activity streams.
* **Outputs:** Raw post text, timestamp descriptors, URN metadata, and page screenshots for auditing.

### 3.2 Signal Filtering & Deduplication Layer
* **Role:** Ensures data quality, eliminates redundant processing, and keeps pipeline focused on fresh market insights.
* **Mechanism:**
  * **Recency Filter:** Evaluates relative time markers (e.g., rejecting posts older than 48 hours).
  * **History Tracking:** Matches post URNs against a persisted hash ledger to guarantee single-pass processing.

### 3.3 Dynamic Categorization Module
* **Role:** Classifies unstructured post content into a domain taxonomy.
* **Mechanism:** Prompts an LLM to evaluate the post semantics and return standardized topic categories (e.g., *Enterprise Sales, Sales Psychology, Leadership, AI & Automation*).

### 3.4 Strategic Reframing Engine (Engine 2.1)
* **Role:** Transforms raw influencer commentary into original, branded B2B thought leadership.
* **Mechanism:**
  * **Idea Extraction:** Decouples the underlying business premise from the original author's specific wording.
  * **7-Angle Lab:** Generates up to seven conceptual angles (*Contrarian, Counter-Intuitive, Field Experience, Operational Mechanism, CXO Perspective, Psychology, Tactical Lesson*).
  * **Three-Candidate Competition:** Internal competition across Contrarian, Experience/Story, and Observation candidates.
  * **De-corporatization Filter:** Scrubbing generic AI slop, corporate abstractions, and banned buzzwords in favor of concrete human dialogue.

### 3.5 Quality & Human Interest Gate
* **Role:** Ensures content meets high engagement and authority thresholds before reaching human reviewers.
* **Mechanism:** Evaluates post candidates across five human dimensions: Scroll-Stop Potential, Recognition, Curiosity, Tension, and Emotional Relevance. Applies a strict quality threshold (Minimum Human Interest Score $\ge 8.0/10$).

### 3.6 Human-in-the-Loop (HITL) Decision Layer
* **Role:** Guarantees zero unreviewed posts are published, maintaining complete executive control.
* **Mechanism:** Delivers interactive preview cards via mobile push notifications with action triggers:
  * **Approve/Publish:** Initiates distribution.
  * **Another Angle:** Triggers 7-Angle Lab to select an alternate candidate angle.
  * **Custom Edit:** Accepts natural language editorial feedback to re-run reframing logic.
  * **Media Upload:** Attaches user-provided image assets.

### 3.7 Distribution & Master Repository Layer
* **Role:** Manages final publication and builds a master database of market intelligence.
* **Mechanism:** Delivers payloads via official REST APIs or fallback browser automation while updating synchronized JSON, Markdown, and formatted Excel repositories.
