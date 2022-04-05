from Controllers.main import app
import os
import json

if __name__ == '__main__':

    #Passing credentials as environment variables
    cred_path = os.path.join('config', 'credentials.json')
    if os.path.exists(cred_path):
        with open(cred_path) as f:
            creds = json.load(f)
        os.environ["CLIENT_ID"] = creds["CLIENT_ID"]
        os.environ["CLIENT_SECRET"] = creds["CLIENT_SECRET"]

        app.run(debug=True, host='127.0.0.1', port=5000)
