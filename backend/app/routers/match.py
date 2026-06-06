import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.security import get_current_user, get_current_matchmaker

router = APIRouter(prefix="/match", tags=["智能匹配"])

EDUCATION_ORDER = {
    models.Education.HIGH_SCHOOL: 0,
    models.Education.COLLEGE: 1,
    models.Education.BACHELOR: 2,
    models.Education.MASTER: 3,
    models.Education.DOCTOR: 4,
}

INCOME_ORDER = {
    models.IncomeRange.BELOW_5K: 0,
    models.IncomeRange.K5_10K: 1,
    models.IncomeRange.K10_20K: 2,
    models.IncomeRange.K20_50K: 3,
    models.IncomeRange.ABOVE_50K: 4,
}


def calculate_match_score(
    user_profile: models.Profile,
    user_pref: models.Preference,
    target_profile: models.Profile,
    target_pref: models.Preference
) -> int:
    score = 0
    
    user_hobbies = set(json.loads(user_profile.hobbies)) if user_profile.hobbies else set()
    target_hobbies = set(json.loads(target_profile.hobbies)) if target_profile.hobbies else set()
    common_hobbies = user_hobbies & target_hobbies
    score += len(common_hobbies) * 10
    
    if user_profile.city and target_profile.city and user_profile.city == target_profile.city:
        score += 20
    
    if target_profile.education and user_pref.min_education:
        target_edu_level = EDUCATION_ORDER.get(target_profile.education, 0)
        min_edu_level = EDUCATION_ORDER.get(user_pref.min_education, 0)
        edu_diff = target_edu_level - min_edu_level
        if edu_diff >= 2:
            score += 10
        elif edu_diff >= 1:
            score += 5
    
    if user_profile.education and target_pref.min_education:
        user_edu_level = EDUCATION_ORDER.get(user_profile.education, 0)
        target_min_edu = EDUCATION_ORDER.get(target_pref.min_education, 0)
        edu_diff2 = user_edu_level - target_min_edu
        if edu_diff2 >= 2:
            score += 10
        elif edu_diff2 >= 1:
            score += 5
    
    if target_profile.income and user_pref.min_income:
        target_income_level = INCOME_ORDER.get(target_profile.income, 0)
        min_income_level = INCOME_ORDER.get(user_pref.min_income, 0)
        income_diff = target_income_level - min_income_level
        if income_diff >= 2:
            score += 10
        elif income_diff >= 1:
            score += 5
    
    if user_profile.income and target_pref.min_income:
        user_income_level = INCOME_ORDER.get(user_profile.income, 0)
        target_min_income = INCOME_ORDER.get(target_pref.min_income, 0)
        income_diff2 = user_income_level - target_min_income
        if income_diff2 >= 2:
            score += 10
        elif income_diff2 >= 1:
            score += 5
    
    return score


def is_age_in_range(age: int, min_age: int, max_age: int) -> bool:
    return min_age <= age <= max_age


def profile_to_card(profile: models.Profile, score: int) -> schemas.ProfileCardResponse:
    hobbies_list = json.loads(profile.hobbies) if profile.hobbies else []
    return schemas.ProfileCardResponse(
        user_id=profile.user_id,
        nickname=profile.nickname,
        age=profile.age,
        gender=profile.gender,
        height=profile.height,
        education=profile.education,
        occupation=profile.occupation,
        income=profile.income,
        city=profile.city,
        marital_status=profile.marital_status,
        hobbies=hobbies_list,
        introduction=profile.introduction,
        match_score=score
    )


@router.get("/recommendations", response_model=list[schemas.ProfileCardResponse])
def get_recommendations(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not user_profile or not user_profile.gender or user_profile.status != models.ProfileStatus.APPROVED:
        raise HTTPException(status_code=400, detail="请先完善资料并等待审核通过")
    
    user_pref = db.query(models.Preference).filter(models.Preference.user_id == current_user.id).first()
    if not user_pref:
        raise HTTPException(status_code=400, detail="请先设置择偶条件")
    
    target_gender = models.Gender.FEMALE if user_profile.gender == models.Gender.MALE else models.Gender.MALE
    
    viewed_user_ids = [v.viewed_user_id for v in current_user.viewed_profiles]
    
    candidates = db.query(models.Profile).filter(
        models.Profile.gender == target_gender,
        models.Profile.status == models.ProfileStatus.APPROVED,
        models.Profile.user_id != current_user.id,
        ~models.Profile.user_id.in_(viewed_user_ids) if viewed_user_ids else True
    ).all()
    
    matched_candidates = []
    
    for candidate in candidates:
        if not candidate.age or not candidate.height:
            continue
        
        candidate_pref = db.query(models.Preference).filter(
            models.Preference.user_id == candidate.user_id
        ).first()
        if not candidate_pref:
            continue
        
        if not is_age_in_range(candidate.age, user_pref.min_age, user_pref.max_age):
            continue
        if not is_age_in_range(user_profile.age, candidate_pref.min_age, candidate_pref.max_age):
            continue
        
        if not (user_pref.min_height <= candidate.height <= user_pref.max_height):
            continue
        if candidate_pref.min_height and candidate_pref.max_height:
            if not (candidate_pref.min_height <= user_profile.height <= candidate_pref.max_height):
                continue
        
        if candidate.education and user_pref.min_education:
            if EDUCATION_ORDER.get(candidate.education, 0) < EDUCATION_ORDER.get(user_pref.min_education, 0):
                continue
        
        if user_profile.education and candidate_pref.min_education:
            if EDUCATION_ORDER.get(user_profile.education, 0) < EDUCATION_ORDER.get(candidate_pref.min_education, 0):
                continue
        
        if candidate.income and user_pref.min_income:
            if INCOME_ORDER.get(candidate.income, 0) < INCOME_ORDER.get(user_pref.min_income, 0):
                continue
        
        if user_profile.income and candidate_pref.min_income:
            if INCOME_ORDER.get(user_profile.income, 0) < INCOME_ORDER.get(candidate_pref.min_income, 0):
                continue
        
        if candidate.marital_status == models.MaritalStatus.DIVORCED and not user_pref.accept_divorced:
            continue
        if user_profile.marital_status == models.MaritalStatus.DIVORCED and not candidate_pref.accept_divorced:
            continue
        
        if candidate.has_children and not user_pref.accept_with_children:
            continue
        if user_profile.has_children and not candidate_pref.accept_with_children:
            continue
        
        score = calculate_match_score(user_profile, user_pref, candidate, candidate_pref)
        matched_candidates.append((candidate, score))
    
    matched_candidates.sort(key=lambda x: x[1], reverse=True)
    top_10 = matched_candidates[:10]
    
    for candidate, _ in top_10:
        viewed = models.ViewedProfile(
            viewer_id=current_user.id,
            viewed_user_id=candidate.user_id
        )
        db.add(viewed)
    db.commit()
    
    return [profile_to_card(profile, score) for profile, score in top_10]


@router.get("/recommendations/refresh", response_model=list[schemas.ProfileCardResponse])
def refresh_recommendations(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    viewed = db.query(models.ViewedProfile).filter(
        models.ViewedProfile.viewer_id == current_user.id
    ).delete()
    db.commit()
    
    return get_recommendations(current_user, db)


@router.post("/manual")
def manual_match(
    match_data: schemas.ManualMatch,
    current_matchmaker: models.User = Depends(get_current_matchmaker),
    db: Session = Depends(get_db)
):
    male = db.query(models.User).filter(models.User.id == match_data.male_user_id).first()
    female = db.query(models.User).filter(models.User.id == match_data.female_user_id).first()
    
    if not male or not female:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    male_profile = db.query(models.Profile).filter(models.Profile.user_id == male.id).first()
    female_profile = db.query(models.Profile).filter(models.Profile.user_id == female.id).first()
    
    if not male_profile or not female_profile:
        raise HTTPException(status_code=400, detail="用户资料不完整")
    
    notification1 = models.Notification(
        user_id=male.id,
        title="红娘为您推荐了一位佳人",
        content=f"红娘为您推荐了 {female_profile.nickname or '一位会员'}，快去看看吧！",
        type="manual_match"
    )
    notification2 = models.Notification(
        user_id=female.id,
        title="红娘为您推荐了一位佳人",
        content=f"红娘为您推荐了 {male_profile.nickname or '一位会员'}，快去看看吧！",
        type="manual_match"
    )
    db.add(notification1)
    db.add(notification2)
    db.commit()
    
    return {"message": "牵线成功，双方已收到通知"}
