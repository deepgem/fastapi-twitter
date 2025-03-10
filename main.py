from fastapi import FastAPI, Depends, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import urllib.parse
import models
from models import Twitter, get_db, check_and_update_tables
from datetime import datetime

# Initialize a FastAPI application
app = FastAPI()

# Set up Jinja2 templates with the specified directory
templates = Jinja2Templates(directory="templates")


# Home page route, returns an HTML response
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # Get a database session
    db = get_db()
    if not db:
        # Return a template page for missing PostgreSQL connection
        return templates.TemplateResponse("missing-pg.html", {"request": request})
    # Check and update database tables
    check_and_update_tables()
    # Query all Twitter records and sort by creation time in descending order
    twitters = db.query(Twitter).order_by(Twitter.created_at.desc()).all()
    # Process Twitter data
    twitters = [
        {"id": twitter.id, "content": twitter.content, "created_at": twitter.created_at}
        for twitter in twitters
    ]
    # Render the index page with processed Twitter data
    return templates.TemplateResponse(
        "index.html", {"request": request, "twitters": twitters}
    )


# Route to create a new Twitter record, handles POST requests
@app.post("/new")
def new_twitter(request: Request, content: str = Form(...)):
    # Get a database session
    db = get_db()
    if not db:
        # Redirect to the home page if database connection fails
        return RedirectResponse(url="/", status_code=303)
    # Create a new Twitter object
    new_twitter = Twitter(content=content)
    # Add the new Twitter object to the database session
    db.add(new_twitter)
    # Commit changes to the database
    db.commit()
    # Refresh the new Twitter object to get updated data from the database
    db.refresh(new_twitter)
    # Redirect to the home page
    return RedirectResponse(url="/", status_code=303)
