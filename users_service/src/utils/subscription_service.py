from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.models.user import User
from src.models.subscriber import Subscriber

class SubscriptionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # --- Подписка на автора ---
    async def subscribe_to_author(self, subscriber_id: int, target_user_id: int):
        if subscriber_id == target_user_id:
            raise ValueError("Нельзя подписаться на самого себя")

        # Проверяем, существует ли автор
        author = await self.db.execute(
            select(User).where(User.id == target_user_id)
        )
        author_obj = author.scalar_one_or_none()
        if not author_obj:
            raise KeyError("Пользователь-автор не найден")

        # Пробуем вставить подписку
        try:
            stmt = insert(Subscriber).values(
                subscriber_id=subscriber_id,
                author_id=target_user_id
            )
            await self.db.execute(stmt)
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise RuntimeError("Вы уже подписаны на этого пользователя")

    # --- Отписка от автора ---
    async def unsubscribe_from_author(self, subscriber_id: int, target_user_id: int) -> None:
        stmt = delete(Subscriber).where(
            Subscriber.subscriber_id == subscriber_id,
            Subscriber.author_id == target_user_id
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        if result.rowcount == 0:
            raise KeyError("Подписка не найдена")

    async def update_subscription_key(self, user_id: int, subscription_key: str):
        """
        Обновляет subscription_key у пользователя и возвращает объект User
        """
        try:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(subscription_key=subscription_key)
                .returning(User)  # важно!
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            user = result.scalar_one_or_none()

            if not user:
                raise KeyError(f"Пользователь с id={user_id} не найден")

            return user  # ORM объект User

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Ошибка при обновлении ключа подписки: {e}")