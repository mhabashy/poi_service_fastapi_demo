import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from .. import models, schemas
from ..database import get_db
from ..auth import verify_api_key, decode_jwt_token

router = APIRouter(prefix="/moderation", tags=["moderation"])

@router.get("/pois", response_model=List[schemas.POI])
def get_pois_for_moderation(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    api_key: models.APIKey = Depends(verify_api_key)
):
    """
    Get a list of all POIs for moderation.
    This includes approved, rejected, and pending POIs.
    Requires API key authentication.
    """
    pois = db.query(models.POI) \
        .offset(skip) \
        .limit(limit) \
        .all()
    
    return pois

@router.get("/pois/pending", response_model=List[schemas.POI])
def get_pending_pois(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    api_key: models.APIKey = Depends(verify_api_key)
):
    """
    Get a list of all pending POIs for moderation.
    This includes only POIs that have not been approved or rejected yet.
    Requires API key authentication.
    """
    pois = db.query(models.POI) \
        .filter(models.POI.is_approved == False, models.POI.is_rejected == False) \
        .offset(skip) \
        .limit(limit) \
        .all()
    
    return pois

@router.post("/pois/{poi_id}/approve", response_model=schemas.POI)
def approve_poi(
    poi_id: int, 
    approve_data: schemas.POIApprove,
    db: Session = Depends(get_db),
    api_key: models.APIKey = Depends(verify_api_key)
):
    """
    Approve a POI.
    Requires API key authentication and a valid JWT token.
    """
    # Decode the JWT token
    payload = decode_jwt_token(approve_data.token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    poi = db.query(models.POI).filter(models.POI.id == poi_id).first()
    if poi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="POI not found"
        )
    
    poi.is_approved = True
    poi.is_rejected = False
    poi.rejection_reason = None
    poi.moderation_date = datetime.utcnow()
    
    db.commit()
    db.refresh(poi)
    
    return poi

@router.post("/pois/{poi_id}/reject", response_model=schemas.POI)
def reject_poi(
    poi_id: int, 
    reject_data: schemas.POIReject,
    db: Session = Depends(get_db),
    api_key: models.APIKey = Depends(verify_api_key)
):
    """
    Reject a POI with a reason.
    Requires API key authentication and a valid JWT token.
    """
    
    payload = decode_jwt_token(reject_data.token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    poi = db.query(models.POI).filter(models.POI.id == poi_id).first()
    if poi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="POI not found"
        )
    
    poi.is_approved = False
    poi.is_rejected = True
    poi.rejection_reason = reject_data.reason
    poi.moderation_date = datetime.utcnow()
    
    db.commit()
    db.refresh(poi)
    
    return poi

@router.post("/api-keys", response_model=schemas.APIKey) # different user with different key
def create_api_key(
    api_key_data: schemas.APIKeyCreate,
    db: Session = Depends(get_db),
    api_key: models.APIKey = Depends(verify_api_key)
):
    """
    Create a new API key.
    Requires existing API key authentication.
    """
    from ..auth import generate_api_key
    
    new_key = generate_api_key()
    db_api_key = models.APIKey(
        key=new_key,
        name=api_key_data.name,
        is_active=True
    )
    
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    
    return db_api_key

@router.post("/api-token", response_model=object) # generate token with api key
def create_api_token(
    api_key: models.APIKey = Depends(verify_api_key)
):
    """
    Create a new API token.
    Requires existing API key authentication.
    """
    from ..auth import create_jwt_token
    new_token = create_jwt_token({'key': api_key.key}) # can be any data you want to encode in the token
    
    return {
        "token": new_token,
    }