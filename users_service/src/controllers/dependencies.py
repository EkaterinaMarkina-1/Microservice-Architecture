from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

async def get_subscription_service(db: AsyncSession = Depends(get_async_session)):
    from src.utils.subscription_service import SubscriptionService
    return SubscriptionService(db=db)
