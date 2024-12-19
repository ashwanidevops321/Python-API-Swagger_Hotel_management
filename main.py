from fastapi import FastAPI
from routes import (
    rooms,
    bookings,
    auth,
    location,
    contact,
    faq,
    testimonials
)
app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
app.include_router(location.router, prefix="/location", tags=["Location"])
app.include_router(contact.router, prefix="/contact", tags=["Contact"])
#app.include_router(services.router, prefix="/services", tags=["Services"])
app.include_router(faq.router, prefix="/faq", tags=["FAQ"])
app.include_router(testimonials.router, prefix="/testimonials", tags=["Testimonials"])
