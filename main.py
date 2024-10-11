import asyncio
import os
import time
from datetime import datetime, timezone

from dotenv import load_dotenv
from twikit import Client
import logging
from db import get_system_dates, get_user_id, insert_user, get_user_last_tweet_date, update_user, update_system
from nostr import upload_notes
from twitter import login, download_tweets
from util import minutes_passed, date_to_str, parse_twitter_date, str_to_date

logging.basicConfig(
    level=logging.INFO,  # Set the log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define the log format
)

# Initialize client
client = Client('en-US')

load_dotenv()

async def main():
    while True:
        logging.log(logging.INFO, 'Running twistr')
        (last_login_date, last_download_date) = get_system_dates()

        client.load_cookies('cookies.json')

        if minutes_passed(last_login_date) > int(os.getenv('LOGIN_DELAY_IN_MINUTES')):
            logging.log(logging.INFO, 'Refreshing login')
            await login(client)
            update_system(last_login_date=date_to_str(datetime.now(timezone.utc)))


        if minutes_passed(last_download_date) > int(os.getenv('DOWNLOAD_DELAY_IN_MINUTES')):
            for handle in os.getenv('TWITTER_HANDLES').split(','):
                logging.log(logging.INFO, f'Downloading new tweets for {handle}')
                user_id = await retrieve_user_id(handle)
                tweets = await download_tweets(user_id, client)
                previous_last_tweet_timestamp = str_to_date(get_user_last_tweet_date(user_id))
                new_tweets = [tweet for tweet in tweets
                              if parse_twitter_date(tweet.created_at) > previous_last_tweet_timestamp]
                if len(new_tweets) > 0:
                    logging.log(logging.INFO, f'{len(tweets)} New tweets found for {handle}, uploading to nostr')
                    last_tweet_timestamp = new_tweets[0].created_at
                    await upload_notes(new_tweets)
                    logging.log(logging.INFO, f'{len(tweets)} Uploaded')
                    update_user(user_id, date_to_str(parse_twitter_date(last_tweet_timestamp)), date_to_str(datetime.now(timezone.utc)))
                else:
                    logging.log(logging.INFO, f'No new tweets found for {handle}')
            update_system(last_download_date = date_to_str(datetime.now(timezone.utc)))
        time.sleep(120)


async def retrieve_user_id(handle):
    user_id = get_user_id(handle)
    if not user_id:
        user = await client.get_user_by_screen_name(handle)
        if user:
            insert_user(user.id, handle)
            user_id = user.id
        else:
            raise ValueError(f'User {handle} not found')
    return user_id


asyncio.run(main())