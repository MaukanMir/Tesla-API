import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "Q8L7Y14ODS52JTKZ"
NEWS_API_KEY = "1433d0338dd544d0b548db61861e89ef"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "http://newsapi.org/v2/everything"

TWILIO_SID = "AC7515443715cc7846b93a397f634e9d90"
TWILIO_AUTH_TOKEN = "fbaf1dbcda8528d71882ca4a238c3797"



stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}


response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]

data_list = [value for (key,value)in stock_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
day_before_yesterday = data_list[1]
before_yesterdays_closing_price = float(day_before_yesterday["4. close"])

#If the stock change is greater than a certain amount, the program will send me the top three articles about tesla along with the rate of change in stock price to my phone number.

def stock_price(n1,n2):
    price_change = round(abs(((n2-n1)/n1) *100))
    required = {
        "qInTitle": COMPANY_NAME,
        "language": "en",
        "apiKey": NEWS_API_KEY
    }
    if price_change > 1:

        news_response = requests.get(NEWS_ENDPOINT, params=required)
        news_response.raise_for_status()
        news_data = news_response.json()['articles']

        three_articles = news_data[:3]

        headlines = [
            f"{STOCK}: Percentage Increase of: {price_change}%📈  Headlines: {article['title']}.\nBrief:{article['description']}" for article in three_articles]

        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        for article in headlines:
            message = client.messages \
                .create(
                    body=article,
                    from_='+14807446411',
                    to='+16106759632'
                )
    else:
        return False


print(stock_price(before_yesterdays_closing_price, yesterday_closing_price))

    

