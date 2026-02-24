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







