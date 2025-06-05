from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import engine, get_db
from .models import Base, User
from .routers import auth, rooms, bookings, admin, classes, students
from .auth import get_password_hash
from .config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create admin user if it doesn't exist
    db = next(get_db())
    try:
        admin_user = db.query(User).filter(
            User.email == settings.admin_email
        ).first()
        if not admin_user:
            admin_user = User(
                email=settings.admin_email,
                hashed_password=get_password_hash(settings.admin_password),
                full_name="System Administrator",
                is_admin=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print(f"Admin user created: {settings.admin_email}")
        
        # Create sample rooms if none exist
        from .models import Room
        if db.query(Room).count() == 0:
            sample_rooms = [
                Room(
                    name="Practice Room 1",
                    description="Standard practice room with acoustic drum kit",
                    capacity=2,
                    equipment="Acoustic drum kit, sticks, practice pad"
                ),
                Room(
                    name="Practice Room 2", 
                    description="Electronic drum practice room",
                    capacity=1,
                    equipment="Electronic drum kit, headphones, amplifier"
                ),
                Room(
                    name="Recording Studio",
                    description="Professional recording studio with full drum kit",
                    capacity=4,
                    equipment="Professional drum kit, microphones, recording equipment"
                )
            ]
            for room in sample_rooms:
                db.add(room)
            db.commit()
            print("Sample rooms created")
            
    finally:
        db.close()
    
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Agendamento de aulas API",
    description="API para agendamento de salas de prática de bateria",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(admin.router)
app.include_router(classes.router)
app.include_router(students.router, prefix="/students", tags=["students"])

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo ao Agendamento de aulas API",
        "docs": "/docs",
        "admin_email": settings.admin_email
    }


@app.get("/health")
def health_check():
    return {"status": "saudável"}
