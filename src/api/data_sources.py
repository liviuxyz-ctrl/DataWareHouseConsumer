# src/api/data_sources.py
from fastapi import APIRouter, HTTPException
from src.db.models import DataSource, DataSourceModel
from typing import List

router = APIRouter()

@router.get("/data-sources", response_model=List[str])
def get_data_sources(offset: int = 0, limit: int = 20):
    data_sources = DataSource.objects.all()[offset:offset+limit]
    return [data_source.source_name for data_source in data_sources]

@router.get("/data-sources/{data_source_id}", response_model=DataSourceModel)
def get_data_source(data_source_id: str):
    data_source = DataSource.objects.filter(source_name=data_source_id).first()
    if not data_source:
        raise HTTPException(status_code=404, detail="Data source not found")
    return data_source
