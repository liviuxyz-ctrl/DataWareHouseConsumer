# src/api/assets.py
from fastapi import APIRouter, HTTPException
from src.db.models import Asset, AssetModel
from typing import List

router = APIRouter()

#Works
@router.get("/assets", response_model=List[str])
def get_assets(offset: int = 0, limit: int = 20):
    assets = Asset.objects.all()[offset:offset+limit]
    return [asset.name for asset in assets]

@router.get("/assets/{asset_id}", response_model=AssetModel)
def get_asset(asset_id: str):
    asset = Asset.objects.filter(name=asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset
