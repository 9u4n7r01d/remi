from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class StaffRole(Base):
    __tablename__ = "staff_role"

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    rank = Column(String)
    role_id = Column(Integer)

    def __repr__(self):
        return (
            f"StaffRole(id={self.id!r}, server_id={self.server_id!r}, role={self.rank!r}, "
            f"role_id={self.role_id!r}) "
        )
