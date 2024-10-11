import os

async def download_tweets(user_id, client):
    return await client.get_user_tweets(user_id, 'Tweets')

async def login(client):
    await client.logout()

    await client.login(
        auth_info_1=os.getenv('TWITTER_USERNAME') ,
        auth_info_2=os.getenv('TWITTER_EMAIL'),
        password=os.getenv('TWITTER_PASSWORD')
    )
    client.save_cookies('cookies.json')