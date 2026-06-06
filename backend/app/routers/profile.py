import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import get_current_user, get_current_matchmaker

router = APIRouter(prefix="/profile", tags=["会员资料"])


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


@router.get("/me", response_model=schemas.ProfileResponse)
def get_my_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="资料不存在")
    return profile_to_response(profile)


@router.put("/me", response_model=schemas.ProfileResponse)
def update_my_profile(
    profile_in: schemas.ProfileUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="资料不存在")
    
    update_data = profile_in.model_dump(exclude_unset=True)
    
    if "hobbies" in update_data and update_data["hobbies"] is not None:
        update_data["hobbies"] = json.dumps(update_data["hobbies"], ensure_ascii=False)
    
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    profile.status = models.ProfileStatus.PENDING
    
    db.commit()
    db.refresh(profile)
    
    return profile_to_response(profile)


@router.get("/preference/me", response_model=schemas.PreferenceResponse)
def get_my_preference(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    preference = db.query(models.Preference).filter(models.Preference.user_id == current_user.id).first()
    if not preference:
        raise HTTPException(status_code=404, detail="择偶条件不存在")
    
    cities_list = json.loads(preference.preferred_cities) if preference.preferred_cities else []
    return schemas.PreferenceResponse(
        id=preference.id,
        user_id=preference.user_id,
        min_age=preference.min_age,
        max_age=preference.max_age,
        min_height=preference.min_height,
        max_height=preference.max_height,
        min_education=preference.min_education,
        min_income=preference.min_income,
        accept_divorced=preference.accept_divorced,
        accept_with_children=preference.accept_with_children,
        preferred_cities=cities_list
    )


@router.put("/preference/me", response_model=schemas.PreferenceResponse)
def update_my_preference(
    preference_in: schemas.PreferenceUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    preference = db.query(models.Preference).filter(models.Preference.user_id == current_user.id).first()
    if not preference:
        raise HTTPException(status_code=404, detail="择偶条件不存在")
    
    update_data = preference_in.model_dump(exclude_unset=True)
    
    if "preferred_cities" in update_data and update_data["preferred_cities"] is not None:
        update_data["preferred_cities"] = json.dumps(update_data["preferred_cities"], ensure_ascii=False)
    
    for key, value in update_data.items():
        setattr(preference, key, value)
    
    db.commit()
    db.refresh(preference)
    
    cities_list = json.loads(preference.preferred_cities) if preference.preferred_cities else []
    return schemas.PreferenceResponse(
        id=preference.id,
        user_id=preference.user_id,
        min_age=preference.min_age,
        max_age=preference.max_age,
        min_height=preference.min_height,
        max_height=preference.max_height,
        min_education=preference.min_education,
        min_income=preference.min_income,
        accept_divorced=preference.accept_divorced,
        accept_with_children=preference.accept_with_children,
        preferred_cities=cities_list
    )


@router.get("/{user_id}", response_model=schemas.ProfileResponse)
def get_user_profile(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="资料不存在")
    
    if profile.status != models.ProfileStatus.APPROVED and user_id != current_user.id:
        if current_user.role != models.UserRole.MATCHMAKER:
            raise HTTPException(status_code=403, detail="该资料未审核通过")
    
    return profile_to_response(profile)


@router.get("/matchmaker/pending", response_model=list[schemas.ProfileResponse])
def get_pending_profiles(
    skip: int = 0,
    limit: int = 20,
    current_matchmaker: models.User = Depends(get_current_matchmaker),
    db: Session = Depends(get_db)
):
    profiles = db.query(models.Profile).filter(
        models.Profile.status == models.ProfileStatus.PENDING
    ).offset(skip).limit(limit).all()
    
    return [profile_to_response(p) for p in profiles]


@router.post("/matchmaker/review/{profile_id}")
def review_profile(
    profile_id: int,
    review_data: schemas.ProfileReview,
    current_matchmaker: models.User = Depends(get_current_matchmaker),
    db: Session = Depends(get_db)
):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="资料不存在")
    
    profile.status = review_data.status
    if review_data.status == models.ProfileStatus.REJECTED:
        profile.reject_reason = review_data.reject_reason
    
    notification = models.Notification(
        user_id=profile.user_id,
        title="资料审核结果",
        content=f"您的资料已{'通过' if review_data.status == models.ProfileStatus.APPROVED else '被驳回'}",
        type="profile_review"
    )
    db.add(notification)
    
    db.commit()
    
    return {"message": "审核完成"}
