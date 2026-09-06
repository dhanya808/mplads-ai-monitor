from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = None
    role: Optional[str] = None

DEMO_USERS = {
    "mp.varanasi@sansad.nic.in": {
        "email": "mp.varanasi@sansad.nic.in",
        "name": "Hon. Rajeshwar Verma",
        "role": "MP",
        "role_title": "Member of Parliament",
        "designation": "Lok Sabha MP (18th Lok Sabha)",
        "jurisdiction": "Varanasi Parliamentary Constituency (PC-77)",
        "badge_color": "bg-blue-100 text-blue-800",
        "organization": "Parliament of India / Sansad"
    },
    "dm.varanasi@up.gov.in": {
        "email": "dm.varanasi@up.gov.in",
        "name": "Shri Satyendra Kumar, IAS",
        "role": "DM",
        "role_title": "District Magistrate & DPO",
        "designation": "District Magistrate / Collector",
        "jurisdiction": "District Planning Cell, Varanasi",
        "badge_color": "bg-emerald-100 text-emerald-800",
        "organization": "Government of Uttar Pradesh"
    },
    "sna.planning@up.gov.in": {
        "email": "sna.planning@up.gov.in",
        "name": "Dr. Rameshwar Singh",
        "role": "SNA",
        "role_title": "State Nodal Authority (SNA)",
        "designation": "Special Secretary (Planning)",
        "jurisdiction": "Uttar Pradesh (80 Constituencies)",
        "badge_color": "bg-purple-100 text-purple-800",
        "organization": "Planning Department, Govt of UP"
    },
    "diid.director@mospi.gov.in": {
        "email": "diid.director@mospi.gov.in",
        "name": "Smt. Ananya Sen, ISS",
        "role": "MOSPI",
        "role_title": "Director, DIID MoSPI",
        "designation": "Director (Data Informatics & Innovation)",
        "jurisdiction": "National Oversight Tier (All India)",
        "badge_color": "bg-amber-100 text-amber-800",
        "organization": "Ministry of Statistics & Programme Implementation"
    }
}

# In-memory active session (for single user demonstration)
current_session = {
    "user": DEMO_USERS["mp.varanasi@sansad.nic.in"],
    "is_authenticated": True
}

@router.post("/login")
def login(req: LoginRequest):
    email = req.email.strip().lower()
    
    # If role-based quick login
    if req.role:
        role_map = {
            "MP": "mp.varanasi@sansad.nic.in",
            "DM": "dm.varanasi@up.gov.in",
            "SNA": "sna.planning@up.gov.in",
            "MOSPI": "diid.director@mospi.gov.in"
        }
        email = role_map.get(req.role.upper(), email)

    user = DEMO_USERS.get(email)
    if not user:
        # Fallback create a demo session for any official email entered
        user = {
            "email": email,
            "name": email.split("@")[0].replace(".", " ").title(),
            "role": "MP",
            "role_title": "Authorized Stakeholder",
            "designation": "Government Officer",
            "jurisdiction": "Varanasi (PC-77)",
            "badge_color": "bg-blue-100 text-blue-800",
            "organization": "National Programme Portal"
        }

    current_session["user"] = user
    current_session["is_authenticated"] = True

    return {
        "success": True,
        "message": "Authentication successful. Welcome to MPLADS AI Monitor.",
        "user": user,
        "redirect_url": "/dashboard"
    }

@router.get("/me")
def get_current_user():
    return {
        "is_authenticated": current_session["is_authenticated"],
        "user": current_session["user"]
    }

@router.post("/logout")
def logout():
    current_session["is_authenticated"] = False
    return {"success": True, "message": "Logged out successfully", "redirect_url": "/login"}
