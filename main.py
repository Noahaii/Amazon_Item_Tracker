from bs4 import BeautifulSoup
import lxml
import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

#  globals
SID = os.environ.get('TWILIO_SID')
TOKEN = os.environ.get('TWILIO_TOKEN')

#  returns a tuple of (price, product)
def amazonPrice():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url="https://www.amazon.com/Raspberry-Pi-Computer-Suitable-Workstation/dp/B0899VXM8F/ref=sr_1_3?crid=1WDBPJ4EL41KQ&keywords=raspberry+pi+4+8gb&qid=1659980645&sprefix=rasp%2Caps%2C825&sr=8-3",
                             headers=headers)
    web_html = response.content
    soup = BeautifulSoup(web_html, "lxml")

    pricetag = soup.find(name='span', class_="a-offscreen")
    price = float(pricetag.getText().split('$')[1])

    product = soup.find(name='span', class_="a-size-large product-title-word-break")
    productName = product.getText()
    print(productName)
    return (price, productName)

def sendMessage(amazonDetails):
    client = Client(SID, TOKEN)
    textMessage = f"this is the price of the \"{amazonDetails[1]}\", Price: {amazonDetails[0]}"

    message = client.messages.create(
        to= "+18183193600",
        from_= "+15737664742",
        body= textMessage)


def main():
    amazonDetails = amazonPrice()
    sendMessage(amazonDetails)


if __name__ == "__main__":
    main()