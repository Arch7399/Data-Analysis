import pandas as pd

# Display options for jupyter dataframe visualization
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# coinmarketbase imports for api
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


# data fetch function
def api_runner():
    global df

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {"start": "1", "limit": "1000", "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "your API key",
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    df = pd.json_normalize(data["data"])
    df["timestamp"] = pd.to_datetime("now")
    df

    # save data locally or append if already exists
    if not os.path.isfile(r"C:\Users\Arch\Desktop\CryptoAPI.csv"):
        df.to_csv(r"path to file\File.csv", header="column_names")
    else:
        df.to_csv(r"path to file\File.csv", mode="a", header=False)


import os
from time import time
from time import sleep

# loop according to your needs and frequency
for i in range(1):
    api_runner()
    sleep(10)
    print("API fetch ran successfully")

# read the data from the local csv and store it as a dataframe
df3 = pd.read_csv(r"path to file\File.csv")

# formats all numeric values in scientific notation to 5 decimals
pd.set_option("display.float_format", lambda x: "%.5f" % x)

# calculates the mean of all fetches for the specified columns and groups them by the name field as index
df4 = df3.groupby("name")[
    [
        "quote.USD.percent_change_1h",
        "quote.USD.percent_change_24h",
        "quote.USD.percent_change_7d",
        "quote.USD.price",
        "quote.USD.volume_24h",
    ]
].mean()

# Sort by '24h trade volume'
df3 = df4.sort_values(by=["quote.USD.volume_24h"], ascending=False)

# filter price between 1 and 5
df3 = df3[
    (df3["quote.USD.price"] <= 5)
    & (df3["quote.USD.price"] > 1)
    & (df3["quote.USD.percent_change_24h"] > 5)
]

# select specific columns
df3 = df3[
    [
        "quote.USD.percent_change_1h",
        "quote.USD.percent_change_24h",
        "quote.USD.percent_change_7d",
    ]
]
print(df3)

df5 = df3.stack()
df6 = df5.to_frame(name="values")

index = pd.Index(range(90))
df7 = df6.reset_index()
df7 = df7.rename(columns={"level_1": "percentage_change"})

df7["percentage_change"] = df7["percentage_change"].replace(
    [
        "quote.USD.percent_change_1h",
        "quote.USD.percent_change_24h",
        "quote.USD.percent_change_7d",
    ],
    ["1h", "24h", "7d"],
)

# using seaborn module for visualization
import seaborn as sns
import matplotlib.pyplot as plt

sns.catplot(x="percentage_change", y="values", hue="name", data=df7, kind="point")
plt.show()

# Calculate the correlation matrix of the top currency with others
filtered_df4 = df4.loc[df3.index]
# transpose the data frame to apply dataframe correlation method
df8 = filtered_df4.T
correlation_matrix = df8.corr()
first_currency = df3.index[0]
correlation = correlation_matrix.loc[:, first_currency]

correlation_df = correlation.reset_index()
correlation_df.columns = ["Currency", "Correlation"]
# prevents showing correlation of currency with itself
correlation_df = correlation_df[correlation_df["Currency"] != first_currency]
correlation_df = correlation_df.sort_values(by="Correlation", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x="Correlation", y="Currency", data=correlation_df, palette="coolwarm")

plt.title(f"Correlation of {first_currency} with Other Currencies")
plt.xlabel("Correlation")
plt.ylabel("Currency")

# plt.show()

# SNS using smtplib module
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function to send email alert
def send_email_alert(currencies, recipient_emails):
    # Email configurations
    sender_email = "senderemail@mail.com"
    password = ""

    # Email content
    subject = "Cryptocurrency Alert"
    body = f"{', '.join(currencies)} are performing well."

    html_content = """
        <html>
        <head>
        <title>Cryptocurrency Alert</title>
        <style>
        /* Responsive styles */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f8ff;  /* Light blue background */
        }

        .container {
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
        }

        h1 {
            color: #333;
            font-size: 1.5rem;
            text-align: center;
        }

        p {
            margin: 0;
            padding: 5px;
            color: #666;  /* Slightly darker text for better contrast */
        }

        ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        li {
            display: inline-block;
            margin: 0 10px 10px 0;
            padding: 5px 10px;
            background-color: #e0ebef;  /* Lighter blue for list items */
            border-radius: 5px;
        }

        /* Additional styling */
        h1 {
            margin-bottom: 15px;
        }

        p {
            font-size: 0.9rem;
        }
        </style>
        </head>
        <body>
        <div class="container">
        <h1>Cryptocurrency Alert</h1>
        <p>The following currencies are performing well:</p>
        <ul>
         """
    for currency in currencies:
        url = f"https://coinmarketcap.com/currencies/{currency}/"
        html_content += f'<li><a href="{url}">{currency}</a></li>\n'

    html_content += """   
        </ul>
        </div>
        </body>
        </html>
        """

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipient_emails)
    message["Subject"] = subject

    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    # Connect to SMTP server and send email
    with smtplib.SMTP("smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_emails, message.as_string())


# Performance evaluation analysis
df9 = df3.reset_index()
df9 = df9.rename(
    columns={
        "quote.USD.percent_change_1h": "1h",
        "quote.USD.percent_change_24h": "24h",
        "quote.USD.percent_change_7d": "7d",
    }
)


def evaluate_performance(row):
    performance = {"1h": "Poor", "24h": "Poor", "7d": "Poor"}

    if row["1h"] > 1:
        performance["1h"] = "Good"
    if row["24h"] > 5:
        performance["24h"] = "Good"
    if row["7d"] > 10:
        performance["7d"] = "Good"

    return performance


# calculate performance for all currencies
df9["Performance"] = df9.apply(evaluate_performance, axis=1)


def is_performing_well(performance):
    return all(value == "Good" for value in performance.values())


df9["IsPerformingWell"] = df9["Performance"].apply(is_performing_well)

performing_currencies = []
for index, row in df9.iterrows():
    if row["IsPerformingWell"]:
        print(f"Alert: {row['name']} is performing well")
        performing_currencies.append(row["name"])

# List of Recipient emails
recipient_emails = ["youremail@mail.com"]

# send email alert if and only if currencies are performing well
if performing_currencies:
    send_email_alert(performing_currencies, recipient_emails)
    print(f"{performing_currencies} are performing well.!")
