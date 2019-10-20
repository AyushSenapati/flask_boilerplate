from app import db


class BaseModel(db.Model):
    '''
    This is an abstrct model. Upon inheriting this model
    few common fields and functionalities will be added to the child model.
    '''
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(),
        nullable=False
    )
    # Uncomment if updated_at field is needed
    updated_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
