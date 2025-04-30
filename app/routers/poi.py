from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
import base64
import re

router = APIRouter(prefix="/pois", tags=["pois"])

@router.post("/", response_model=schemas.POI, status_code=status.HTTP_201_CREATED)
async def create_poi(
    poi_data: schemas.POICreateWithImage,
    db: Session = Depends(get_db)
):
    """
    Create a new POI with optional image.
    POIs are created in an unapproved state and must be approved by a moderator.
    
    The image should be provided as a base64 encoded string.
    """
    images = poi_data.images
    poi_dict = poi_data.dict(exclude={"images"})
    
    db_poi = models.POI(**poi_dict)
    
    db.add(db_poi)
    db.flush()
    print("here")
    print(images)
    if images:
        try:
            isFirst = True
            for image in images:
                print(image);
                # if not re.match(r'^data:image\/[a-zA-Z]+;base64,', poi_data.images):
                #     try:
                #         base64.b64decode(poi_data.images)
                #     except Exception:
                #         raise ValueError("Invalid base64 string format")
                # if
                poi_image = models.POIImage(
                    poi_id=db_poi.id,
                    image_data=image,
                    is_primary=isFirst
                )
                isFirst = False
                db.add(poi_image)
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error processing image: {str(e)}"
            )
    
    db.commit()
    db.refresh(db_poi)
    
    return db_poi

@router.get("/", response_model=List[schemas.POI])
def get_approved_pois(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Get a list of all approved POIs.
    """
    pois = db.query(models.POI) \
        .filter(models.POI.is_approved == True) \
        .offset(skip) \
        .limit(limit) \
        .all()
    
    return pois

@router.get("/{poi_id}", response_model=schemas.POI)
def get_poi(poi_id: int, db: Session = Depends(get_db)):
    """
    Get a specific POI by ID.
    Only approved POIs are accessible.
    """
    poi = db.query(models.POI) \
        .filter(models.POI.id == poi_id, models.POI.is_approved == True) \
        .first()
    
    if poi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="POI not found or not approved"
        )
    
    return poi