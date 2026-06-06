import json
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.security import hash_password


def init_database():
    db = SessionLocal()
    try:
        matchmaker_count = db.query(models.User).filter(
            models.User.role == models.UserRole.MATCHMAKER
        ).count()
        
        if matchmaker_count == 0:
            create_matchmakers(db)
            create_mock_members(db)
            create_mock_activities(db)
            print("初始化数据完成")
        else:
            print("数据已存在，跳过初始化")
    except Exception as e:
        print(f"初始化数据失败: {e}")
        db.rollback()
    finally:
        db.close()


def create_matchmakers(db: Session):
    matchmakers = [
        {"phone": "matchmaker1", "password": "mm123"},
        {"phone": "matchmaker2", "password": "mm123"},
    ]
    
    for mm in matchmakers:
        user = models.User(
            phone=mm["phone"],
            hashed_password=hash_password(mm["password"]),
            role=models.UserRole.MATCHMAKER
        )
        db.add(user)
    
    db.commit()


def create_mock_members(db: Session):
    male_names = ["张伟", "王强", "李明", "刘洋", "陈杰", "杨帆", "赵磊", "黄涛", "周鹏", "吴凯"]
    female_names = ["李娜", "王芳", "张丽", "刘婷", "陈雪", "杨倩", "赵敏", "黄丽", "周燕", "吴霞"]
    
    educations = [models.Education.HIGH_SCHOOL, models.Education.COLLEGE, 
                  models.Education.BACHELOR, models.Education.MASTER, models.Education.DOCTOR]
    incomes = [models.IncomeRange.BELOW_5K, models.IncomeRange.K5_10K, 
               models.IncomeRange.K10_20K, models.IncomeRange.K20_50K, models.IncomeRange.ABOVE_50K]
    marital_statuses = [models.MaritalStatus.SINGLE, models.MaritalStatus.SINGLE, 
                        models.MaritalStatus.SINGLE, models.MaritalStatus.DIVORCED]
    cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京", "西安", "重庆"]
    occupations = ["程序员", "设计师", "教师", "医生", "律师", "销售", "会计", "工程师", "运营", "产品经理"]
    hobbies_pool = ["运动", "读书", "旅行", "美食", "音乐", "电影", "游戏", "宠物", "摄影", "烹饪"]
    
    for i in range(10):
        phone = f"1380000{i+1:04d}"
        user = models.User(
            phone=phone,
            hashed_password=hash_password("user123"),
            role=models.UserRole.MEMBER
        )
        db.add(user)
        db.flush()
        
        birth_year = 1995 + (i % 8)
        birth_month = (i % 12) + 1
        birth_day = (i % 28) + 1
        
        hobbies = [hobbies_pool[i % 10], hobbies_pool[(i + 2) % 10], hobbies_pool[(i + 5) % 10]]
        
        profile = models.Profile(
            user_id=user.id,
            nickname=male_names[i],
            gender=models.Gender.MALE,
            birth_date=date(birth_year, birth_month, birth_day),
            height=172 + (i % 12),
            weight=65 + (i % 15),
            education=educations[(i + 1) % 5],
            occupation=occupations[i],
            income=incomes[(i + 1) % 5],
            city=cities[i % 5],
            hometown=cities[(i + 3) % 10],
            marital_status=marital_statuses[i % 4],
            has_children=bool(i % 5 == 4),
            smoking=bool(i % 5 == 0),
            drinking=bool(i % 3 == 0),
            hobbies=json.dumps(hobbies, ensure_ascii=False),
            introduction=f"大家好，我是{male_names[i]}，性格开朗，热爱生活，希望找到一个温柔善良的另一半。",
            status=models.ProfileStatus.APPROVED
        )
        db.add(profile)
        
        preference = models.Preference(
            user_id=user.id,
            min_age=20,
            max_age=38,
            min_height=155,
            max_height=178,
            min_education=models.Education.HIGH_SCHOOL,
            min_income=models.IncomeRange.BELOW_5K,
            accept_divorced=True,
            accept_with_children=False,
            preferred_cities=json.dumps([cities[i % 5], cities[(i + 1) % 5]], ensure_ascii=False)
        )
        db.add(preference)
    
    for i in range(10):
        phone = f"1390000{i+1:04d}"
        user = models.User(
            phone=phone,
            hashed_password=hash_password("user123"),
            role=models.UserRole.MEMBER
        )
        db.add(user)
        db.flush()
        
        birth_year = 1996 + (i % 8)
        birth_month = (i % 12) + 1
        birth_day = (i % 28) + 1
        
        hobbies = [hobbies_pool[(i + 1) % 10], hobbies_pool[(i + 4) % 10], hobbies_pool[(i + 7) % 10]]
        
        profile = models.Profile(
            user_id=user.id,
            nickname=female_names[i],
            gender=models.Gender.FEMALE,
            birth_date=date(birth_year, birth_month, birth_day),
            height=158 + (i % 15),
            weight=48 + (i % 12),
            education=educations[i % 5],
            occupation=occupations[(i + 2) % 10],
            income=incomes[i % 5],
            city=cities[i % 5],
            hometown=cities[(i + 4) % 10],
            marital_status=marital_statuses[(i + 1) % 4],
            has_children=bool(i % 6 == 5),
            smoking=False,
            drinking=bool(i % 4 == 0),
            hobbies=json.dumps(hobbies, ensure_ascii=False),
            introduction=f"大家好，我是{female_names[i]}，温柔善良，热爱生活，期待遇到那个对的人。",
            status=models.ProfileStatus.APPROVED
        )
        db.add(profile)
        
        preference = models.Preference(
            user_id=user.id,
            min_age=22,
            max_age=40,
            min_height=165,
            max_height=190,
            min_education=models.Education.HIGH_SCHOOL,
            min_income=models.IncomeRange.BELOW_5K,
            accept_divorced=True,
            accept_with_children=False,
            preferred_cities=json.dumps([cities[i % 5], cities[(i + 2) % 5]], ensure_ascii=False)
        )
        db.add(preference)
    
    db.commit()


def create_mock_activities(db: Session):
    matchmaker = db.query(models.User).filter(
        models.User.role == models.UserRole.MATCHMAKER
    ).first()
    
    if not matchmaker:
        return
    
    activities_data = [
        {
            "name": "8分钟约会·春季专场",
            "activity_time": datetime.utcnow() + timedelta(days=7),
            "location": "北京市朝阳区国贸大厦A座20楼",
            "activity_type": models.ActivityType.EIGHT_MINUTE,
            "male_limit": 15,
            "female_limit": 15,
            "min_age": 22,
            "max_age": 35,
            "fee": 99.0,
            "description": "轻松愉快的8分钟约会，让你在短时间内认识更多异性朋友。"
        },
        {
            "name": "户外徒步联谊活动",
            "activity_time": datetime.utcnow() + timedelta(days=14),
            "location": "北京香山公园",
            "activity_type": models.ActivityType.OUTDOOR,
            "male_limit": 20,
            "female_limit": 20,
            "min_age": 20,
            "max_age": 40,
            "fee": 50.0,
            "description": "一起徒步登山，在大自然中邂逅美好缘分。"
        },
        {
            "name": "红酒品鉴主题派对",
            "activity_time": datetime.utcnow() + timedelta(days=21),
            "location": "上海市静安区五星酒店宴会厅",
            "activity_type": models.ActivityType.THEME_PARTY,
            "male_limit": 25,
            "female_limit": 25,
            "min_age": 25,
            "max_age": 45,
            "fee": 199.0,
            "description": "高端红酒品鉴会，品味生活，遇见对的人。"
        }
    ]
    
    for act_data in activities_data:
        activity = models.Activity(
            **act_data,
            created_by=matchmaker.id,
            status=models.ActivityStatus.REGISTERING
        )
        db.add(activity)
    
    db.commit()
