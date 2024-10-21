from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker   #ORM 모델을 사용하여 테이블의 구조를 객체로 표현
from sqlalchemy.ext.declarative import declarative_base
import pymysql
import cryptography
#from env.db_env import user, pw, host, db_name
import os
from dotenv import load_dotenv, find_dotenv

# .env 파일에서 환경 변수 로드
# load_dotenv()


#sqplite3 엔진을 정의, DB파일 todo.sqlite3
DB_URL = 'sqlite:///prjmyapp.sqlite3'
DB_URL_2 = 'sqlite:///todo.sqlite3'

# 환경변수에서 mysql 접속 정보 불러오기
# user= os.getenv("user")
# password= os.getenv("pw")
# host= os.getenv("host")
# db_name= os.getenv("db_name")
# print(user)

# 환경변수 출력하여 확인
# print(f"user: {user}, password: {password}, host: {host}, db_name: {db_name}")

#mysql 엔진을 정의
# DB_URL = f"mysql+pymysql://{user}:{password}@{host}:3306/{db_name}"

# mysql 연결 객체 생성
# engine = create_engine(DB_URL)

# 데이터베이스에 연결하는 엔진을 생성하는 함수. - sqlite3
engine = create_engine(DB_URL,connect_args={'check_same_thread': False})

# 데이터베이스와 상호 작용하는 세션을 생성하는 클래스
# 애플리케이션에서 데이터베이스와 상호작용할 때 세션을 사용하여 데이터베이스 트랜잭션(transaction)을 관리함.
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 선언적 모델링을 위한 기본 클래스
Base = declarative_base()  # 이 클래스는 다른 ORM모델을 생성하는 기반이 됨.