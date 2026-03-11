# Interactive UI using Fast API
import os, sys
import pandas as pd
import pymongo
import certifi

ca = certifi.where()
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")

from networksecurity.logger.logger import logging
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.constant import training_config
from networksecurity.pipelines.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_pickle_object
from networksecurity.utils.ml_utils.network_model import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database = client[training_config.DATA_INGESTION_DATABASE_NAME]
collection = client[training_config.DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.get("/predict")
async def predict_route(request:Request, file:UploadFile=File(...)):
    df = pd.read_csv(file.file)
    preprocessor = load_pickle_object("final_model/preprocessor.pkl")
    model = load_pickle_object("final_model/model.pkl")
    network_model = NetworkModel(preprocessor=preprocessor, model=model)
    
    y_pred = network_model.predict(df)

if __name__ == "__main__":
    app.run(app, host = "localhost", port=5000)