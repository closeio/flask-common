import uuid
import sqlalchemy as db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

# From https://code.launchpad.net/~stefanor/ibid/sqlalchemy-0.6-trunk/+merge/66033
class PGSQLModeListener(object):
    def connect(self, dbapi_con, con_record):
        c = dbapi_con.cursor()
        c.execute("SET TIME ZONE UTC")
        c.close()

class Base(object):
    id = db.Column(UUID, default=lambda: str(uuid.uuid4()), primary_key=True)
    created_at = db.Column(db.DateTime(), default=db.func.now())
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())

    __mapper_args__ = {
        'order_by': db.desc('updated_at')
    }

class UserBase(Base):
    created_by_id = declared_attr(lambda cls: db.Column(UUID, db.ForeignKey('user.id'), default=cls._get_current_user))
    created_by = declared_attr(lambda cls: relationship('User', primaryjoin='%s.created_by_id == User.id' % cls.__name__))
    updated_by_id = declared_attr(lambda cls: db.Column(UUID, db.ForeignKey('user.id'), default=cls._get_current_user, onupdate=cls._get_current_user))
    updated_by = declared_attr(lambda cls: relationship('User', primaryjoin='%s.updated_by_id == User.id' % cls.__name__))

    @classmethod
    def _get_current_user(cls):
        return None
