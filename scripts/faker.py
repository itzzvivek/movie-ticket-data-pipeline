from faker import Faker
import csv
import random
from datetime import datetime, timedelta

fake = Faker()

NUM_USERS = 1000
NUM_MOVIES = 500
NUM_THEATERS = 200
SHOWS_PER_THEATER = 100
NUM_BOOKINGS = 10000


def random_datetime(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))


#Users
with open('users.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["user_id", "name", "email", "age", "city"])
    for i in range(1, NUM_USERS + 1):
        writer.writerow([f"U{i:05d}", fake.name(), fake.email(), random.randint(18, 60), fake.city()])

#Movies
genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance"]
languages = ["English", "Malayalam", "Kannada", "Tamil", "Telugu", "Hindi"]

with open('movies.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["movie_id", "title", "genre", "language", "duration", "release_date"])
    for i in range(1, NUM_MOVIES + 1):
        writer.writerow([f"M{i:04d}", 
                        fake.sentence(nb_words=2).replace(",", ""), 
                        random.choice(genres), 
                        random.choice(languages), 
                        random.randint(90, 180), 
                        fake.date_between(start_date='-5y', end_date='today')])
        
# Theaters
cities = [fake.city() for _ in range(50)]
with open('theaters.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["theater_id", "name", "city", "total_seats"])
    for i in range(1, NUM_THEATERS + 1):
        writer.writerow([f"T{i:04d}", 
                        fake.company(), 
                        random.choice(cities), 
                        random.randint(100, 300)])
        
        
# --- SHOWS ---
show_times = ["10:00", "13:00", "16:00", "19:00", "22:00"]
show_list = []
with open("shows.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["show_id", "theater_id", "movie_id", "screen_no", "show_time"])
    show_id = 1
    for t in range(1, NUM_THEATERS + 1):
        for _ in range(SHOWS_PER_THEATER):
            writer.writerow([
                f"S{show_id:06d}",
                f"T{t:04d}",
                f"M{random.randint(1, NUM_MOVIES):04d}",
                random.randint(1, 5),
                f"2025-06-{random.randint(20,30)}T{random.choice(show_times)}:00"
            ])
            show_list.append(f"S{show_id:06d}")
            show_id += 1

# --- BOOKINGS ---
with open("bookings.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["booking_id", "user_id", "show_id", "seats_booked", "booking_time"])
    for i in range(1, NUM_BOOKINGS + 1):
        writer.writerow([
            f"B{i:06d}",
            f"U{random.randint(1, NUM_USERS):05d}",
            random.choice(show_list),
            random.randint(1, 6),
            random_datetime(datetime(2025, 6, 10), datetime(2025, 6, 20)).isoformat()
        ])

        # --- PAYMENTS ---
statuses = ["confirmed", "failed", "pending"]
with open("payments.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["payment_id", "booking_id", "amount", "status", "payment_time"])
    for i in range(1, NUM_BOOKINGS + 1):
        seats = random.randint(1, 6)
        price = seats * random.choice([120, 180, 250])
        writer.writerow([
            f"P{i:06d}",
            f"B{i:06d}",
            price,
            random.choice(statuses),
            random_datetime(datetime(2025, 6, 10), datetime(2025, 6, 20)).isoformat()
        ])