#python3 -m venv .venv
#source .venv/bin/activate
#pip3 install -r requirements.txt
source .venv/bin/activate && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload