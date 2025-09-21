# QuantumLogic Chip Technology v3

Research prototype for the NIW endeavor by Alex Costa Souza. 
This version includes a second quantum algorithm and a small FastAPI service to present the pipeline like a product.

## Quick start

python -m venv .venv
source .venv/bin/activate   # Windows users run .venv\Scripts\activate
pip install -r requirements.txt

pytest -q

# run the FastAPI service
uvicorn qlct.pipeline.fastapi_app:app --reload

# call from a second terminal
curl -X POST http://127.0.0.1:8000/score -H "Content-Type: application/json" -d '{"bits":3,"target":5}'
curl -X POST http://127.0.0.1:8000/protect -H "Content-Type: application/json" -d '{"payload":{"sensor":"qchip","data":[1,0,1]}}'
