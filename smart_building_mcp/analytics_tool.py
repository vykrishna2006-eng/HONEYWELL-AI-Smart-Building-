from backend.services.analytics_service import AnalyticsService
from database.database import SessionLocal

def get_dashboard():
    db = SessionLocal()
    try:
        service = AnalyticsService()
        return service.get_dashboard_summary(db)
    finally:
        db.close()