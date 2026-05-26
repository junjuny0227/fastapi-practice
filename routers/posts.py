from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import Post
from schemas import PostCreate, PostUpdate, PostResponse

# APIRouter: URL 경로를 그룹으로 묶는 객체입니다.
# prefix="/posts"로 설정하면 이 파일의 모든 경로 앞에 "/posts"가 자동으로 붙습니다.
# tags=["posts"]는 Swagger 문서(/docs)에서 그룹 이름으로 표시됩니다.
router = APIRouter(prefix="/posts", tags=["posts"])


# 404 처리를 매번 반복하지 않도록 공통 함수로 분리했습니다.
def get_post_or_404(post_id: int, db: Session) -> Post:
    post = db.get(Post, post_id)  # PK로 단건 조회
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
    return post


# --- 게시글 작성 ---
# @router.post("/"): POST /posts/ 요청을 처리합니다.
# response_model=PostResponse: 반환값을 PostResponse 형식으로 직렬화합니다.
# status_code=201: 성공 시 200 대신 201 Created를 반환합니다.
# db: Session = Depends(get_db): 요청마다 get_db()가 자동으로 실행되어 DB 세션을 주입해줍니다.
@router.post("/", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.model_dump())  # PostCreate 딕셔너리를 Post 모델로 변환
    db.add(db_post)    # INSERT 준비
    db.commit()        # 실제 DB에 저장
    db.refresh(db_post)  # DB에서 최신 데이터(id, created_at 등) 다시 불러오기
    return db_post


# --- 게시글 목록 조회 ---
# GET /posts/ 요청을 처리합니다. 최신 글부터 내려줍니다.
@router.get("/", response_model=list[PostResponse])
def list_posts(db: Session = Depends(get_db)):
    stmt = select(Post).order_by(Post.created_at.desc())  # SELECT * FROM posts ORDER BY created_at DESC
    return db.execute(stmt).scalars().all()


# --- 게시글 단건 조회 ---
# GET /posts/1 처럼 특정 ID의 게시글 하나를 조회합니다.
# {post_id}는 URL 경로 파라미터로, 함수 인자와 자동으로 연결됩니다.
@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_or_404(post_id, db)


# --- 게시글 수정 ---
# PUT /posts/1 요청을 처리합니다. 제목 또는 내용을 수정합니다.
# 작성자는 수정 불가 — PostUpdate 스키마에 author가 없기 때문입니다.
@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    post = get_post_or_404(post_id, db)

    # exclude_unset=True: 클라이언트가 보낸 필드만 적용합니다.
    # 예) {"title": "새 제목"} 만 보내면 content는 건드리지 않습니다.
    for key, value in post_update.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    post.updated_at = datetime.now(timezone.utc)  # 수정 시각 명시적 갱신
    db.commit()
    db.refresh(post)
    return post


# --- 게시글 삭제 ---
# DELETE /posts/1 요청을 처리합니다.
# status_code=204: 성공 시 응답 본문 없이 204 No Content를 반환합니다.
@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post_or_404(post_id, db)
    db.delete(post)
    db.commit()
