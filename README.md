# Marketplace - 중고거래 플랫폼

안전하고 사용자 친화적인 중고거래 플랫폼입니다.

## 주요 기능

- 사용자 인증
  - 회원가입 및 로그인 시스템
  - 사용자 프로필
  - 비밀번호 재설정 기능

- 상품 관리
  - 상품 등록, 조회, 수정, 삭제
  - 상품 이미지 업로드
  - 상품 카테고리
  - 상품 검색 및 필터링

- 메시징 시스템
  - 구매자와 판매자 간 실시간 메시징
  - 메시지 알림
  - 메시지 히스토리

- 관리자 패널
  - 사용자 관리
  - 상품 관리
  - 메시지 모니터링
  - 플랫폼 통계

- 보안 기능
  - 사용자 차단 시스템
  - 상품 차단 시스템
  - 안전한 비밀번호 해싱
  - 입력 검증

## 설치 방법

1. 저장소 클론:
```bash
git clone https://github.com/yourusername/marketplace.git
cd marketplace
```

2. 가상환경 생성 및 활성화:
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows의 경우:
venv\Scripts\activate
# macOS/Linux의 경우:
source venv/bin/activate
```

3. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정:
```bash
# .env 파일 생성
echo "SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///marketplace.db
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password" > .env
```

5. 데이터베이스 초기화:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. 업로드 디렉토리 생성:
```bash
mkdir -p app/static/uploads
```

7. 애플리케이션 실행:
```bash
flask run
```

## 환경 변수 설정

`.env` 파일에서 다음 환경 변수를 설정할 수 있습니다:

- `SECRET_KEY`: Flask 시크릿 키
- `DATABASE_URL`: 데이터베이스 연결 URL
- `MAIL_USERNAME`: 이메일 알림을 위한 이메일 주소
- `MAIL_PASSWORD`: 이메일 알림을 위한 이메일 비밀번호

## 사용 방법

1. 회원가입 또는 기존 계정으로 로그인
2. 상품 목록을 둘러보거나 검색 기능 사용
3. 메시징 시스템을 통해 판매자와 소통
4. 자신의 상품 등록
5. 계정 및 상품 관리

## 관리자 계정 생성

관리자 계정을 생성하려면:

1. 일반 계정으로 회원가입
2. Flask 쉘에서 다음 명령어 실행:
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='your-username').first()
    user.is_admin = True
    db.session.commit()
```

## 주요 페이지

- 메인 페이지: `http://localhost:5000`
- 회원가입: `http://localhost:5000/register`
- 로그인: `http://localhost:5000/login`
- 상품 목록: `http://localhost:5000/products`
- 상품 등록: `http://localhost:5000/products/new` (로그인 필요)
- 메시지: `http://localhost:5000/messages` (로그인 필요)
- 관리자 페이지: `http://localhost:5000/admin` (관리자 권한 필요)

## 문제 해결

문제가 발생하면 다음을 확인해주세요:

1. 모든 패키지가 제대로 설치되었는지 확인
2. 환경 변수가 올바르게 설정되었는지 확인
3. 데이터베이스가 초기화되었는지 확인
4. 업로드 디렉토리가 생성되었는지 확인

## 기여 방법

1. 저장소를 포크
2. 기능 브랜치 생성
3. 변경사항 커밋
4. 브랜치에 푸시
5. Pull Request 생성

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 LICENSE 파일을 참조하세요.

## 지원

지원이 필요하시면 support@marketplace.com으로 이메일을 보내거나 저장소에 이슈를 생성해주세요.
