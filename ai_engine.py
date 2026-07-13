import os
import time
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine, text
import google.generativeai as genai

def get_rsi(ticker_symbol):
  """Calculates 14-DAY RSI using pure pandas"""
  try:
    data: = yf.download(ticker_symbol, period="1mo", progress = False)
    if len(data) < 15:
      return "N/A"
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain/loss
    rsi = 100 - (100/(1+ rs))
    return round(rsi.iloc[-1].item(),2)
  except Exception:
    return "N/A"

def run_ai_analysis():
  print("Waking up Gemini AI engine....")
  db_url = os.environ.get("DATABASE_URL")
  if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://",1)
  engine = create_engine(db_url)

  genai.configure(api_key = os.environ.get("GEMINI_API_KEY"))
  model = genai.GenerativeModel('gemini-1.5-flash')

  query = """
    SELECT id, ticker, company_name
    FROM assets
    WHERE ticker is NOT NULL
    AND (ai_verdict is NULL OR confidence_score IS NULL)
  """

  df = pd.read_sql_query(query, engine)

  if df.empty:
    print("All assets have been analyzed, AI returning to sleep.")
    return

  with engine.begin() as conn:
    for index, row in df.iterrows():
      ticker_sym = row['ticker']
      company = row['company_name']
      print(f"Analyzing {ticker_sym}...")

      try:
        # fetching live data for the prompt
        ticker = yf.Ticker(ticker_sym)
        info = ticker.info
        fast_info = ticker.fast_info

        pe_ratio = info.get('trailingPE', info.get('forwardPE', 'N/A'))
        market_cap = fast_info.get('market_cap', 'N/A')
        high_52 = fast_info.get('year_high','N/A')
        low_52 = fast_info.get(year_low','N/A')
        ma_50 = fast_info.get('fifty_day_average','N/A')
        ma_200 = fast_info.get('two_hundred_day_average','N/A')
        rsi = get_rsi(ticker_sym)

        #pull top3 news on ticker
        news_list = ticker.news
        news_headlines = "\n".join([n['title'] for n in news_list[:3]]) if news_list else "No recent news available."

        if pe_ratio != 'N\A': pe_ratio = round(pe_ratio, 2)

        # Master Prompt
        prompt = f"""
        Act as a Professional quantitative financial analyst focusing on the Indian Stock Market, specializing in equities, REITs and INVITs.
        Company Name: {company}
        Ticker Symbol: {ticker_sym}
        Valuation (P/E): {pe_ratio}
        Market Cap: {market_cap}
        52 Week High: {high_52}
        52 Week Low: {low_52}
        50-Day Moving Average: {ma_50}
        200-Day Moving Average: {ma_200}
        14-Day RSI: {rsi}
        Recent News Headlines: {news_headlines}
        Analyze this stock using the provided real-time fundamental metrics and technical moving averages. Assess its valuation (using the P/ E ratio) and its current price momentum relative to its 52-week highs and lows and its technical trend(is the current price above or below its 50-day moving average and 200 day moving averages?). Write a punchy, 3- sentence summary of its current financial health and technical momentum, declaring if it is a buy, hold or overvalued.
        Factor in the recent news headlines: is the sentiment bullish, bearish or neutral? Does it justify the current technical momentum?
        Crucially factor in the 14-day RSI: if it is above 70, flag it as technically overbought and if it below 30, flag it as technically oversold and a potential entry point.
        Custom Thesis Guardrails:
        Rule 1: If the P/E ratio is greater than 35, the maximum score you can assign is 4, regardless of technical momentum.
        Rule 2: An RSI below 30 combined with bullish news sentiment is a "High Conviction Setup". Immediately flag this in your verdict. 
        Return the response exactly in this format:
        Verdict:[your 3 sentence Summary analysis here]
        Score:[Insert a number here from 1 to 10]
        Yield:[Insert current dividend/distribution yield percentage, e.g,. 7.5%]
        Frequency:[Insert how often they pay out, e.g., Quarterly or Bi-Annually]
        Consistency:[State whether payouts are stable, growing or fluctuating]
        """
        response = model.generate_content(prompt)

        output_lines = response.text.strip().split('\n')
        output_lines = [line for line in output_lines if line.strip()]  # remove empty lines

        verdict = output_lines[0].replace('[','').replace(']','').strip()
        score_str = output_lines[1].replace('[','').replace(']','').strip()

        try:
          score = int(''.join(filter(str.isdigit, score_str)))
        except ValueError:
          score = 5 #default safety score

        # save to database
        update_query = text('''
                                  UPDATE assets
                                  SET ai_verdict = :verdict,
                                      confidence_score = :score
                                  Where ticker = :ticker
        ''')

        conn.execute(update_query, {"verdict", verdict, "score", score, "ticker", ticker_sym})

        print(f"Successfully generated analysis for {ticker_sym}. Score: {score}")
        time.sleep(3)  #brief pause for gemini

      except Exception as e:
        print(f"Failed to analyze {ticker_sym}. Error : {e}")
                
If __name__ = "__main__":
  run_ai_analysis()
