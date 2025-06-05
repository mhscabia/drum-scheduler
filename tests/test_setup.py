import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    print("✓ FastAPI app imported successfully")
    
    from app.database import engine, Base
    print("✓ Database components imported successfully")
    
    # Try to create tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")
    
    print("✓ All components loaded successfully!")
    print("Ready to start the server...")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
