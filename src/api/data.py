from fastapi import APIRouter, HTTPException
from src.db.models import BaseFinancialData, initialize_cassandra_connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from datetime import datetime
from typing import List, Dict
import re

router = APIRouter()

def sanitize_table_name(name: str) -> str:
    sanitized_name = re.sub(r'\W|^(?=\d)', '_', name)
    return sanitized_name

def create_financial_data_model(asset_id: str, data_source_id: str) -> Model:
    sanitized_symbol = sanitize_table_name(asset_id)
    sanitized_source = sanitize_table_name(data_source_id)
    class_name = f"{sanitized_symbol}_{sanitized_source}"

    attrs = {
        '__module__': __name__,
        '__keyspace__': 'financial_data',
        'asset_id': columns.UUID(partition_key=True),
        'source_id': columns.UUID(partition_key=True),
        'business_date': columns.Date(primary_key=True),
        'system_time': columns.DateTime(primary_key=True, clustering_order="DESC"),
        'symbol': columns.Text(index=True),
        'value': columns.Float()
    }
    return type(class_name, (BaseFinancialData,), attrs)

@router.get("/data")
def get_data(asset_id: str, data_source_id: str, start_business_date: str, end_business_date: str, include_attributes: bool = False):
    start_date = datetime.strptime(start_business_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_business_date, "%Y-%m-%d")

    initialize_cassandra_connection()

    # Create the appropriate model
    FinancialDataModel = create_financial_data_model(asset_id, data_source_id)

    query = FinancialDataModel.objects.filter(
        asset_id=asset_id,
        source_id=data_source_id,
        business_date__gte=start_date,
        business_date__lte=end_date
    ).limit(100).order_by("-business_date")

    records = list(query)

    if include_attributes:
        attributes = {attr: [] for attr in records[0].__dict__.keys() if not attr.startswith("_")}
        record_data = []
        for record in records:
            record_dict = {attr: getattr(record, attr) for attr in attributes.keys()}
            record_data.append(record_dict)
        return {"data": record_data, "attributes": list(attributes.keys())}

    return {"data": records}
