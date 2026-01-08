from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SubscriptionKeyUpdate(BaseModel):
    """Обновление ключа push-уведомлений пользователя"""
    subscription_key: Optional[str] = Field(
        None,
        description="Ключ для push-уведомлений (null — отключить уведомления)",
        example="bb779f9b-44b3-48e7-9576-bbdf7884cbb1"
    )

    model_config = ConfigDict(extra="forbid")


class SubscribeRequest(BaseModel):
    """Запрос на подписку на пользователя"""
    target_user_id: int = Field(
        ...,
        gt=0,
        description="ID пользователя, на которого оформляется подписка"
    )

    model_config = ConfigDict(extra="forbid")


class UnsubscribeRequest(BaseModel):
    """Запрос на отписку от пользователя"""
    target_user_id: int = Field(
        ...,
        gt=0,
        description="ID пользователя, от которого выполняется отписка"
    )

    model_config = ConfigDict(extra="forbid")
