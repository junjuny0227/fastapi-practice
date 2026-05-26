FROM python:3.12-slim

# uv 바이너리를 공식 이미지에서 복사합니다.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# 의존성 파일을 먼저 복사해 레이어 캐시를 활용합니다.
# 소스 코드가 바뀌어도 의존성이 동일하면 이 레이어는 재빌드하지 않습니다.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 소스 코드 복사
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
