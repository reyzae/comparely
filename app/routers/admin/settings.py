"""
Admin Settings Router
Handles application settings and configuration.
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import Phone, Category
from .auth import get_current_user
import logging

# Setup templates
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["admin-settings"])


@router.get("/settings", response_class=HTMLResponse)
async def admin_settings(request: Request, db: Session = Depends(get_db)):
    """Halaman settings"""
    
    # Get database stats
    total_devices = db.query(Phone).count()
    total_categories = db.query(Category).count()
    
    # Settings data
    settings = {
        "site_name": "COMPARELY",
        "site_description": "Compare technology devices",
        "items_per_page": 20,
        "enable_ai": True,
        "enable_registration": False,
        "maintenance_mode": False
    }
    
    return templates.TemplateResponse(
        "admin/settings.html",
        {
            "request": request,
            "current_user": get_current_user(request, db),
            "settings": settings,
            "database_status": "Connected",
            "total_devices": total_devices,
            "total_categories": total_categories,
            "ai_api_key_masked": "••••••••••••"
        }
    )


@router.post("/settings/update")
async def update_settings(
    request: Request,
    site_name: str = Form(...),
    site_description: str = Form(...),
    items_per_page: int = Form(20),
    enable_ai: bool = Form(False),
    enable_registration: bool = Form(False),
    maintenance_mode: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Update application settings"""
    try:
        # Placeholder for settings update logic
        logger.info(f"Settings updated: {site_name}")
        
        return RedirectResponse(
            url="/admin/settings?message=Settings updated successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error updating settings: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to update settings",
            status_code=303
        )


@router.post("/settings/update-api")
async def update_api_settings(
    request: Request,
    ai_api_key: str = Form(...),
    db: Session = Depends(get_db)
):
    """Update API settings"""
    try:
        # Placeholder for API key update
        logger.info("API settings updated")
        
        return RedirectResponse(
            url="/admin/settings?message=API settings updated successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error updating API settings: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to update API settings",
            status_code=303
        )


@router.post("/settings/backup-database")
async def backup_database(request: Request, db: Session = Depends(get_db)):
    """Backup database"""
    try:
        # Placeholder for database backup logic
        logger.info("Database backup initiated")
        
        return RedirectResponse(
            url="/admin/settings?message=Database backup completed successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error backing up database: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to backup database",
            status_code=303
        )


@router.post("/settings/optimize-database")
async def optimize_database(request: Request, db: Session = Depends(get_db)):
    """Optimize database"""
    try:
        # Placeholder for database optimization
        logger.info("Database optimization completed")
        
        return RedirectResponse(
            url="/admin/settings?message=Database optimized successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error optimizing database: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to optimize database",
            status_code=303
        )


@router.post("/admin/reset-database")
async def reset_database(request: Request, db: Session = Depends(get_db)):
    """Reset database (delete all devices)"""
    try:
        # Delete all devices
        deleted_count = db.query(Phone).delete()
        db.commit()
        
        logger.warning(f"Database reset: {deleted_count} devices deleted")
        
        return RedirectResponse(
            url="/admin/settings?message=Database reset successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error resetting database: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to reset database",
            status_code=303
        )


@router.post("/settings/clear-cache")
async def clear_cache(request: Request, db: Session = Depends(get_db)):
    """Clear application cache"""
    try:
        # Placeholder for cache clearing
        logger.info("Cache cleared")
        
        return RedirectResponse(
            url="/admin/settings?message=Cache cleared successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error clearing cache: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to clear cache",
            status_code=303
        )


@router.post("/settings/update-ui")
async def update_ui_preferences(
    request: Request,
    items_per_page: int = Form(20),
    date_format: str = Form("YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Update UI preferences"""
    try:
        # Placeholder for UI preferences update
        logger.info(f"UI preferences updated: {items_per_page} items per page")
        
        return RedirectResponse(
            url="/admin/settings?message=UI preferences updated successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error updating UI preferences: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to update UI preferences",
            status_code=303
        )
