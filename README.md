# 🤖 FinGuard AI - Intelligent Financial Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" alt="Python 3.11">
  <img src="https://img.shields.io/badge/LangChain-0.2-green?style=for-the-badge&logo=langchain" alt="LangChain">
  <img src="https://img.shields.io/badge/Streamlit-1.28-red?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/FastAPI-0.104-teal?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Ollama-llama3.1-yellow?style=for-the-badge&logo=llama" alt="Ollama">
  <img src="https://img.shields.io/badge/ChromaDB-0.4-purple?style=for-the-badge" alt="ChromaDB">
</p>

<p align="center">
  <b>FinGuard AI</b> is an intelligent financial assistant that combines real-time financial data (Yahoo Finance) with synthetic document analysis through RAG (Retrieval-Augmented Generation).
</p>

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Architecture & Workflow](#-architecture--workflow)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Available Companies](#-available-companies)
- [API Endpoints](#-api-endpoints)
- [Query Examples](#-query-examples)
- [RAG Knowledge Base](#-rag-knowledge-base)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

---

## 🔍 Project Overview

**FinGuard AI** is a hybrid financial assistant capable of working with two types of data:

1. **Real Companies** - retrieving up-to-date financial data via Yahoo Finance API (stock prices, company information, historical data, financial ratios)

2. **Synthetic/Fictional Companies** - analyzing financial documents through RAG (Retrieval-Augmented Generation) using ChromaDB vector database

The project demonstrates the capabilities of modern AI agents in the financial domain and serves as a testing platform for various approaches to financial information processing.

---

## 🏗 Architecture & Workflow
![Query plan](https://github.com/SamirAlZgul/Agent_FinGuard/blob/dev/query_plan.png?raw=true)

### 📋 Detailed Interaction Flow

| Step | From | To | Action | Data Format |
|------|------|----|--------|-------------|
| **1** | **User** | **Streamlit UI** | Query entered in chat interface | `string` (natural language) |
| **2** | **Streamlit** | **FastAPI Server** | HTTP POST request to `/agent/run` | `JSON: {"text": "query", "session_id": "uuid"}` |
| **3** | **FastAPI** | **Agent** | `run_agent()` function call | `(query: str, session_id: str) → str` |
| **4** | **Agent** | **LangGraph** | Create messages array and invoke agent | `{"messages": [{"role": "user", "content": query}]}` |
| **5** | **LangGraph** | **Ollama LLM** | Pass prompt to LLM for analysis | LangChain message format |
| **6** | **Ollama** | **LangGraph** | Return tool decision | ReAct format with Action/Action Input |
| **7** | **LangGraph** | **Tools** | Execute selected tool | Function call with parameters |
| **8** | **MCP Tools** | **Yahoo Finance** | Fetch real-time financial data | REST API call via `yfinance` |
| **9** | **RAG Tools** | **ChromaDB** | Semantic search in vector DB | `similarity_search_with_score()` |
| **10** | **Tools** | **LangGraph** | Return observation data | Formatted string with results |
| **11** | **LangGraph** | **Ollama LLM** | Send observation for final response | Observation + conversation history |
| **12** | **Ollama** | **LangGraph** | Generate natural language answer | `string` (final response) |
| **13** | **LangGraph** | **Agent** | Extract and process response | `AIMessage` object |
| **14** | **Agent** | **FastAPI** | Clean response with `safe_str()` | `string` (sanitized UTF-8) |
| **15** | **FastAPI** | **Streamlit** | Return JSON response | `{"response": "answer", "session_id": "uuid", "tools_used": [...]}` |
| **16** | **Streamlit** | **User** | Display message in chat | Rendered markdown in UI |

---

## ✨ Features

### 📊 Real Companies (Yahoo Finance)
- ✅ **Real-time stock prices** - current quotes retrieval
- ✅ **Company information** - profile, sector, industry, business description
- ✅ **Historical data** - prices for periods (1d, 5d, 1mo, 3mo, 6mo, 1y)
- ✅ **Financial ratios** - P/E, P/B, ROE, margins, and more

### 📚 Fictional Companies (RAG)
- ✅ **Document search** - semantic search in financial reports
- ✅ **30+ synthetic companies** - across various economic sectors
- ✅ **Quarterly and annual reports** - detailed financial information
- ✅ **Industry analysis reports** - macroeconomic insights
- ✅ **Company comparisons** - analysis across different metrics

### 🧠 AI Capabilities
- ✅ **ReAct agent** - action planning and execution
- ✅ **Local LLM** - Ollama with llama3.1:8b model
- ✅ **Context awareness** - conversation history tracking
- ✅ **Multi-tool orchestration** - combining different data sources

### 🖥️ User Interface
- ✅ **Chat interface** - intuitive conversation
- ✅ **Session history** - context preservation
- ✅ **Query examples** - quick start for new users
- ✅ **Tool visibility** - transparency about used tools
- ✅ **Sidebar** - information about available companies

---






