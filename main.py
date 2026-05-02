from fastapi import FastAPI
from stock_code_route import program
app = FastAPI()

@app.get("/")
def read_root():
    return program()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)