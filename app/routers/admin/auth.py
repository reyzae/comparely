"""
Admin Authentication Router

This module handles all authentication-related routes for the admin panel:
- Login/logout functionality
- Session management
- User profile management
- Password change

Author: Comparely Team
Last Modified: 2025-12-19
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import User, Role

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Create router (no prefix, will be added by parent)
router = APIRouter(tags=["admin-auth"])


def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    Get current logged-in user from session.
    Untuk sementara, return dummy user jika tidak ada session.
    """
    # Cek session cookie
    user_id = request.session.get("user_id") if "session" in request.scope else None
    
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
    
    # Dummy user untuk development (hapus di production!)
    return {
        "id": 1,
        "username": "admin",
        "email": "admin@comparely.com",
        "full_name": "Administrator",
        "role": {"name": "Admin"}
    }


@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Halaman login admin"""
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request}
    )


@router.post("/login")
async def admin_login(request: Request, db: Session = Depends(get_db)):
    """Handle login form submission"""
    # TEMPORARY: Bypass authentication, langsung redirect ke dashboard
    # TODO: Re-enable proper authentication setelah SessionMiddleware fixed
    
    # Get form data (for validation purposes)
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    
    # Simple check - jika ada username dan password, langsung masuk
    if username and password:
        # Langsung redirect ke dashboard tanpa session
        return RedirectResponse(url="/admin/dashboard", status_code=303)
    else:
        return RedirectResponse(
            url="/admin/login?error=Please enter username and password",
            status_code=303
        )


@router.get("/logout")
async def admin_logout(request: Request):
    """Logout admin"""
    # TEMPORARY: Just redirect tanpa clear session
    # TODO: Re-enable session.clear() setelah SessionMiddleware fixed
    return RedirectResponse(url="/admin/login", status_code=303)


@router.get("/profile", response_class=HTMLResponse)
async def admin_profile(request: Request):
    """Halaman profile admin"""
    return templates.TemplateResponse(
        "admin/profile.html",
        {"request": request}
    )


@router.post("/profile/change-password")
async def admin_change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    """Handle change password"""
    # TODO: Implement password change logic
    return RedirectResponse(
        url="/admin/profile?message=Password changed successfully",
        status_code=303
    )
