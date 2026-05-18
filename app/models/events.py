import logging
from app.db.postgres import Base, SessionLocal
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, JSON
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

_logger = logging.getLogger(__name__)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    aggregate_id = Column(String, nullable=False)
    aggregate_type = Column(String, nullable=False)

    event_type = Column(String, nullable=False)

    # When a new operation on same aggregation_id happens, it will update sequence count to 1
    # This way we will get all operations on specific aggregation_id in order
    event_sequence = Column(Integer, nullable=False)

    event_data = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "aggregate_id",
            "event_sequence",
            name="unique_aggregate_event_sequence"
        ), 
    )

def create_event(data):
    db = SessionLocal()
    try:
        event = Event(
            aggregate_id=data["event_id"],  # product_101
            aggregate_type=data["event_name"],  # product
            event_type=data["event_type"],  # PRODUCT_CREATED
            event_sequence=data["event_sequence"],
            event_data=data["event_data"]
        )

        db.add(event)
        db.commit()
    
    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

def fetch_latest_event_sequence(aggregate_id):
    db = SessionLocal()

    try:
        latest_event_sequence = (
            db.query(func.max(Event.event_sequence))
            .filter(Event.aggregate_id == aggregate_id)
            .scalar()
        )
        return latest_event_sequence or 0
    except Exception as e:
        raise e
    finally:
        db.close()

def fetch_event_by_id(aggregate_id):
    db = SessionLocal()

    try:
        event = (
            db.query(Event)
            .filter(Event.aggregate_id == aggregate_id)
            .first()
        )
        if event:
            return event
        else:
            raise Exception(f"No event available with given id")
    except Exception as e:
        raise e
    finally:
        db.close()

def fetch_all_events(aggregate_id):
    db = SessionLocal()

    try:
        events = (
            db.query(Event)
            .filter(Event.aggregate_id == aggregate_id)
            .order_by(Event.event_sequence.asc())
            .all()
        )
        if events:
            return events
        else:
            raise Exception(f"No event available with given id")
    except Exception as e:
        raise e
    finally:
        db.close()