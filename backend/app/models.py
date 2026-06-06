from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    MEMBER = "member"
    MATCHMAKER = "matchmaker"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class Education(str, enum.Enum):
    HIGH_SCHOOL = "high_school"
    COLLEGE = "college"
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTOR = "doctor"


class IncomeRange(str, enum.Enum):
    BELOW_5K = "below_5k"
    K5_10K = "5k_10k"
    K10_20K = "10k_20k"
    K20_50K = "20k_50k"
    ABOVE_50K = "above_50k"


class MaritalStatus(str, enum.Enum):
    SINGLE = "single"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


class ProfileStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ActivityStatus(str, enum.Enum):
    REGISTERING = "registering"
    FULL = "full"
    ONGOING = "ongoing"
    ENDED = "ended"


class ActivityType(str, enum.Enum):
    EIGHT_MINUTE = "eight_minute"
    OUTDOOR = "outdoor"
    THEME_PARTY = "theme_party"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.MEMBER, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False)
    preference = relationship("Preference", back_populates="user", uselist=False)
    sent_likes = relationship("Like", foreign_keys="Like.from_user_id", back_populates="from_user")
    received_likes = relationship("Like", foreign_keys="Like.to_user_id", back_populates="to_user")
    matches_as_user1 = relationship("Match", foreign_keys="Match.user1_id", back_populates="user1")
    matches_as_user2 = relationship("Match", foreign_keys="Match.user2_id", back_populates="user2")
    viewed_profiles = relationship("ViewedProfile", foreign_keys="ViewedProfile.viewer_id", back_populates="viewer")
    activity_registrations = relationship("ActivityRegistration", back_populates="user")
    sent_reviews = relationship("ActivityReview", foreign_keys="ActivityReview.reviewer_id", back_populates="reviewer")
    received_reviews = relationship("ActivityReview", foreign_keys="ActivityReview.reviewee_id", back_populates="reviewee")
    notifications = relationship("Notification", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    nickname = Column(String(50))
    gender = Column(SQLEnum(Gender))
    birth_date = Column(Date)
    height = Column(Integer)
    weight = Column(Integer)
    education = Column(SQLEnum(Education))
    occupation = Column(String(100))
    income = Column(SQLEnum(IncomeRange))
    city = Column(String(50))
    hometown = Column(String(50))
    marital_status = Column(SQLEnum(MaritalStatus))
    has_children = Column(Boolean, default=False)
    smoking = Column(Boolean, default=False)
    drinking = Column(Boolean, default=False)
    hobbies = Column(Text)
    introduction = Column(Text)
    status = Column(SQLEnum(ProfileStatus), default=ProfileStatus.DRAFT)
    reject_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    min_age = Column(Integer, default=20)
    max_age = Column(Integer, default=40)
    min_height = Column(Integer, default=150)
    max_height = Column(Integer, default=200)
    min_education = Column(SQLEnum(Education), default=Education.HIGH_SCHOOL)
    min_income = Column(SQLEnum(IncomeRange), default=IncomeRange.BELOW_5K)
    accept_divorced = Column(Boolean, default=True)
    accept_with_children = Column(Boolean, default=True)
    preferred_cities = Column(Text)

    user = relationship("User", back_populates="preference")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_likes")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_likes")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user1 = relationship("User", foreign_keys=[user1_id], back_populates="matches_as_user1")
    user2 = relationship("User", foreign_keys=[user2_id], back_populates="matches_as_user2")


class ViewedProfile(Base):
    __tablename__ = "viewed_profiles"

    id = Column(Integer, primary_key=True, index=True)
    viewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    viewed_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    viewer = relationship("User", foreign_keys=[viewer_id], back_populates="viewed_profiles")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    activity_time = Column(DateTime, nullable=False)
    location = Column(String(200), nullable=False)
    activity_type = Column(SQLEnum(ActivityType), nullable=False)
    male_limit = Column(Integer, nullable=False)
    female_limit = Column(Integer, nullable=False)
    min_age = Column(Integer, default=18)
    max_age = Column(Integer, default=60)
    fee = Column(Float, default=0)
    description = Column(Text)
    status = Column(SQLEnum(ActivityStatus), default=ActivityStatus.REGISTERING)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    registrations = relationship("ActivityRegistration", back_populates="activity")
    reviews = relationship("ActivityReview", back_populates="activity")


class ActivityRegistration(Base):
    __tablename__ = "activity_registrations"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)

    activity = relationship("Activity", back_populates="registrations")
    user = relationship("User", back_populates="activity_registrations")


class ActivityReview(Base):
    __tablename__ = "activity_reviews"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    tags = Column(Text)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    activity = relationship("Activity", back_populates="reviews")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="sent_reviews")
    reviewee = relationship("User", foreign_keys=[reviewee_id], back_populates="received_reviews")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    type = Column(String(50))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
