import logging
import os
import requests

from celery_app import celery_app
from db.base import create_session
from repositories.users_rep import UsersRepository

USERS_DATABASE_URL = os.getenv("USERS_DATABASE_URL")
PUSH_URL = os.getenv("PUSH_URL")

if not USERS_DATABASE_URL:
    raise RuntimeError("USERS_DATABASE_URL is not set")

UsersSessionFactory = create_session(USERS_DATABASE_URL)


@celery_app.task(
    name="notify_followers",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def notify_followers(self, author_id: int, post_id: int,post_title:str):
    users_db = UsersSessionFactory()

    try:
        users_rep = UsersRepository(users_db)

        title = post_title[:10]

        subs = users_rep.get_subscribers_with_keys(author_id)

        for sub in subs:
            if not sub.subscription_key:
                logging.warning(
                    "No subscription_key for subscriber %s",
                    sub.subscriber_id,
                )
                continue

            response = requests.post(
                PUSH_URL,
                headers={
                    "Authorization": f"Bearer {sub.subscription_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "message": f"Пользователь {author_id} выпустил новый пост: {title}..."
                },
                timeout=5,
            )
            response.raise_for_status()

    finally:
        users_db.close()