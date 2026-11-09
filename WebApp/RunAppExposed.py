import os
import threading
from pyngrok import ngrok
from app import app, load_models

def start_ngrok():
    # Set your ngrok auth token here
    # You can get one for free at https://dashboard.ngrok.com/login
    ngrok.set_auth_token("3FcjjIc4ed8M64XxgLxxO1B31IB_5p3jGrNJzFB1LvVzdoTJt")
    
    port = 5000
    public_url = ngrok.connect(port).public_url
    print("=" * 50)
    print(f"🌍 Your app is live at: {public_url}")
    print("=" * 50)

if __name__ == '__main__':
    # Initialize the models
    load_models()
    
    # Start ngrok in a separate thread
    threading.Thread(target=start_ngrok).start()
    
    # Start the Flask app
    app.run(port=5000, debug=False, use_reloader=False)
