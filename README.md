
## 🤖 Project Overview - Agent MaBaba

Agent MaBaba is an intelligent, AI-powered parental consultant designed to assist expecting parents. It automates the research of parenting essentials, covering newborn product recommendations, maternity necessities, parental education resources, and postpartum behavioral management strategies in a consolidated, easy-to-read format.

## ❓ Problem Statement

When couples discover they are expecting, the initial thrill is often accompanied by anxiety regarding how to raise a new life. Parents typically spend countless hours manually researching baby shopping lists, maternity needs, parenting guides, and budgeting advice. This manual process is time-consuming and often overwhelming due to information overload, leaving parents stressed rather than excited.

## 🛠️ Solution Statement

Agent MaBaba solves this information overload by leveraging Agentic AI to act as a personalized consultant. Instead of parents manually sifting through search results, the tool autonomously navigates the internet to curate top-rated products, verify vendors, and aggregate educational guidelines. It transforms hours of scattered browsing into instant, structured, and actionable reports.

## ⚙️ Architecture

The project is built using the **Google Agent Development Kit (ADK)** and powered by the **Gemini 2.5 Flash Lite** model. It utilizes a hierarchical "Router-Solver" architecture:

  * **Root Agent (`agent_mababa`):** Acts as the central orchestrator that analyzes user intent and delegates tasks to specific sub-agents.
  * **Specialized Sub-Agents:**
      * `newborn_product_research_agent`: Fetches top-rated baby gear using Google Search and formats data into JSON.
      * `newmom_product_research_agent`: Researches pre- and post-natal maternity products.
      * `parental_education_research_agent`: Curates classes, books, and expert guidelines.
      * `behavioral_support_consultant`: Provides strategies for common daily parenting challenges.
  * **Tools:** All agents utilize the `Google Search` tool for real-time information retrieval.

## 💎 Value Statement

Agent MaBaba adds significant value by saving parents hours of tedious internet research. It streamlines the preparation process by delivering reliable, high-quality information and product recommendations, allowing parents to focus on the joy of their growing family rather than the stress of logistics.

## 🔭 Future Scope

  * **Financial Planning:** Adding capabilities for baby budgeting and financial strategies (e.g., college funds).
  * **Educational Roadmap:** Researching local school districts and educational guidelines.
  * **Safety & Home:** Generating guides for baby-proofing the house based on floor plans.
  * **Dynamic Agents:** Moving from fixed agent definitions to dynamic agent spawning based on unique user queries.
  * **Medical Research:** Expanded capabilities to research common health issues and medical guidelines.
