from fastapi import APIRouter, Depends, status

from src.controllers.subscription import (
    update_subscription_key,
    subscribe_to_author,
    unsubscribe_from_author,
)
from src.schemas.subscription import (
    SubscriptionKeyUpdate,
    SubscribeRequest,
    UnsubscribeRequest,
)
from src.schemas.user_schemas import UserOut

router = APIRouter(prefix="/api/users", tags=["subscriptions"])


@router.put(
    "/me/subscription-key",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Установить ключ для push-уведомлений",
    description="Сохраняет или очищает subscription_key текущего пользователя",
)
async def set_subscription_key(
    payload: SubscriptionKeyUpdate,
    result: UserOut = Depends(update_subscription_key),
):
    return result


@router.post(
    "/subscribe",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Подписаться на автора",
    description="Текущий пользователь подписывается на получение уведомлений о новых постах автора",
)
async def subscribe(
    payload: SubscribeRequest,
    _: None = Depends(subscribe_to_author),
):
    return None


@router.post(
    "/unsubscribe",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Отписаться от автора",
    description="Удаляет подписку на уведомления от указанного автора",
)
async def unsubscribe(
    payload: UnsubscribeRequest,
    _: None = Depends(unsubscribe_from_author),
):
    return None
