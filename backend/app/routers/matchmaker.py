from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models, schemas
from app.security import get_current_matchmaker

router = APIRouter(prefix="/matchmaker", tags=["红娘工作台"])


@router.get("/statistics", response_model=schemas.StatisticsResponse)
def get_statistics(
    current_matchmaker: models.User = Depends(get_current_matchmaker),
    db: Session = Depends(get_db)
):
    total_members = db.query(models.User).filter(
        models.User.role == models.UserRole.MEMBER
    ).count()
    
    male_count = db.query(models.User).join(models.Profile).filter(
        models.User.role == models.UserRole.MEMBER,
        models.Profile.gender == models.Gender.MALE
    ).count()
    
    female_count = db.query(models.User).join(models.Profile).filter(
        models.User.role == models.UserRole.MEMBER,
        models.Profile.gender == models.Gender.FEMALE
    ).count()
    
    male_ratio = male_count / total_members if total_members > 0 else 0
    
    total_matches = db.query(models.Match).count()
    
    total_activities = db.query(models.Activity).count()
    
    total_registrations = db.query(models.ActivityRegistration).count()
    
    activity_participation_rate = 0
    if total_members > 0 and total_activities > 0:
        unique_participants = db.query(
            func.count(func.distinct(models.ActivityRegistration.user_id))
        ).scalar()
        activity_participation_rate = unique_participants / total_members
    
    pending_profiles = db.query(models.Profile).filter(
        models.Profile.status == models.ProfileStatus.PENDING
    ).count()
    
    return schemas.StatisticsResponse(
        total_members=total_members,
        male_count=male_count,
        female_count=female_count,
        male_ratio=male_ratio,
        total_matches=total_matches,
        total_activities=total_activities,
        total_registrations=total_registrations,
        activity_participation_rate=activity_participation_rate,
        pending_profiles=pending_profiles
    )
