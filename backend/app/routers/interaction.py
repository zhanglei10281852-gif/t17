from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import get_current_user

router = APIRouter(prefix="/interaction", tags=["互动管理"])


def mask_phone(phone: str) -> str:
    if len(phone) >= 7:
        return phone[:3] + "*" * (len(phone) - 7) + phone[-4:]
    return phone


def profile_to_response(profile: models.Profile) -> schemas.ProfileResponse:
    import json
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


@router.post("/like/{user_id}")
def like_user(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能给自己点赞")
    
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    existing_like = db.query(models.Like).filter(
        models.Like.from_user_id == current_user.id,
        models.Like.to_user_id == user_id
    ).first()
    
    if existing_like:
        return {"message": "已经心动过了", "is_match": False}
    
    like = models.Like(from_user_id=current_user.id, to_user_id=user_id)
    db.add(like)
    
    reverse_like = db.query(models.Like).filter(
        models.Like.from_user_id == user_id,
        models.Like.to_user_id == current_user.id
    ).first()
    
    is_match = False
    if reverse_like:
        is_match = True
        match = models.Match(user1_id=current_user.id, user2_id=user_id)
        db.add(match)
        
        notification1 = models.Notification(
            user_id=current_user.id,
            title="配对成功！",
            content="恭喜您配对成功，快去查看对方的联系方式吧！",
            type="match"
        )
        notification2 = models.Notification(
            user_id=user_id,
            title="配对成功！",
            content="恭喜您配对成功，快去查看对方的联系方式吧！",
            type="match"
        )
        db.add(notification1)
        db.add(notification2)
    else:
        notification = models.Notification(
            user_id=user_id,
            title="有人对您心动了",
            content="有人对您表达了好感，快去看看吧！",
            type="like"
        )
        db.add(notification)
    
    db.commit()
    
    return {"message": "心动成功", "is_match": is_match}


@router.get("/likes/received", response_model=list[schemas.LikeResponse])
def get_received_likes(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    likes = db.query(models.Like).filter(
        models.Like.to_user_id == current_user.id
    ).order_by(models.Like.created_at.desc()).all()
    
    result = []
    for like in likes:
        from_profile = db.query(models.Profile).filter(
            models.Profile.user_id == like.from_user_id
        ).first()
        like_data = schemas.LikeResponse(
            id=like.id,
            from_user_id=like.from_user_id,
            to_user_id=like.to_user_id,
            created_at=like.created_at,
            from_user_profile=profile_to_response(from_profile) if from_profile else None
        )
        result.append(like_data)
    
    return result


@router.get("/likes/sent", response_model=list[schemas.LikeResponse])
def get_sent_likes(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    likes = db.query(models.Like).filter(
        models.Like.from_user_id == current_user.id
    ).order_by(models.Like.created_at.desc()).all()
    
    result = []
    for like in likes:
        to_profile = db.query(models.Profile).filter(
            models.Profile.user_id == like.to_user_id
        ).first()
        like_data = schemas.LikeResponse(
            id=like.id,
            from_user_id=like.from_user_id,
            to_user_id=like.to_user_id,
            created_at=like.created_at,
            to_user_profile=profile_to_response(to_profile) if to_profile else None
        )
        result.append(like_data)
    
    return result


@router.get("/matches", response_model=list[schemas.MatchResponse])
def get_matches(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    matches = db.query(models.Match).filter(
        (models.Match.user1_id == current_user.id) | (models.Match.user2_id == current_user.id)
    ).order_by(models.Match.created_at.desc()).all()
    
    result = []
    for match in matches:
        other_user_id = match.user2_id if match.user1_id == current_user.id else match.user1_id
        other_user = db.query(models.User).filter(models.User.id == other_user_id).first()
        other_profile = db.query(models.Profile).filter(
            models.Profile.user_id == other_user_id
        ).first()
        
        match_data = schemas.MatchResponse(
            id=match.id,
            user1_id=match.user1_id,
            user2_id=match.user2_id,
            created_at=match.created_at,
            other_user_profile=profile_to_response(other_profile) if other_profile else None,
            masked_phone=mask_phone(other_user.phone) if other_user else None
        )
        result.append(match_data)
    
    return result


@router.get("/notifications", response_model=list[schemas.NotificationResponse])
def get_notifications(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notifications = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id
    ).order_by(models.Notification.created_at.desc()).all()
    
    return notifications


@router.post("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    notification.is_read = True
    db.commit()
    
    return {"message": "已标记为已读"}
