import streamlit as st
import requests
import json
from datetime import datetime

# Настройка страницы
st.set_page_config(
    page_title="FinGuard AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# API endpoint - ИСПРАВЛЕНО на 127.0.0.1
API_URL = "http://127.0.0.1:8000"

# Инициализация session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    import uuid

    st.session_state.session_id = str(uuid.uuid4())
if "tools_used" not in st.session_state:
    st.session_state.tools_used = []

# Заголовок
st.title("🤖 FinGuard AI - Финансовый помощник")
st.markdown("---")

# Боковая панель
with st.sidebar:
    st.header("⚙️ Настройки")

    # Проверка подключения к API
    try:
        health = requests.get(f"{API_URL}/health", timeout=2)
        if health.status_code == 200:
            st.success("✅ API подключен")
        else:
            st.error("❌ API не отвечает")
    except Exception as e:
        st.error(f"❌ API не доступен")

    st.markdown("---")

    # Информация о сессии
    st.subheader("📋 Сессия")
    st.code(st.session_state.session_id)

    if st.button("🆕 Новая сессия"):
        import uuid

        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.tools_used = []
        st.rerun()

    st.markdown("---")

    # Доступные команды
    st.subheader("📚 Доступные компании")

    with st.expander("Реальные компании (Yahoo Finance)"):
        st.markdown("""
        - Apple (AAPL)
        - Microsoft (MSFT)
        - Tesla (TSLA)
        - Google (GOOGL)
        - Amazon (AMZN)
        """)

    with st.expander("Выдуманные компании (RAG документы)"):
        st.markdown("""
        - TechNova (TNVA)
        - QuantumLeap (QLEAP)
        - CapitalGuard (CGUARD)
        - Apex (APEX)
        - BioVita (BVITA)
        - GenoMedix (GMDX)
        - NovaStar (NOVA)
        - GreenFuture (GFR)
        - OmniConsumer (OMNI)
        - LuxeRetail (LUXE)
        - Industrial Dynamics (IDYN)
        - AeroSpace (AERO)
        """)

    st.markdown("---")

    # Примеры запросов
    st.subheader("💡 Примеры запросов")
    examples = [
        "цена акций apple",
        "расскажи о компании microsoft",
        "информация о technova",
        "сколько выручка у quantumleap",
        "сравни biovita и genomedix",
        "какие компании ты знаешь"
    ]

    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state["example"] = ex
            st.rerun()

# Основной чат
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "tools" in message and message["tools"]:
            with st.expander("🛠️ Использованные инструменты"):
                st.write(message["tools"])

# Поле ввода
prompt = st.chat_input("Введите ваш вопрос о финансах...")

# Обработка примера из боковой панели
if "example" in st.session_state:
    prompt = st.session_state.pop("example")

if prompt:
    # Добавляем сообщение пользователя
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Отправляем запрос к API
    with st.chat_message("assistant"):
        with st.spinner("🤔 Анализирую запрос..."):
            try:
                response = requests.post(
                    f"{API_URL}/agent/run",
                    json={
                        "text": prompt,
                        "session_id": st.session_state.session_id
                    },
                    timeout=200
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data["response"]
                    tools = data.get("tools_used", [])

                    # Отображаем ответ
                    st.markdown(answer)

                    # Показываем использованные инструменты
                    if tools:
                        with st.expander("🛠️ Использованные инструменты"):
                            st.write(tools)

                    # Сохраняем в историю
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "tools": tools
                    })
                else:
                    st.error(f"Ошибка API: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Не удалось подключиться к API")
            except Exception as e:
                st.error(f"❌ Ошибка: {str(e)}")

# Подвал
st.markdown("---")
st.markdown("🔒 FinGuard AI - Ваш персональный финансовый помощник")