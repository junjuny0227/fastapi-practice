# GSM SV 배포 가이드

FastAPI 게시판 서버를 GSM SV 학교 서버에 Docker로 배포하는 전체 과정입니다.

---

## 1. VM 생성

GSM SV 콘솔(`gsmsv.site`)에 로그인한 뒤 `/deploy` 페이지에서 VM을 생성합니다.

| 단계 | 선택 |
|---|---|
| OS | Ubuntu 22.04 LTS |
| 노드 | 사용률이 낮은 노드 선택 |
| 티어 | small 이상 권장 (2vCPU / 4GB RAM) |

생성 완료 후 인스턴스 상세 페이지에서 **SSH 포트**와 **초기 비밀번호**를 확인합니다.

---

## 2. SSH 접속

```bash
ssh ubuntu@ssh.gsmsv.site -p <SSH포트>
```

초기 비밀번호 입력 후 즉시 변경합니다.

```bash
passwd
```

---

## 3. 시스템 초기 설정

### 패키지 업데이트

```bash
sudo apt update && sudo apt upgrade -y
```

### 불필요한 패키지 정리

```bash
sudo apt autoremove -y
```

---

## 4. Docker 설치

Ubuntu 공식 권장 방법으로 설치합니다.

### 사전 패키지 설치

```bash
sudo apt install -y ca-certificates curl
```

### Docker 공식 GPG 키 등록

```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

### Docker apt 저장소 추가

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
```

### Docker 설치

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
```

### 설치 확인

```bash
docker --version
docker compose version
```

### sudo 없이 docker 명령어 사용하기

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 5. 코드 배포

### Git 설치 및 코드 클론

```bash
sudo apt install -y git

git clone https://github.com/<계정명>/fastapi-practice.git
cd fastapi-practice
```

> GitHub에 코드를 올리지 않은 경우, 로컬에서 SCP로 전송할 수 있습니다.
> ```bash
> # 로컬 터미널에서 실행
> scp -P <SSH포트> -r ./fastapi-practice ubuntu@ssh.gsmsv.site:~/
> ```

---

## 6. 서버 실행

```bash
docker compose up -d --build
```

- `-d`: 백그라운드 실행
- `--build`: 이미지 새로 빌드

### 실행 확인

```bash
docker compose ps
```

```
NAME            STATUS
fastapi-practice-api-1   Up
```

### 로그 확인

```bash
docker compose logs -f
```

---

## 7. 접속 테스트

인스턴스 상세 페이지에서 **HTTP 포트 번호**를 확인합니다.

```bash
# VM 내부에서 확인
curl http://localhost/posts/

# 외부에서 접속 (브라우저 또는 터미널)
curl http://ssh.gsmsv.site:<HTTP포트>/posts/

# Swagger UI
http://ssh.gsmsv.site:<HTTP포트>/docs
```

---

## 8. 자주 쓰는 명령어

| 작업 | 명령어 |
|---|---|
| 서버 시작 | `docker compose up -d` |
| 서버 중지 | `docker compose down` |
| 코드 업데이트 후 재배포 | `docker compose up -d --build` |
| 실시간 로그 보기 | `docker compose logs -f` |
| 컨테이너 상태 확인 | `docker compose ps` |

---

## 9. 코드 업데이트 시 재배포

```bash
git pull
docker compose up -d --build
```

---

## 포트 구조 요약

```
외부 접속
  └─ GSM SV HTTP 포트 (예: 30080)
       └─ VM 80번 포트
            └─ Docker 컨테이너 8000번 포트 (FastAPI)
```
