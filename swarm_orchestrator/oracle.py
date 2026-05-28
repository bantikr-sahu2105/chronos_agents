# import os
# import zmq
# import time
# import random
# import logging
# from google import genai
# from dotenv import load_dotenv

# load_dotenv()
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ORACLE] - %(message)s')

# client = genai.Client()

# NEWS_FEED = [
#     "Tech Giant reports record-breaking Q3 earnings, shattering Wall Street estimates.",
#     "Federal Reserve announces emergency rate cut of 100 bps.",
#     "Major pipeline explodes, disrupting global oil supply significantly.",
#     "Unemployment drops to historic lows, economy booming.",
#     "CEO of major simulated company resigns amidst massive accounting scandal.",
#     "Routine Tuesday: No major economic data released today."
# ]

# # THE PRODUCTION FALLBACK MATRIX
# # If the API fails, the system safely defaults to these scores.
# FALLBACK_SCORES = {
#     "Tech Giant reports record-breaking Q3 earnings, shattering Wall Street estimates.": 0.85,
#     "Federal Reserve announces emergency rate cut of 100 bps.": 0.75,
#     "Major pipeline explodes, disrupting global oil supply significantly.": -0.85,
#     "Unemployment drops to historic lows, economy booming.": 0.70,
#     "CEO of major simulated company resigns amidst massive accounting scandal.": -0.90,
#     "Routine Tuesday: No major economic data released today.": 0.0
# }

# def score_news_sentiment(headline):
#     prompt = f"""
#     Analyze the financial sentiment of this headline. 
#     Respond ONLY with a single float number between -1.0 (extreme bearish/panic) and 1.0 (extreme bullish/euphoria).
#     Do not include any other text, words, or formatting.
#     Headline: "{headline}"
#     """
#     try:
#         # Changed back to the highly stable 1.5-flash model
#         response = client.models.generate_content(
#             model='gemini-1.5-flash', 
#             contents=prompt,
#         )
#         score = float(response.text.strip())
#         return max(-1.0, min(1.0, score))
#     except Exception as e:
#         logging.warning(f"API Rate Limit/Error Hit. Triggering Local Fallback Matrix.")
#         return FALLBACK_SCORES.get(headline, 0.0)

# def run_oracle():
#     context = zmq.Context()
#     host = os.getenv("ZMQ_HOST", "127.0.0.1")
#     port = os.getenv("ZMQ_ORDER_PORT", "5555")

#     socket = context.socket(zmq.REQ)
#     socket.connect(f"tcp://{host}:{port}")
    
#     logging.info("Gemini Macro Oracle Online. Monitoring news feeds...")

#     try:
#         while True:
#             time.sleep(15) 
            
#             headline = random.choice(NEWS_FEED)
#             logging.info(f"BREAKING NEWS: {headline}")
            
#             sentiment = score_news_sentiment(headline)
#             logging.info(f"Sentiment Score: {sentiment}")

#             if abs(sentiment) >= 0.7:
#                 side = "BUY" if sentiment > 0 else "SELL"
#                 qty = 100000 
                
#                 logging.warning(f"HIGH IMPACT DETECTED! Injecting Massive {side} Order for {qty} shares!")
                
#                 socket.send_json({
#                     "agent_id": "GEMINI_ORACLE",
#                     "action": side,
#                     "qty": qty,
#                     "type": "MARKET"
#                 })
                
#                 reply = socket.recv_json()
#                 logging.info(f"Oracle Execution: {reply}")
#             else:
#                 logging.info("News impact minimal. No Oracle intervention required.")

#     except KeyboardInterrupt:
#         logging.info("Oracle shutting down.")
#         socket.close()
#         context.term()

# if __name__ == "__main__":
#     run_oracle()


# # import os
# # import zmq
# # import time
# # import random
# # import logging
# # from google import genai
# # from dotenv import load_dotenv

# # load_dotenv()

# # logging.basicConfig(
# #     level=logging.INFO,
# #     format='%(asctime)s - [ORACLE] - %(message)s'
# # )

# # client = genai.Client()

# # # =========================================================
# # # DEFAULT RANDOM NEWS FEED
# # # =========================================================

# # NEWS_FEED = [
# #     "Tech company reports record earnings.",
# #     "Central bank cuts interest rates aggressively.",
# #     "War escalates near strategic oil routes.",
# #     "Global recession fears increase.",
# #     "Major defense contract announced by government.",
# #     "AI sector receives massive investment boost."
# # ]

# # # =========================================================
# # # SECTOR MAPPING
# # # =========================================================

# # SECTOR_RULES = {
# #     "war": {
# #         "BUY": ["DEFENSE", "OIL"],
# #         "SELL": ["AIRLINE", "TOURISM"]
# #     },

# #     "oil": {
# #         "BUY": ["OIL", "ENERGY"],
# #         "SELL": ["AIRLINE"]
# #     },

# #     "recession": {
# #         "BUY": ["GOLD", "UTILITIES"],
# #         "SELL": ["BANKS", "TECH"]
# #     },

# #     "interest rate cut": {
# #         "BUY": ["TECH", "BANKS"],
# #         "SELL": []
# #     },

# #     "ai": {
# #         "BUY": ["AI", "TECH"],
# #         "SELL": []
# #     },

# #     "defense": {
# #         "BUY": ["DEFENSE"],
# #         "SELL": []
# #     }
# # }

# # # =========================================================
# # # STOCK SYMBOL MAP
# # # =========================================================

# # SECTOR_STOCKS = {
# #     "DEFENSE": ["LMT", "RTX", "NOC"],
# #     "OIL": ["XOM", "CVX"],
# #     "ENERGY": ["SLB"],
# #     "AIRLINE": ["DAL", "AAL"],
# #     "TOURISM": ["BKNG"],
# #     "TECH": ["NVDA", "AAPL", "MSFT"],
# #     "AI": ["NVDA", "AMD"],
# #     "BANKS": ["JPM", "GS"],
# #     "GOLD": ["GLD"],
# #     "UTILITIES": ["NEE"]
# # }

# # # =========================================================
# # # GEMINI SENTIMENT SCORING
# # # =========================================================

# # def score_news_sentiment(headline):

# #     prompt = f"""
# #     Analyze this financial news headline.

# #     Return ONLY one float between:
# #     -1.0 = extremely bearish
# #      1.0 = extremely bullish

# #     Headline: "{headline}"
# #     """

# #     try:
# #         response = client.models.generate_content(
# #             model='gemini-1.5-flash',
# #             contents=prompt
# #         )

# #         score = float(response.text.strip())
# #         return max(-1.0, min(1.0, score))

# #     except Exception as e:
# #         logging.warning(f"Gemini API Error: {e}")
# #         return 0.0

# # # =========================================================
# # # EVENT ANALYZER
# # # =========================================================

# # def detect_market_actions(news):

# #     news_lower = news.lower()

# #     buy_sectors = []
# #     sell_sectors = []

# #     for keyword, actions in SECTOR_RULES.items():

# #         if keyword in news_lower:
# #             buy_sectors.extend(actions["BUY"])
# #             sell_sectors.extend(actions["SELL"])

# #     return buy_sectors, sell_sectors

# # # =========================================================
# # # SEND ORDER
# # # =========================================================

# # def execute_trade(socket, action, stock, qty=1000):

# #     order = {
# #         "agent_id": "GEMINI_ORACLE",
# #         "symbol": stock,
# #         "action": action,
# #         "qty": qty,
# #         "type": "MARKET"
# #     }

# #     logging.warning(
# #         f"EXECUTING {action} ORDER | {stock} | Qty={qty}"
# #     )

# #     socket.send_json(order)

# #     reply = socket.recv_json()

# #     logging.info(f"Execution Reply: {reply}")

# # # =========================================================
# # # MAIN LOOP
# # # =========================================================

# # def run_oracle():

# #     context = zmq.Context()

# #     host = os.getenv("ZMQ_HOST", "127.0.0.1")
# #     port = os.getenv("ZMQ_ORDER_PORT", "5555")

# #     socket = context.socket(zmq.REQ)
# #     socket.connect(f"tcp://{host}:{port}")

# #     logging.info("AI Macro Oracle Online")

# #     try:

# #         while True:

# #             print("\n")
# #             print("=" * 60)
# #             print("1 -> Random News Simulation")
# #             print("2 -> Inject Manual News")
# #             print("3 -> Exit")
# #             print("=" * 60)

# #             choice = input("Select option: ")

# #             if choice == "1":

# #                 headline = random.choice(NEWS_FEED)

# #             elif choice == "2":

# #                 headline = input("\nEnter Breaking News: ")

# #             elif choice == "3":

# #                 break

# #             else:
# #                 continue

# #             logging.info(f"NEWS EVENT: {headline}")

# #             sentiment = score_news_sentiment(headline)

# #             logging.info(f"Sentiment Score: {sentiment}")

# #             buy_sectors, sell_sectors = detect_market_actions(headline)

# #             # =================================================
# #             # BUY SIDE
# #             # =================================================

# #             for sector in buy_sectors:

# #                 stocks = SECTOR_STOCKS.get(sector, [])

# #                 for stock in stocks:

# #                     execute_trade(
# #                         socket,
# #                         "BUY",
# #                         stock,
# #                         qty=5000
# #                     )

# #             # =================================================
# #             # SELL SIDE
# #             # =================================================

# #             for sector in sell_sectors:

# #                 stocks = SECTOR_STOCKS.get(sector, [])

# #                 for stock in stocks:

# #                     execute_trade(
# #                         socket,
# #                         "SELL",
# #                         stock,
# #                         qty=5000
# #                     )

# #             if not buy_sectors and not sell_sectors:

# #                 logging.info(
# #                     "No strong sector reaction detected."
# #                 )

# #     except KeyboardInterrupt:

# #         logging.info("Oracle shutting down.")

# #     finally:

# #         socket.close()
# #         context.term()

# # # =========================================================
# # # ENTRY POINT
# # # =========================================================

# # if __name__ == "__main__":
# #     run_oracle()






































# UPDATED `oracle.py`

import os
import zmq
import time
import random
import logging
import threading
from google import genai
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ORACLE] - %(message)s')

client = genai.Client()

NEWS_FEED = [
    "Tech Giant reports record-breaking Q3 earnings, shattering Wall Street estimates.",
    "Federal Reserve announces emergency rate cut of 100 bps.",
    "Major pipeline explodes, disrupting global oil supply significantly.",
    "Unemployment drops to historic lows, economy booming.",
    "CEO of major simulated company resigns amidst massive accounting scandal.",
    "Routine Tuesday: No major economic data released today."
]

FALLBACK_SCORES = {
    "Tech Giant reports record-breaking Q3 earnings, shattering Wall Street estimates.": 0.85,
    "Federal Reserve announces emergency rate cut of 100 bps.": 0.75,
    "Major pipeline explodes, disrupting global oil supply significantly.": -0.85,
    "Unemployment drops to historic lows, economy booming.": 0.70,
    "CEO of major simulated company resigns amidst massive accounting scandal.": -0.90,
    "Routine Tuesday: No major economic data released today.": 0.0
}


SECTOR_IMPACT = {
    "DEFENCE": ["war", "missile", "army", "border", "attack", "military"],
    "TECH": ["ai", "chip", "cloud", "software", "data", "robot"],
    "BANKING": ["interest", "rate", "inflation", "federal reserve", "loan"],
    "OIL": ["pipeline", "crude", "oil", "gas", "energy"],
    "PHARMA": ["drug", "medicine", "fda", "vaccine", "health"]
}


latest_state = {
    "sector": "TECH"
}


def score_news_sentiment(headline):

    prompt = f"""
    Analyze the financial sentiment of this headline.
    Respond ONLY with a single float number between -1.0 and 1.0.

    Headline: {headline}
    """

    try:

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        score = float(response.text.strip())

        return max(-1.0, min(1.0, score))

    except Exception:

        logging.warning("Gemini failed. Using fallback sentiment.")
        return FALLBACK_SCORES.get(headline, 0.0)



def detect_sector_boost(news, sector):

    news = news.lower()
    sector = sector.upper()

    keywords = SECTOR_IMPACT.get(sector, [])

    for keyword in keywords:
        if keyword in news:
            return True

    return False



def manual_news_input(socket):

    while True:

        user_news = input("\nENTER MANUAL NEWS (or press enter to skip): ")

        if not user_news.strip():
            continue

        process_news(socket, user_news, manual=True)



def process_news(socket, headline, manual=False):

    logging.info(f"NEWS => {headline}")

    sentiment = score_news_sentiment(headline)

    logging.info(f"Sentiment Score: {sentiment}")

    sector = latest_state.get("sector", "TECH")

    boosted = detect_sector_boost(headline, sector)

    if boosted:
        logging.warning(f"SECTOR BOOST DETECTED for {sector} sector!")
        sentiment += 0.35

    sentiment = max(-1.0, min(1.0, sentiment))

    if abs(sentiment) >= 0.5:

        side = "BUY" if sentiment > 0 else "SELL"

        qty = int(abs(sentiment) * 200000)

        logging.warning(
            f"ORACLE EXECUTING BULK {side} ORDER | Qty={qty}"
        )

        socket.send_json({
            "agent_id": "GEMINI_ORACLE",
            "action": side,
            "qty": qty,
            "type": "MARKET"
        })

        reply = socket.recv_json()

        logging.info(f"Execution Result => {reply}")

    else:

        logging.info("News impact too weak.")



def run_oracle():

    context = zmq.Context()

    host = os.getenv("ZMQ_HOST", "127.0.0.1")
    port = os.getenv("ZMQ_ORDER_PORT", "5555")

    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{host}:{port}")

    logging.info("Oracle Online...")

    threading.Thread(
        target=manual_news_input,
        args=(socket,),
        daemon=True
    ).start()

    try:

        while True:

            time.sleep(15)

            socket.send_json({
                "action": "FETCH_STATE"
            })

            state = socket.recv_json()

            latest_state["sector"] = state.get("sector", "TECH")

            headline = random.choice(NEWS_FEED)

            process_news(socket, headline)

    except KeyboardInterrupt:

        logging.info("Oracle shutting down.")
        socket.close()
        context.term()


if __name__ == "__main__":
    run_oracle()



