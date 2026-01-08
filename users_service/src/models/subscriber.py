from sqlalchemy import ForeignKey, UniqueConstraint, Integer
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("subscriber_id", "author_id", name="ux_sub"),
    )
