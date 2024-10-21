# Multi-Feature Application 🌐

**Multi-Feature Application**은 여러 기능을 하나의 웹 애플리케이션에서 통합한 프로젝트입니다.  
이 프로젝트는 **FastAPI**와 **SQLite**를 사용해 개발되었으며, **To-Do 리스트**와 **Sales 대시보드**, **얼굴 인식** 기능을 포함합니다.

## 📌 프로젝트 소개

이 프로젝트의 목적은 다양한 기능을 가진 웹 애플리케이션을 개발하며 **웹 프레임워크(FastAPI)**와 **데이터베이스(SQLAlchemy, SQLite)** 사용 능력을 강화하는 것입니다.  
사용자는 이 애플리케이션을 통해 할 일을 관리하거나 월별 매출을 시각화할 수 있습니다.

---

## 🚀 주요 기능

1. **To-Do 리스트**:
   - 작업 추가 및 관리 기능
   - 할 일 목록을 직관적으로 확인 가능

2. **Sales 대시보드**:
   - 월별 매출 데이터를 추가하고 시각화
   - 기존 매출 데이터 수정 기능 제공
  
3. **얼굴 인식**:
   - 사용자 얼굴 인식 기능
   - 저장된 얼굴과 인식된 얼굴 비교 기능

---

## 🔧 사용한 기술 스택

- **Python**: 백엔드 개발
- **FastAPI**: 웹 프레임워크
- **SQLite**: 데이터베이스
- **SQLAlchemy**: ORM(Object Relational Mapping) 사용
- **Bootstrap 5**: 프론트엔드 스타일링
- **DBeaver**: 데이터베이스 관리 툴

---

## 🛠️ 설치 및 실행 방법


### 1. 프로젝트 클론
'''bash

    git clone https://github.com/hunbo/project_myapp
    cd multi-feature-app

### 2. 가상환경 생성 및 패키지 설치
    python -m venv venv
    source venv/bin/activate  # (Windows: venv\Scripts\activate)
    pip install -r requirements.txt

### 3. 서버 실행
    uvicorn main:app --reload

### 4. 웹 브라우저에서 실행
    http://127.0.0.1:8000

---

📊 주요 화면
메인 페이지:

사용자가 To-Do 리스트와 Sales 대시보드, 얼굴 인식 대시보드로 이동할 수 있는 네비게이션 제공

To-Do 리스트:

할 일을 추가하고 관리하는 페이지

Sales 대시보드:

월별 매출 데이터를 입력하고 수정하는 페이지

얼굴 인식:

저장된 얼굴과 인식되는 얼굴과 비교 대조하는 페이지

🤝 기여 방법
- 이 저장소를 포크합니다.
- 새로운 브랜치를 생성합니다.
- 기능을 추가한 후 커밋합니다.
- Pull Request를 생성합니다.

📧 문의
 이 프로젝트에 대한 질문이 있으시면 언제든지 저에게 연락주세요!
 이메일: 19010247shim@gmail.com

