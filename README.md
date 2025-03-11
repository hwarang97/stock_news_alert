# Description
A program that sends alerts when a stock's closing price fluctuates beyond a predefined threshold. For example, if the closing price differs by more than 5% compared to the previous day's closing price, the program automatically sends an email notification. The email also includes three related news articles about the stock for additional context.

# How to Use

## Change stock
```
STOCK = "TSLA"  -> Chage stock that you want to see
```

## Set threshold
```python
THRESHOLD = 5
```

## Set your .env file
```
NEWS_API_KEY= 
POLYGON_API_KEY=
GOOGLE_SENDER=                     # Google send email
GOOGLE_SENDER_PASSWORD=            # This is google app secret 
GOOGLE_RECEIVER=                   # Where you want to receive email
```

# Tech (need to sign in, free)
- NewsAPI 
- Polygon.io 
- Google SMTP Server 

# How to Work
![image](https://github.com/user-attachments/assets/3e5473f3-011f-48d0-91df-420ab75e7020)
