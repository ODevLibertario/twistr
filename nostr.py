import os

from nostr_sdk import Keys, Client, NostrSigner, EventBuilder, init_logger, LogLevel

from util import format_date

async def upload_notes(tweets):
    init_logger(LogLevel.INFO)

    keys = Keys.parse(os.getenv('NOSTR_NSEC'))
    signer = NostrSigner.keys(keys)

    client = Client(signer)

    # Add relays and connect
    for relay in os.getenv('NOSTR_RELAYS').split(','):
        await client.add_relay(relay)

    await client.connect()

    # Send an event using the Nostr Signer
    for tweet in tweets:
        note_text = f"""From: {tweet.user.name}\nAt: {format_date(tweet.created_at)}\n\n{tweet.full_text}""".strip()

        builder = EventBuilder.text_note(note_text, [])
        await client.send_event_builder(builder)

