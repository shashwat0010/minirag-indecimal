# RAG Benchmark Report: OpenRouter vs Local LLM (TinyLlama)

## Summary Statistics
- **Avg OpenRouter Latency:** 2.12s
- **Avg Local LLM Latency:** 20.84s

### Key Findings
- **OpenRouter (Cloud)**: Significantly faster (avg 2.1s) and strictly follows the "Not specified in documents" rule. It is highly grounded and avoids hallucination by refusing to answer missing info.
- **Local LLM (TinyLlama)**: Much slower on CPU (avg 20.8s) and prone to hallucination. For example, it picked up cement bag prices (₹370/bag) as the "booking amount" and invented a document date ("January 31st, 2022").

## Detailed Comparison

### What is the one-line summary of Indecimal?
**OpenRouter Answer (Latency: 2.23s):**
Indecimal provides end-to-end home construction support with transparent pricing, quality assurance, and structured project tracking from inquiry to handover.

**Local LLM Answer (Latency: 12.64s):**
Indecimal promises transparency, timely delivery, and affordable pricing for home construction projects.

**Retrieved Chunks Used:** 3

---

### What are the three package pricing levels per sqft?
**OpenRouter Answer (Latency: 2.60s):**
- Essential: ₹1,851 /sqft (incl. GST)
- Premier (Most Popular): ₹1,995 /sqft (incl. GST)
- Infinia: ₹2,250 /sqft (incl. GST)

**Local LLM Answer (Latency: 31.51s):**
These are shown as per-sqft package rates (inclusive of GST) on the public comparison page: Essential: ₹1,851 /sqft (incl. GST), Premier (most popular): ₹1,995 /sqft (incl. GST), and Infinia: ₹2,250 /sqft (incl. GST).

**Retrieved Chunks Used:** 3

---

### What does Indecimal promise to build instead of just contracts?
**OpenRouter Answer (Latency: 1.78s):**
- Indecimal promises to build confidence instead of just contracts.

**Local LLM Answer (Latency: 9.59s):**
Confidentiality, transparency, and timely delivery.

**Retrieved Chunks Used:** 3

---

### What are the specification wallets for flooring in the Premier package?
**OpenRouter Answer (Latency: 2.02s):**
- For living & dining flooring in the Premier package:
  - Tiles/granite up to ₹100/sqft

- For rooms & kitchen flooring in the Premier package:
  - Tiles/granite up to ₹80/sqft

**Local LLM Answer (Latency: 14.46s):**
The Premier package includes tiles and granite/marble up to ₹100/sqft.

**Retrieved Chunks Used:** 3

---

### What is the booking amount for the design phase?
**OpenRouter Answer (Latency: 2.00s):**
- Not specified in the provided documents.

**Local LLM Answer (Latency: 11.55s):**
The booking amount for the design phase is up to ₹370/bag.

**Retrieved Chunks Used:** 3

---

### What is the 'Premier' package price per sqft including GST?
**OpenRouter Answer (Latency: 1.80s):**
- The 'Premier' package price per sqft including GST is ₹1,995.

**Local LLM Answer (Latency: 14.10s):**
It is mentioned that these packages include GST and show an indicative pricing for each package type.

**Retrieved Chunks Used:** 3

---

### What are the internal reference details for the Audience of the documents?
**OpenRouter Answer (Latency: 1.90s):**
The internal reference details for the Audience of the documents are:
- Audience: Support, Sales, Product, and AI Assistant Knowledge Base

**Local LLM Answer (Latency: 11.43s):**
The audience is Support, Sales, Product, and AI Assistant Knowledge Base.

**Retrieved Chunks Used:** 3

---

### How does Indecimal handle project tracking from inquiry to handover?
**OpenRouter Answer (Latency: 2.96s):**
- Indecimal provides real-time construction progress tracking.
- It offers live photo updates through its app/dashboard for project monitoring.
- Transparency is maintained through clear agreements and real-time online project tracking.
- Payments to contractors are stage-based and released only after verified completion.

**Local LLM Answer (Latency: 73.87s):**
Q: Can you explain how Indecimal tracks projects from inquiry to handover? A: Yes! Here's an example of how they track projects:

Inquiry: I am interested in starting my new home build project.

Response: We will be happy to help you get started by scheduling a consultation call at your convenience. During this call, we can discuss your specific needs and goals for your new home build project. Based on our discussion, we will create a customized plan tailored specifically to meet your unique requirements. This plan includes all necessary details such as scope, timelines, budget, and any other relevant information required for the project. After the initial consultation, we will send you a proposal outlining the proposed project scope, timeline, and estimated costs. Our team will work closely with you throughout the entire project lifecycle to ensure that everything stays within budget and meets your expectations. Handover: Once the project has been completed successfully, we will deliver the final product to your doorstep. At this point, we will also perform a final inspection to ensure that everything was done according to your satisfaction. In summary, Indecimal offers complete transparency during every step of the project lifecycle, including project tracking from inquiry to handover.

**Retrieved Chunks Used:** 3

---

### What is the audience for the Package Comparison document?
**OpenRouter Answer (Latency: 2.09s):**
The audience for the Package Comparison document is Sales, Estimation, and the AI Assistant Knowledge Base.

**Local LLM Answer (Latency: 19.68s):**
The internal reference document serves as an overview of the company's packages and their pricing structure. It provides information about the different packages offered by the company, including their indicative/per sqft prices, structure specifications, and customer journeys.

**Retrieved Chunks Used:** 3

---

### What is the last updated date of the documents?
**OpenRouter Answer (Latency: 1.85s):**
Not specified in the provided documents.

**Local LLM Answer (Latency: 9.54s):**
The last updated date of the documents is January 31st, 2022.

**Retrieved Chunks Used:** 3

---

