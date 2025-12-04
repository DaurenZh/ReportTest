from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Report, User, UserRole
from schemas import ReportCreate, ReportResponse
from auth import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create new report
    db_report = Report(
        category=report_data.category,
        message=report_data.message,
        user_id=current_user.id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report


@router.get("/", response_model=List[ReportResponse])
def get_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Admin sees all reports, staff sees only their own
    if current_user.role == UserRole.admin:
        reports = db.query(Report).all()
    else:
        reports = db.query(Report).filter(Report.user_id == current_user.id).all()
    
    return reports
