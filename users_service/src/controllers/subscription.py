from fastapi import HTTPException, Depends
from src.schemas.subscription import SubscriptionKeyUpdate, SubscribeRequest, UnsubscribeRequest
from src.utils.auth import get_current_user_id
from src.utils.subscription_service import SubscriptionService
from src.database import get_async_session 
from sqlalchemy.ext.asyncio import AsyncSession


async def get_subscription_service(db: AsyncSession = Depends(get_async_session)):
    return SubscriptionService(db=db)


async def update_subscription_key(
    payload: SubscriptionKeyUpdate,
    current_user_id: int = Depends(get_current_user_id),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    """
    Обновление ключа подписки текущего пользователя
    """
    try:
        result = await subscription_service.update_subscription_key(
            user_id=current_user_id,
            subscription_key=payload.subscription_key,
        )
        return result
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def subscribe_to_author(
    payload: SubscribeRequest,
    current_user_id: int = Depends(get_current_user_id),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    """
    Подписка текущего пользователя на автора
    """
    try:
        await subscription_service.subscribe_to_author(
            subscriber_id=current_user_id,
            target_user_id=payload.target_user_id,
        )
        return {"status": "subscribed", "author_id": payload.target_user_id}
    except (KeyError, ValueError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


async def unsubscribe_from_author(
    payload: UnsubscribeRequest,
    current_user_id: int = Depends(get_current_user_id),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    """
    Отписка текущего пользователя от автора
    """
    try:
        await subscription_service.unsubscribe_from_author(
            subscriber_id=current_user_id,
            target_user_id=payload.target_user_id,
        )
        return {"status": "unsubscribed", "author_id": payload.target_user_id}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
