# booking_api
A Django RESTful API that allows users to set their weekly availability and allows guests to book non-overlapping time slots (15m, 30m, 45m, or 1 hour) based on that availability.

Features
Users can set weekly availability (e.g., every Monday from 9am–5pm)

Guest users can book available time slots

Bookings are validated:

Must not overlap with other bookings

Must fit within defined availability

Must be exact duration: 15, 30, 45, or 60 minutes

Well-structured API responses with status codes

Authentication is not enforced (for demo)

Tech Stack
Python 3.x

Django 4.x

Django REST Framework

SQLite (default DB)

