from flask import Flask, request,jsonify,render_template
import requests
import threading
import streamlit as st

#Flask app
app = Flask(__name__)


@app.route('/', methods=['POST'])  # Create Route
def index():  # create function
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
 #   print(source_currency)
  #  print(amount)
   ####### print(target_currency)
    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount= amount * cf
    final_amount=round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }

  #  print(final_amount)
    return jsonify(response)


def fetch_conversion_factor(source, target):
    url = "https://free.currconv.com/api/v8/convert?q={}_{}&compact=ultra&apiKey=8ee7ada6101c53ce7eca".format(source,target)


    response = requests.get(url)
    response = response.json()
    print(response)
    return response['{}_{}'.format(source,target)]

# Route to serve chatbot HTML
@app.route('/chatbot', methods=['GET'])
def chatbot():
    return render_template('chatbotkaka.html')

# Streamlit app
def run_streamlit():
    st.title("Currency Converter Telegram Bot")
    st.write("This app runs a Flask-based Telegram bot in the background.")
    st.success("Flask app is running in the background.")
    st.write("Open the chatbot interface by visiting: [Chatbot Interface](http://localhost:5000/chatbot)")

# Start Flask in a thread
def run_flask():
    app.run(debug=False, use_reloader=False, port=5000)



if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_streamlit()

