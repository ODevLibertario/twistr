# Twistr

Script to run periodically and import tweets from Twitter and upload them to Nostr as notes, no Twitter API key required.

### Installation

Requires Python 3.10 or greater.

    pip install python-dotenv
    pip install nostr-sdk   
    pip install twikit 

Rename .env.example to .env and fill up your desired configuration.

Run main.py

## Warnings IMPORTANT!!!

ALWAYS use a throw away Twitter account, this process is not allowed but the TOS and can get you banned.

Be careful with how often you pool Tweets or Login to Twitter it detects abuses and might lock or suspend the account, 50 requests to download tweets every 15 minutes is the maximum so be careful to not try to extract from too many handles.

Your IP could be blacklisted by Twitter so avoid using your home IP with this application. Use a VPN or a VPS.

