# task-notification-system
o Notifications must be delivered in real time to connected users when tasks are updated, assigned, or completed.

# Navigate to the project directory
cd /Users/elishabere/Desktop/task-notification-system

# Create and activate virtual environment (if not already done)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to the backend directory
cd backend

# Run the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000