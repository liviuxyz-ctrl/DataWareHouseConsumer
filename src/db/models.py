# src/db/models.py

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.connection import setup
from src.config.settings import Config
import uuid
from pydantic import BaseModel
from typing import Optional

class Asset(Model):
    __keyspace__ = 'financial_data'
    asset_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text()
    type = columns.Text()

class DataSource(Model):
    __keyspace__ = 'financial_data'
    source_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    source_name = columns.Text(index=True)

class BaseFinancialData(Model):
    __abstract__ = True
    asset_id = columns.UUID(partition_key=True)
    source_id = columns.UUID(partition_key=True)
    business_date = columns.Date(primary_key=True)
    system_time = columns.DateTime(primary_key=True, clustering_order="DESC")
    symbol = columns.Text(index=True)

def initialize_cassandra_connection():
    setup(Config.CASSANDRA_NODES, "financial_data", protocol_version=4)

# Pydantic models
class AssetModel(BaseModel):
    asset_id: Optional[uuid.UUID]
    name: str
    type: str

    class Config:
        orm_mode = True

class DataSourceModel(BaseModel):
    source_id: Optional[uuid.UUID]
    source_name: str

    class Config:
        orm_mode = True
