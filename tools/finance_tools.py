import asyncio
import nest_asyncio
nest_asyncio.apply()
import os
import traceback
import yfinance as yf
from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
import uuid  # используется в интерактивном режиме

from mcp_client import mcp_client
from rag_knowledge_base import rag_db
# Загружаем переменные окружения из .env файла
load_dotenv()

import sys
import io

# Принудительно устанавливаем кодировку вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='ignore')

# Также установим переменные окружения
os.environ['PYTHONIOENCODING'] = 'utf-8'

import codecs

def safe_str(obj) -> str:
    """Безопасно преобразует любой объект в строку, игнорируя ошибки кодировки"""
    try:
        if obj is None:
            return ""
        if isinstance(obj, str):
            # Уже строка - очищаем
            return obj.encode('utf-8', errors='ignore').decode('utf-8')
        # Преобразуем в строку и очищаем
        return str(obj).encode('utf-8', errors='ignore').decode('utf-8')
    except:
        return "[Ошибка преобразования строки]"

def clean_messages(messages_list):
    """Очищает все сообщения от проблемных символов"""
    cleaned = []
    for msg in messages_list:
        try:
            if hasattr(msg, "content"):
                msg.content = safe_str(msg.content)
            elif isinstance(msg, dict) and "content" in msg:
                msg["content"] = safe_str(msg["content"])
            cleaned.append(msg)
        except:
            continue
    return cleaned


# ============================================
# 2. НАСТРОЙКА МОДЕЛИ
# ============================================
class StreamingCallback(BaseCallbackHandler):
    """Кастомный колбэк для вывода в консоль в реальном времени."""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(token, end="", flush=True)

    def on_agent_action(self, action: AgentAction, **kwargs) -> None:
        print(f"\n\n🔧 Action: {action.tool}")
        print(f"📝 Input: {action.tool_input}")

    def on_agent_finish(self, finish: AgentFinish, **kwargs) -> None:
        print(f"\n\n✅ Final: {finish.return_values['output']}")


# llm = ChatOpenAI(
#     base_url="https://router.huggingface.co/v1/",
#     api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
#     model="deepseek-ai/DeepSeek-R1-0528",
#     temperature=0.1,
#     streaming=True,
#     callbacks=[StreamingCallback()]
# )

llm = ChatOllama(
    model="llama3.1:8b",  # или "mistral", "qwen2.5"
    temperature=0.1,
    streaming=True,
    callbacks=[StreamingCallback()]
)

# ============================================
# 3. СОЗДАНИЕ PROMPT ДЛЯ REACT АГЕНТА (ИСПРАВЛЕН)
# ============================================

react_prompt = ChatPromptTemplate.from_messages([
    ("system", """
Ты - финансовый помощник FinGuard AI. У тебя есть ДВА ТИПА инструментов:

1. ИНСТРУМЕНТЫ ДЛЯ РЕАЛЬНЫХ КОМПАНИЙ (через Yahoo Finance):
   - get_stock_price_mcp: получить текущую цену акции
   - get_company_info_mcp: базовая информация о компании
   - get_historical_data_mcp: исторические данные
   - get_financial_ratios_mcp: финансовые коэффициенты
   ЭТИ ИНСТРУМЕНТЫ РАБОТАЮТ ТОЛЬКО ДЛЯ РЕАЛЬНЫХ КОМПАНИЙ (AAPL, MSFT, TSLA)

2. ИНСТРУМЕНТ ДЛЯ ВЫДУМАННЫХ КОМПАНИЙ (через RAG):
   - search_financial_docs: ПОИСК В ДОКУМЕНТАХ ПО НАШИМ ВЫДУМАННЫМ КОМПАНИЯМ
   ЭТОТ ИНСТРУМЕНТ РАБОТАЕТ ДЛЯ: TechNova, QuantumLeap, CapitalGuard, Apex, BioVita, GenoMedix, NovaStar, GreenFuture, OmniConsumer, LuxeRetail, Industrial Dynamics, AeroSpace

ВАЖНО: Если пользователь спрашивает про TechNova, QuantumLeap и другие выдуманные компании - используй ТОЛЬКО search_financial_docs!

ПРИМЕР 1 (реальная компания):
Question: цена акций microsoft
Thought: Microsoft (MSFT) - реальная компания, использую get_stock_price_mcp
Action: get_stock_price_mcp
Action Input: {{"ticker": "MSFT"}}
Observation: The current price of MSFT is $415.50
Final Answer: Текущая цена акций Microsoft составляет $415.50

ПРИМЕР 2 (выдуманная компания):
Question: информация о компании technova
Thought: TechNova - выдуманная компания из наших документов, нужно искать в RAG
Action: search_financial_docs
Action Input: {{"query": "TechNova company overview"}}
Observation: [Источник: technova_q1_2023.txt] TechNova Inc. is a leading provider of cloud infrastructure...
Final Answer: TechNova Inc. - поставщик облачной инфраструктуры с выручкой $24.3 млрд в Q1 2023.

ПРИМЕР 3 (список компаний):
Question: информацию о каких компаниях ты знаешь
Thought: Нужно показать список доступных компаний из наших документов
Action: search_financial_docs
Action Input: {{"query": "list of companies in database"}}
Observation: [Источник: technology_investment_outlook.txt] TechNova, QuantumLeap, CapitalGuard, Apex...
Final Answer: Я знаю информацию о следующих выдуманных компаниях: TechNova, QuantumLeap, CapitalGuard, Apex, BioVita, GenoMedix, NovaStar, GreenFuture, OmniConsumer, LuxeRetail, Industrial Dynamics, AeroSpace. Также я могу получить данные о реальных компаниях через Yahoo Finance (например, AAPL, MSFT, TSLA).

ПРИМЕР 4 (сравнение):
Question: сравни technova и quantumleap
Thought: Обе компании выдуманные, нужно искать в документах
Action: search_financial_docs
Action Input: {{"query": "TechNova vs QuantumLeap comparison"}}
Observation: [Источник: technology_investment_outlook.txt] TechNova focuses on cloud, QuantumLeap on AI chips...
Final Answer: TechNova специализируется на облаке (выручка $24.3 млрд), QuantumLeap - на AI чипах (выручка $8.7 млрд).

ПРАВИЛА:
1. Для реальных тикеров (AAPL, MSFT, TSLA, GOOGL, AMZN) - используй MCP инструменты
2. Для выдуманных компаний (TechNova, QuantumLeap и др.) - используй search_financial_docs
3. Если не уверен - сначала используй search_financial_docs для поиска в документах
4. Никогда не оставляй Action без Observation!
"""),
    MessagesPlaceholder(variable_name="messages"),
])


# ============================================
# 4. ОПРЕДЕЛЕНИЕ ИНСТРУМЕНТОВ
# ============================================
@tool
def get_stock_price_mcp(ticker: str) -> str:
    """
    Get current stock price using MCP protocol.

    Args:
        ticker: Stock ticker symbol (e.g., AAPL, MSFT)
    """
    try:
        print(f"🔧 Executing get_stock_price_mcp for {ticker}")

        # СОЗДАЕМ НОВЫЙ ЦИКЛ ДЛЯ КАЖДОГО ВЫЗОВА
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Подключаемся и вызываем инструмент
        loop.run_until_complete(mcp_client.connect())
        result = loop.run_until_complete(mcp_client.call_tool("get_stock_price", {"ticker": ticker}))
        loop.run_until_complete(mcp_client.close())
        loop.close()

        if "error" in result:
            return f"Error: {result['error']}"

        return f"The current price of {result['ticker']} is ${result['price']:.2f}"
    except Exception as e:
        print(f"❌ Error in get_stock_price_mcp: {e}")
        traceback.print_exc()
        return f"Error calling MCP: {str(e)}"


@tool
def get_company_info_mcp(ticker: str) -> str:
    """
    Get detailed company information using MCP.

    Args:
        ticker: Stock ticker symbol
    """
    try:
        print(f"🔧 Executing get_company_info_mcp for {ticker}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(mcp_client.connect())
        result = loop.run_until_complete(mcp_client.call_tool("get_company_info", {"ticker": ticker}))
        loop.run_until_complete(mcp_client.close())
        loop.close()

        if "error" in result:
            return f"Error: {result['error']}"

        return f"""
Company: {result.get('name', 'N/A')}
Sector: {result.get('sector', 'N/A')}
Industry: {result.get('industry', 'N/A')}
Country: {result.get('country', 'N/A')}
Employees: {result.get('employees', 'N/A')}
Summary: {result.get('business_summary', 'N/A')}
        """.strip()
    except Exception as e:
        print(f"❌ Error in get_company_info_mcp: {e}")
        return f"Error calling MCP: {str(e)}"


@tool
def get_historical_data_mcp(ticker: str, period: str = "1mo") -> str:
    """
    Get historical stock data using MCP.

    Args:
        ticker: Stock ticker symbol
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y)
    """
    try:
        print(f"🔧 Executing get_historical_data_mcp for {ticker}, period={period}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(mcp_client.connect())
        result = loop.run_until_complete(mcp_client.call_tool(
            "get_historical_data",
            {"ticker": ticker, "period": period}
        ))
        loop.run_until_complete(mcp_client.close())
        loop.close()

        if "error" in result:
            return f"Error: {result['error']}"

        change = result.get('price_change', {})
        volume = result.get('avg_daily_volume_usd', 0)

        return f"""
📊 {ticker} ({period}):
   Latest: ${result.get('latest_price', 'N/A')}
   Change: {change.get('pct', 0):.1f}% (${change.get('abs', 0):.2f})
   Avg Daily Volume: ${volume:,.0f}
   Data points: {result.get('data_points', 0)}
        """.strip()
    except Exception as e:
        print(f"❌ Error in get_historical_data_mcp: {e}")
        traceback.print_exc()
        return f"Error calling MCP: {str(e)}"


@tool
def get_financial_ratios_mcp(ticker: str) -> str:
    """
    Get key financial ratios using MCP.

    Args:
        ticker: Stock ticker symbol
    """
    try:
        print(f"🔧 Executing get_financial_ratios_mcp for {ticker}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(mcp_client.connect())
        result = loop.run_until_complete(mcp_client.call_tool("get_financial_ratios", {"ticker": ticker}))
        loop.run_until_complete(mcp_client.close())
        loop.close()

        if "error" in result:
            return f"Error: {result['error']}"

        valuation = result.get('valuation', {})
        profitability = result.get('profitability', {})
        liquidity = result.get('liquidity', {})

        return f"""
📊 Financial Ratios for {ticker}:

📈 Valuation:
   P/E: {valuation.get('pe_ratio', 'N/A')}
   Forward P/E: {valuation.get('forward_pe', 'N/A')}
   P/B: {valuation.get('price_to_book', 'N/A')}

💰 Profitability:
   Profit Margin: {profitability.get('profit_margin', 'N/A')}
   ROE: {profitability.get('return_on_equity', 'N/A')}

💧 Liquidity:
   Current Ratio: {liquidity.get('current_ratio', 'N/A')}
   Debt/Equity: {liquidity.get('debt_to_equity', 'N/A')}
        """.strip()
    except Exception as e:
        print(f"❌ Error in get_financial_ratios_mcp: {e}")
        return f"Error calling MCP: {str(e)}"


# finance_tools.py (добавить новый инструмент)
@tool
def search_financial_docs(query: str) -> str:
    """
    Search financial documents, reports, and analysis using RAG.
    Use this for questions about company strategies, financial reports, market analysis,
    or any information not available in real-time stock data.

    Args:
        query: The search query (e.g., "Apple AI strategy", "Microsoft cloud revenue growth")
    """
    try:
        print(f"🔍 RAG search: '{query}'")

        # Выполняем поиск
        results = rag_db.search(query, k=3)

        if not results:
            return "No relevant documents found. Please try a different query."

        # Формируем ответ с найденными документами
        response = f"📚 Found {len(results)} relevant documents:\n\n"
        response += "\n---\n".join(results)

        print(f"✅ RAG search returned {len(results)} results")
        return response

    except Exception as e:
        print(f"❌ Error in RAG search: {e}")
        traceback.print_exc()
        return f"Error searching documents: {str(e)}"

# ============================================
# 5. СОБИРАЕМ НОВЫЕ ИНСТРУМЕНТЫ
# ============================================
# Концепция: заменяем старые инструменты (get_stock_price, get_company_info)
# на новые MCP инструменты. Старые пока оставим для обратной совместимости.
tools = [
    get_stock_price_mcp,      # новый через MCP
    get_company_info_mcp,      # новый через MCP
    get_historical_data_mcp,   # совершенно новый инструмент
    get_financial_ratios_mcp,  # совершенно новый инструмент
    search_financial_docs,
    # Старые инструменты пока можно закомментировать
    # get_stock_price,
    # get_company_info,
]
# ============================================
# 5. СОЗДАНИЕ АГЕНТА (БЕЗ AgentExecutor!)
# ============================================
checkpointer = InMemorySaver()
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=react_prompt,
    checkpointer=checkpointer
)
print("agent", agent)

print("✅ Agent created successfully with MCP tools!")


# ============================================
# 7. ФУНКЦИЯ ЗАПУСКА (ОБНОВЛЕНА)
# ============================================
def run_agent(query: str, thread_id: str = "1") -> str:
    """
    Run the agent with a user query.
    """
    try:
        # Очищаем входной запрос
        clean_query = safe_str(query)
        print(f"\n📌 Query: {clean_query}")
        print("=" * 50)
        print("🔄 Анализирую запрос...")

        messages = [{"role": "user", "content": clean_query}]

        result = None
        error = None

        # Перехватываем все возможные ошибки
        try:
            # Дополнительная защита от проблем с кодировкой
            import sys
            import warnings
            warnings.filterwarnings("ignore")

            # Сохраняем оригинальные обработчики
            old_stdout = sys.stdout
            old_stderr = sys.stderr

            # Создаем обертки для stdout/stderr с игнорированием ошибок
            class SafeWriter:
                def __init__(self, stream):
                    self.stream = stream

                def write(self, data):
                    try:
                        self.stream.write(safe_str(data))
                    except:
                        pass

                def flush(self):
                    try:
                        self.stream.flush()
                    except:
                        pass

            sys.stdout = SafeWriter(old_stdout)
            sys.stderr = SafeWriter(old_stderr)

            # Вызываем агента
            result = agent.invoke(
                {"messages": messages},
                config={"configurable": {"thread_id": thread_id}}
            )

            # Восстанавливаем stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        except Exception as e:
            error = e
            # Восстанавливаем stdout/stderr в случае ошибки
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        # Если была ошибка при вызове
        if error:
            error_msg = safe_str(str(error))
            print(f"\n❌ Error: {error_msg}")
            return f"Произошла ошибка: {error_msg}"

        # Извлекаем ответ
        if isinstance(result, dict) and "messages" in result:
            messages_list = result["messages"]

            # Очищаем все сообщения
            messages_list = clean_messages(messages_list)

            # Ищем финальный ответ
            for msg in reversed(messages_list):
                try:
                    if hasattr(msg, "type") and msg.type == "ai":
                        content = getattr(msg, "content", "")
                        if content and not any(x in content for x in ["Action:", "Thought:", "get_", "mcp"]):
                            return safe_str(content)
                    elif isinstance(msg, dict) and msg.get("role") == "assistant":
                        content = msg.get("content", "")
                        if content and not any(x in content for x in ["Action:", "Thought:", "get_", "mcp"]):
                            return safe_str(content)
                except:
                    continue

            # Если не нашли чистый ответ, берем последнее
            try:
                if messages_list:
                    last_msg = messages_list[-1]
                    if hasattr(last_msg, "content"):
                        return safe_str(last_msg.content)
                    elif isinstance(last_msg, dict):
                        return safe_str(last_msg.get("content", str(last_msg)))
            except:
                pass

        return "Анализ выполнен. Задайте конкретный вопрос."

    except Exception as e:
        print(f"\n❌ Error: {safe_str(str(e))}")
        traceback.print_exc()
        return f"Произошла ошибка: {safe_str(str(e))}"
# ============================================
# 8. ТЕСТОВЫЙ РЕЖИМ (ОБНОВЛЕН)
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("FinGuard AI - Financial Assistant with MCP")
    print("=" * 60)
    print(f"Tools available: {[tool.name for tool in tools]}")
    print("=" * 60)

    # Тест модели
    print("\n🧪 Testing model directly...")
    try:
        test_msg = [{"role": "user", "content": "Say 'test'"}]
        test_response = llm.invoke(test_msg)
        print(f"✅ Model test successful!")
    except Exception as e:
        print(f"❌ Model test failed: {safe_str(str(e))}")

    # Тест MCP соединения
    print("\n🔌 Testing MCP connection...")
    try:
        test_result = asyncio.run(mcp_client.call_tool("get_stock_price", {"ticker": "AAPL"}))
        if "error" not in test_result:
            print(f"✅ MCP connection successful!")
            print(f"   Apple price: ${test_result.get('price', 'N/A')}")
        else:
            print(f"❌ MCP test failed: {test_result['error']}")
    except Exception as e:
        print(f"❌ MCP test failed: {safe_str(str(e))}")

    print("\n🔄 Starting interactive mode...")
    print("Type 'exit' to quit, 'new' for new conversation\n")
    print("💡 Try: 'Analyze Apple stock', 'Compare MSFT and AAPL', 'Get historical data for TSLA'")

    thread_id = "interactive_1"
    while True:
        try:
            user_input = input("\nYou: ").strip()

            # Очищаем ввод
            user_input = safe_str(user_input)

            if user_input.lower() == 'exit':
                print("Goodbye! 👋")
                break
            elif user_input.lower() == 'new':
                import uuid

                thread_id = str(uuid.uuid4())
                print(f"✨ New conversation (thread: {thread_id})")
                continue
            elif not user_input:
                continue

            result = run_agent(user_input, thread_id)
            # Очищаем результат перед выводом
            clean_result = safe_str(result)
            print(f"\n🤖 FinGuard: {clean_result}")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {safe_str(str(e))}")