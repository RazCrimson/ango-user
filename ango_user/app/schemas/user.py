from uuid import uuid4

from sqlalchemy import TIMESTAMP, Column, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID

from ango_user.app.db.base_class import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String)
    pass_hash = Column(LargeBinary)
    init_vector = Column(LargeBinary)
    last_signed_in = Column(TIMESTAMP)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, init_vector={self.init_vector}, last_signed_in={self.last_signed_in}>"
