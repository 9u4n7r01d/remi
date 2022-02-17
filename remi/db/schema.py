from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ServerPrefix(Base):
    __tablename__ = "server_prefix"
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    prefix = Column(String)

    def __repr__(self):
        return f"StaffRole(id={self.id!r}, guild_id={self.guild_id!r}, prefix={self.prefix!r}"


class StaffRole(Base):
    __tablename__ = "staff_role"

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    rank = Column(String)
    role_id = Column(Integer)

    def __repr__(self):
        return f"StaffRole(id={self.id!r}, guild_id={self.guild_id!r}, role={self.rank!r}, role_id={self.role_id!r})"
