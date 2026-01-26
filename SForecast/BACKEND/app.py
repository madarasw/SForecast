from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from news_fetcher.pipeline import run_pipeline
import logging
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing)
    allow_methods=["*"],
    allow_headers=["*"]
)


class CheckRequest(BaseModel):
    dataset: str
    start_date: str
    end_date: str
    query: str
    macro_var: str


@app.post("/check")
def check_data(data: CheckRequest):
    file_path = BASE_DIR / "out.txt"
    content = (
        f"Dataset: {data.dataset}\n"
        f"Start Date: {data.start_date}\n"
        f"End Date: {data.end_date}\n"
        f"Macro_var: {data.macro_var}\n"
        f"Query: {data.query}\n"
    )

    with open(file_path, "w") as f:
        f.write(content)

    run_pipeline(data.dataset, data.start_date, data.end_date, data.macro_var, data.query)
    return {"message": f"out.txt created at {file_path}"}
