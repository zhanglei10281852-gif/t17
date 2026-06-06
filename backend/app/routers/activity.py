import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.security import get_current_user, get_current_matchmaker

router = APIRouter(prefix="/activities", tags=["相亲活动"])


def profile_to_response(profile: models.Profile) -> schemas.ProfileResponse:
    hobbies_list = json.loads(profile.hobbies) if profile.hobbies else []
    return schemas.ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        nickname=profile.nickname,
        gender=profile.gender,
        birth_date=profile.birth_date,
        age=profile.age,
        height=profile.height,
        weight=profile.weight,
        education=profile.education,
        occupation=profile.occupation,
        income=profile.income,
        city=profile.city,
        hometown=profile.hometown,
        marital_status=profile.marital_status,
        has_children=profile.has_children,
        smoking=profile.smoking,
        drinking=profile.drinking,
        hobbies=hobbies_list,
        introduction=profile.introduction,
        status=profile.status,
        reject_reason=profile.reject_reason,
        updated_at=profile.updated_at
    )


def activity_to_response(activity: models.Activity, db: Session) -> schemas.ActivityResponse:
    male_reg = db.query(models.ActivityRegistration).join(
        models.Profile,
        models.ActivityRegistration.user_id == models.Profile.user_id
    ).filter(
        models.ActivityRegistration.activity_id == activity.id,
        models.Profile.gender == models.Gender.MALE
    ).count()
    female_reg = db.query(models.ActivityRegistration).join(
        models.Profile,
        models.ActivityRegistration.user_id == models.Profile.user_id
    ).filter(
        models.ActivityRegistration.activity_id == activity.id,
        models.Profile.gender == models.Gender.FEMALE
    ).count()
    
    return schemas.ActivityResponse(
        id=activity.id,
        name=activity.name,
        activity_time=activity.activity_time,
        location=activity.location,
        activity_type=activity.activity_type,
        male_limit=activity.male_limit,
        female_limit=activity.female_limit,
        min_age=activity.min_age,
        max_age=activity.max_age,
        fee=activity.fee,
        description=activity.description,
        status=activity.status,
        created_by=activity.created_by,
        created_at=activity.created_at,
        male_registered=male_reg,
        female_registered=female_reg
    )


@router.get("", response_model=list[schemas.ActivityResponse])
def list_activities(
    status: models.ActivityStatus = None,
    skip: int = 0,
    limit: int = 20,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Activity)
    if status:
        query = query.filter(models.Activity.status == status)
    
    activities = query.order_by(models.Activity.activity_time.desc()).offset(skip).limit(limit).all()
    return [activity_to_response(a, db) for a in activities]


@router.get("/{activity_id}", response_model=schemas.ActivityResponse)
def get_activity(
    activity_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    return activity_to_response(activity, db)


@router.post("", response_model=schemas.ActivityResponse)
def create_activity(
    activity_in: schemas.ActivityCreate,
    current_matchmaker: models.User = Depends(get_current_matchmaker),
    db: Session = Depends(get_db)
):
    activity = models.Activity(
        **activity_in.model_dump(),
        created_by=current_matchmaker.id
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity_to_response(activity, db)


@router.put("/{activity_id}", response_model=schemas.ActivityResponse)
def update_activity(
    activity_id: int,
    activity_in: schemas.ActivityUpdate,
    current_matchmaker: models.User = Depends(get_current_matchmaker),
    db: Session = Depends(get_db)
):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    
    update_data = activity_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(activity, key, value)
    
    db.commit()
    db.refresh(activity)
    return activity_to_response(activity, db)


@router.post("/{activity_id}/register")
def register_activity(
    activity_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    
    if activity.status != models.ActivityStatus.REGISTERING:
        raise HTTPException(status_code=400, detail="活动不在报名阶段")
    
    existing_reg = db.query(models.ActivityRegistration).filter(
        models.ActivityRegistration.activity_id == activity_id,
        models.ActivityRegistration.user_id == current_user.id
    ).first()
    if existing_reg:
        raise HTTPException(status_code=400, detail="您已报名该活动")
    
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile or not profile.gender or not profile.age:
        raise HTTPException(status_code=400, detail="请先完善个人资料")
    
    if profile.age < activity.min_age or profile.age > activity.max_age:
        raise HTTPException(status_code=400, detail=f"年龄不符合要求，要求{activity.min_age}-{activity.max_age}岁")
    
    male_reg = db.query(models.ActivityRegistration).join(
        models.Profile,
        models.ActivityRegistration.user_id == models.Profile.user_id
    ).filter(
        models.ActivityRegistration.activity_id == activity_id,
        models.Profile.gender == models.Gender.MALE
    ).count()
    female_reg = db.query(models.ActivityRegistration).join(
        models.Profile,
        models.ActivityRegistration.user_id == models.Profile.user_id
    ).filter(
        models.ActivityRegistration.activity_id == activity_id,
        models.Profile.gender == models.Gender.FEMALE
    ).count()
    
    if profile.gender == models.Gender.MALE and male_reg >= activity.male_limit:
        raise HTTPException(status_code=400, detail="男性名额已满")
    if profile.gender == models.Gender.FEMALE and female_reg >= activity.female_limit:
        raise HTTPException(status_code=400, detail="女性名额已满")
    
    registration = models.ActivityRegistration(
        activity_id=activity_id,
        user_id=current_user.id
    )
    db.add(registration)
    
    new_male = male_reg + (1 if profile.gender == models.Gender.MALE else 0)
    new_female = female_reg + (1 if profile.gender == models.Gender.FEMALE else 0)
    if new_male >= activity.male_limit and new_female >= activity.female_limit:
        activity.status = models.ActivityStatus.FULL
    
    db.commit()
    
    return {"message": "报名成功"}


@router.get("/{activity_id}/participants", response_model=list[schemas.ActivityRegistrationResponse])
def get_activity_participants(
    activity_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    
    is_registered = db.query(models.ActivityRegistration).filter(
        models.ActivityRegistration.activity_id == activity_id,
        models.ActivityRegistration.user_id == current_user.id
    ).first()
    
    if not is_registered and current_user.role != models.UserRole.MATCHMAKER:
        raise HTTPException(status_code=403, detail="只有报名者和红娘可以查看参与者")
    
    registrations = db.query(models.ActivityRegistration).filter(
        models.ActivityRegistration.activity_id == activity_id
    ).all()
    
    result = []
    for reg in registrations:
        user_profile = db.query(models.Profile).filter(
            models.Profile.user_id == reg.user_id
        ).first()
        reg_data = schemas.ActivityRegistrationResponse(
            id=reg.id,
            activity_id=reg.activity_id,
            user_id=reg.user_id,
            registered_at=reg.registered_at,
            user_profile=profile_to_response(user_profile) if user_profile else None
        )
        result.append(reg_data)
    
    return result


@router.post("/{activity_id}/review", response_model=schemas.ActivityReviewResponse)
def create_review(
    activity_id: int,
    review_in: schemas.ActivityReviewCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    
    if activity.status != models.ActivityStatus.ENDED:
        raise HTTPException(status_code=400, detail="活动未结束，不能评价")
    
    is_registered = db.query(models.ActivityRegistration).filter(
        models.ActivityRegistration.activity_id == activity_id,
        models.ActivityRegistration.user_id == current_user.id
    ).first()
    if not is_registered:
        raise HTTPException(status_code=400, detail="您未参加此活动")
    
    target_registered = db.query(models.ActivityRegistration).filter(
        models.ActivityRegistration.activity_id == activity_id,
        models.ActivityRegistration.user_id == review_in.reviewee_id
    ).first()
    if not target_registered:
        raise HTTPException(status_code=400, detail="对方未参加此活动")
    
    reviewer_profile = db.query(models.Profile).filter(
        models.Profile.user_id == current_user.id
    ).first()
    reviewee_profile = db.query(models.Profile).filter(
        models.Profile.user_id == review_in.reviewee_id
    ).first()
    
    if reviewer_profile and reviewee_profile and reviewer_profile.gender == reviewee_profile.gender:
        raise HTTPException(status_code=400, detail="只能评价异性")
    
    existing_review = db.query(models.ActivityReview).filter(
        models.ActivityReview.activity_id == activity_id,
        models.ActivityReview.reviewer_id == current_user.id,
        models.ActivityReview.reviewee_id == review_in.reviewee_id
    ).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="您已经评价过该用户")
    
    tags_json = json.dumps(review_in.tags, ensure_ascii=False) if review_in.tags else None
    
    review = models.ActivityReview(
        activity_id=activity_id,
        reviewer_id=current_user.id,
        reviewee_id=review_in.reviewee_id,
        rating=review_in.rating,
        tags=tags_json,
        comment=review_in.comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    
    tags_list = json.loads(review.tags) if review.tags else []
    return schemas.ActivityReviewResponse(
        id=review.id,
        activity_id=review.activity_id,
        reviewer_id=review.reviewer_id,
        reviewee_id=review.reviewee_id,
        rating=review.rating,
        tags=tags_list,
        comment=review.comment,
        created_at=review.created_at
    )


@router.get("/{activity_id}/reviews", response_model=list[schemas.ActivityReviewResponse])
def get_activity_reviews(
    activity_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reviews = db.query(models.ActivityReview).filter(
        models.ActivityReview.activity_id == activity_id
    ).all()
    
    result = []
    for review in reviews:
        tags_list = json.loads(review.tags) if review.tags else []
        result.append(schemas.ActivityReviewResponse(
            id=review.id,
            activity_id=review.activity_id,
            reviewer_id=review.reviewer_id,
            reviewee_id=review.reviewee_id,
            rating=review.rating,
            tags=tags_list,
            comment=review.comment,
            created_at=review.created_at
        ))
    
    return result
