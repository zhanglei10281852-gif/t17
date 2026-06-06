from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models import (
    UserRole, Gender, Education, IncomeRange, MaritalStatus,
    ProfileStatus, ActivityStatus, ActivityType
)


class UserBase(BaseModel):
    phone: str


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.MEMBER


class UserLogin(BaseModel):
    phone: str
    password: str


class UserResponse(BaseModel):
    id: int
    phone: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class ProfileBase(BaseModel):
    nickname: Optional[str] = None
    gender: Optional[Gender] = None
    birth_date: Optional[date] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    education: Optional[Education] = None
    occupation: Optional[str] = None
    income: Optional[IncomeRange] = None
    city: Optional[str] = None
    hometown: Optional[str] = None
    marital_status: Optional[MaritalStatus] = None
    has_children: Optional[bool] = False
    smoking: Optional[bool] = False
    drinking: Optional[bool] = False
    hobbies: Optional[List[str]] = None
    introduction: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    nickname: Optional[str] = None
    gender: Optional[Gender] = None
    birth_date: Optional[date] = None
    age: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    education: Optional[Education] = None
    occupation: Optional[str] = None
    income: Optional[IncomeRange] = None
    city: Optional[str] = None
    hometown: Optional[str] = None
    marital_status: Optional[MaritalStatus] = None
    has_children: Optional[bool] = False
    smoking: Optional[bool] = False
    drinking: Optional[bool] = False
    hobbies: Optional[List[str]] = None
    introduction: Optional[str] = None
    status: ProfileStatus
    reject_reason: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True


class ProfileCardResponse(BaseModel):
    user_id: int
    nickname: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    height: Optional[int] = None
    education: Optional[Education] = None
    occupation: Optional[str] = None
    income: Optional[IncomeRange] = None
    city: Optional[str] = None
    marital_status: Optional[MaritalStatus] = None
    hobbies: Optional[List[str]] = None
    introduction: Optional[str] = None
    match_score: float = 0

    class Config:
        from_attributes = True


class PreferenceBase(BaseModel):
    min_age: Optional[int] = 20
    max_age: Optional[int] = 40
    min_height: Optional[int] = 150
    max_height: Optional[int] = 200
    min_education: Optional[Education] = Education.HIGH_SCHOOL
    min_income: Optional[IncomeRange] = IncomeRange.BELOW_5K
    accept_divorced: Optional[bool] = True
    accept_with_children: Optional[bool] = True
    preferred_cities: Optional[List[str]] = None


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceUpdate(PreferenceBase):
    pass


class PreferenceResponse(PreferenceBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class LikeResponse(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    created_at: datetime
    from_user_profile: Optional[ProfileResponse] = None
    to_user_profile: Optional[ProfileResponse] = None

    class Config:
        from_attributes = True


class MatchResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    created_at: datetime
    other_user_profile: Optional[ProfileResponse] = None
    masked_phone: Optional[str] = None

    class Config:
        from_attributes = True


class ActivityBase(BaseModel):
    name: str
    activity_time: datetime
    location: str
    activity_type: ActivityType
    male_limit: int
    female_limit: int
    min_age: int = 18
    max_age: int = 60
    fee: float = 0
    description: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    activity_time: Optional[datetime] = None
    location: Optional[str] = None
    activity_type: Optional[ActivityType] = None
    male_limit: Optional[int] = None
    female_limit: Optional[int] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    fee: Optional[float] = None
    description: Optional[str] = None
    status: Optional[ActivityStatus] = None


class ActivityResponse(ActivityBase):
    id: int
    status: ActivityStatus
    created_by: int
    created_at: datetime
    male_registered: int = 0
    female_registered: int = 0

    class Config:
        from_attributes = True


class ActivityRegistrationResponse(BaseModel):
    id: int
    activity_id: int
    user_id: int
    registered_at: datetime
    user_profile: Optional[ProfileResponse] = None

    class Config:
        from_attributes = True


class ActivityReviewCreate(BaseModel):
    reviewee_id: int
    rating: int = Field(..., ge=1, le=5)
    tags: Optional[List[str]] = None
    comment: Optional[str] = None


class ActivityReviewResponse(BaseModel):
    id: int
    activity_id: int
    reviewer_id: int
    reviewee_id: int
    rating: int
    tags: Optional[List[str]] = None
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ProfileReview(BaseModel):
    status: ProfileStatus
    reject_reason: Optional[str] = None


class ManualMatch(BaseModel):
    male_user_id: int
    female_user_id: int


class StatisticsResponse(BaseModel):
    total_members: int
    male_count: int
    female_count: int
    male_ratio: float
    total_matches: int
    total_activities: int
    total_registrations: int
    activity_participation_rate: float
    pending_profiles: int


class NotificationResponse(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    type: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
