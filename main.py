from models import Like, Comment
from typing import List
from datetime import datetime, timedelta
import secrets

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

import models
import schemas
from models import Like
from database import engine, SessionLocal

# -----------------------------
# Database setup
# -----------------------------
models.Base.metadata.create_all(bind=engine)

# -----------------------------
# App
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# JWT config
# -----------------------------
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# -----------------------------
# Security
# -----------------------------
security = HTTPBearer()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# -----------------------------
# DB dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# JWT helpers
# -----------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# -----------------------------
# Root
# -----------------------------
@app.get("/")
def home():
    return {"message": "Web App backend is running 🚀"}

# -----------------------------
# Auth
# -----------------------------
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = pwd_context.hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user or not pwd_context.verify(
        user.password, db_user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": token, "token_type": "bearer"}

# -----------------------------
# Posts
# -----------------------------
@app.post("/posts", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    new_post = models.Post(
        title=post.title,
        content=post.content,
        owner_id=user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Post)
        .order_by(models.Post.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

@app.put("/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted"}

# -----------------------------
# Likes
# -----------------------------
@app.post("/posts/{post_id}/like")
def toggle_like(
    post_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == user.id
    ).first()

    if like:
        db.delete(like)
        db.commit()
        liked = False
    else:
        db.add(Like(user_id=user.id, post_id=post_id))
        db.commit()
        liked = True

    count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"likes": count, "liked": liked}

@app.get("/posts/{post_id}/likes")
def get_likes(post_id: int, db: Session = Depends(get_db)):
    count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"likes": count}

@app.get("/posts/{post_id}/liked")
def is_liked(
    post_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    liked = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == user.id
    ).first() is not None

    return {"liked": liked}
# -----------------------------
# COMMENTS
# -----------------------------

# Add comment (PROTECTED)
@app.post("/posts/{post_id}/comments", response_model=schemas.CommentResponse)
def add_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        content=comment.content,
        user_id=user.id,
        post_id=post_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


# Get comments (PUBLIC)
@app.get("/posts/{post_id}/comments", response_model=List[schemas.CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).all()
