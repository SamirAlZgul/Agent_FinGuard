

"""
MCP клиент для подключения к финансовым данным
Это отдельный модуль, который будет работать как мост между нашим агентом и внешними API
Когда что-то надо будет изменить - добавить внешний API, то изменяем в этом файле как функции MCP,
логика агента остается нетронутой
"""
"""
MCP клиент для подключения к финансовым данным.
ИСПРАВЛЕНО: теперь правильно обрабатывает асинхронные вызовы
"""

import json
import asyncio
from typing import Dict, Any, Optional
import yfinance as yf
import traceback


class MCPFinanceClient:
    """
    MCP клиент для финансовых данных.
    """
    def __init__(self):
        self.connected = False
        self._loop = None
        print("🔄 MCP Client initialized")

    async def connect(self):
        """Устанавливаем соединение с MCP сервером."""
        self.connected = True
        print("✅ MCP Client connected")
        return self

    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Единая точка входа для всех инструментов.
        ИСПРАВЛЕНО: добавил обработку ошибок и логирование
        """
        try:
            print(f"🔧 MCP executing: {tool_name} with {params}")

            if not self.connected:
                await self.connect()

            # Маршрутизация запросов к разным API
            if tool_name == "get_stock_price":
                return await self._get_stock_price(params.get("ticker"))
            elif tool_name == "get_company_info":
                return await self._get_company_info(params.get("ticker"))
            elif tool_name == "get_historical_data":
                return await self._get_historical_data(
                    params.get("ticker"),
                    params.get("period", "1mo")
                )
            elif tool_name == "get_financial_ratios":
                return await self._get_financial_ratios(params.get("ticker"))
            else:
                return {"error": f"Unknown tool: {tool_name}", "status": "error"}
        except Exception as e:
            print(f"❌ MCP error in {tool_name}: {str(e)}")
            traceback.print_exc()
            return {"error": str(e), "status": "error", "tool": tool_name}

    async def _get_stock_price(self, ticker: str) -> Dict[str, Any]:
        """Получить цену акции"""
        try:
            print(f"📊 Fetching price for {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get('regularMarketPrice', info.get('currentPrice', 'N/A'))

            result = {
                "ticker": ticker,
                "price": float(price) if price != 'N/A' else None,
                "currency": "USD",
                "source": "Yahoo Finance via MCP",
                "status": "success"
            }
            print(f"✅ Got price for {ticker}: ${result['price']}")
            return result
        except Exception as e:
            print(f"❌ Error fetching price for {ticker}: {e}")
            return {"error": str(e), "ticker": ticker, "status": "error"}

    async def _get_company_info(self, ticker: str) -> Dict[str, Any]:
        """Расширенная информация о компании"""
        try:
            print(f"📊 Fetching company info for {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info

            result = {
                "ticker": ticker,
                "name": info.get('longName', 'N/A'),
                "sector": info.get('sector', 'N/A'),
                "industry": info.get('industry', 'N/A'),
                "country": info.get('country', 'N/A'),
                "website": info.get('website', 'N/A'),
                "business_summary": str(info.get('longBusinessSummary', 'N/A'))[:200] + "...",
                "employees": info.get('fullTimeEmployees', 'N/A'),
                "status": "success"
            }
            print(f"✅ Got company info for {ticker}")
            return result
        except Exception as e:
            print(f"❌ Error fetching company info for {ticker}: {e}")
            return {"error": str(e), "ticker": ticker, "status": "error"}

    async def _get_historical_data(self, ticker: str, period: str) -> Dict[str, Any]:
        """Получить исторические данные"""
        try:
            print(f"📊 Fetching historical data for {ticker}, period={period}...")
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)

            if hist.empty:
                return {"error": f"No data for {ticker}", "status": "error"}

            # Рассчитываем метрики
            prices = []
            volumes = []
            for date, row in hist.iterrows():
                prices.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"])
                })
                volumes.append(int(row["Volume"]))

            # Вычисляем средний объем
            avg_volume = sum(volumes) / len(volumes) if volumes else 0
            latest_price = float(hist["Close"].iloc[-1])

            # Вычисляем изменение
            price_change = float(hist["Close"].iloc[-1] - hist["Close"].iloc[0]) if len(hist) > 1 else 0
            price_change_pct = float((hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100) if len(hist) > 1 else 0

            result = {
                "ticker": ticker,
                "period": period,
                "data_points": len(prices),
                "latest_price": latest_price,
                "avg_daily_volume": int(avg_volume),
                "avg_daily_volume_usd": float(avg_volume * latest_price),
                "price_change": {
                    "abs": round(price_change, 2),
                    "pct": round(price_change_pct, 2)
                },
                "status": "success"
            }
            print(f"✅ Got historical data for {ticker}: {result['data_points']} points")
            return result
        except Exception as e:
            print(f"❌ Error fetching historical data for {ticker}: {e}")
            traceback.print_exc()
            return {"error": str(e), "ticker": ticker, "status": "error"}

    async def _get_financial_ratios(self, ticker: str) -> Dict[str, Any]:
        """Получить финансовые коэффициенты"""
        try:
            print(f"📊 Fetching financial ratios for {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info

            result = {
                "ticker": ticker,
                "valuation": {
                    "pe_ratio": info.get('trailingPE', 'N/A'),
                    "forward_pe": info.get('forwardPE', 'N/A'),
                    "peg_ratio": info.get('pegRatio', 'N/A'),
                    "price_to_book": info.get('priceToBook', 'N/A'),
                    "price_to_sales": info.get('priceToSalesTrailing12Months', 'N/A')
                },
                "profitability": {
                    "profit_margin": info.get('profitMargins', 'N/A'),
                    "operating_margin": info.get('operatingMargins', 'N/A'),
                    "return_on_equity": info.get('returnOnEquity', 'N/A'),
                    "return_on_assets": info.get('returnOnAssets', 'N/A')
                },
                "liquidity": {
                    "current_ratio": info.get('currentRatio', 'N/A'),
                    "quick_ratio": info.get('quickRatio', 'N/A'),
                    "debt_to_equity": info.get('debtToEquity', 'N/A')
                },
                "status": "success"
            }
            print(f"✅ Got financial ratios for {ticker}")
            return result
        except Exception as e:
            print(f"❌ Error fetching financial ratios for {ticker}: {e}")
            return {"error": str(e), "ticker": ticker, "status": "error"}

    async def close(self):
        """Закрываем соединение"""
        self.connected = False
        print("🔌 MCP Client disconnected")


# Создаем глобальный экземпляр
mcp_client = MCPFinanceClient()