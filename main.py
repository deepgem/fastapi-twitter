from fastapi import FastAPI, Depends, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import urllib.parse
import models
from models import Twitter, get_db, check_and_update_tables
from datetime import datetime

# Initialize a FastAPI application instance
app = FastAPI()

# Set up Jinja2 templates, specifying the template directory
templates = Jinja2Templates(directory="templates")


# Route for the home page, returns HTML response
@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    # Check and update database tables
    check_and_update_tables()
    # Query all twitters and sort them by creation time in descending order
    twitters = db.query(Twitter).order_by(Twitter.created_at.desc()).all()
    # Process twitter data
    twitters = [
        {
            "id": twitter.id,
            "content": twitter.content,
            "created_at": twitter.created_at,
        }
        for twitter in twitters
    ]
    # Render the index page with the processed twitter data
    return templates.TemplateResponse(
        "index.html", {"request": request, "twitters": twitters}
    )


# Route for creating a new twitter, handles POST requests
@app.post("/new")
def new_twitter(
    request: Request,
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    # Create a new twitter object
    new_twitter = Twitter(content=content)
    # Add the new twitter to the database session
    db.add(new_twitter)
    # Commit the changes to the database
    db.commit()
    # Refresh the new twitter object to get the latest data from the database
    db.refresh(new_twitter)
    # Redirect to the home page
    return RedirectResponse(url="/", status_code=303)
