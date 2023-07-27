from db.database import sqlmodel_db_session
from models.person import Person
import uuid
from sqlmodel import select, Session

# from sqlalchemy.exc import IntegrityError

first_names = [
    "Emma",
    "Liam",
    "Olivia",
    "Noah",
    "Ava",
    "Isabella",
    "Sophia",
    "Mia",
    "Charlotte",
    "Amelia",
    "Harper",
    "Evelyn",
    "Layla",
    "Henry",
    "Sebastian",
    "William",
    "James",
    "Benjamin",
    "Lucas",
    "Alexander",
]
last_names = [
    "Smith",
    "Johnson",
    "Williams",
    "Jones",
    "Brown",
    "Davis",
    "Miller",
    "Wilson",
    "Moore",
    "Taylor",
    "Anderson",
    "Thomas",
    "Jackson",
    "White",
    "Harris",
    "Martin",
    "Thompson",
    "Garcia",
    "Martinez",
    "Robinson",
]
email_list = [f"person{uuid.uuid4().hex[:8]}@example.com" for _ in
              range(20)]
# import datetime

# date_of_birth_list = []
# start_date = datetime.date(1950, 1, 1)
# end_date = datetime.date(2000, 12, 31)
# delta = end_date - start_date
#
# for _ in range(20):
#     random_days = datetime.timedelta(days=random.randint(0, delta.days))
#     date_of_birth = start_date + random_days
#     date_of_birth_list.append(datetime.datetime.strptime(date_of_birth.strftime("%Y-%m-%d"),"%Y-%m-%d"))


# print(date_of_birth_list, type(date_of_birth_list[0]))

countries = [
    "United States",
    "Canada",
    "United Kingdom",
    "Germany",
    "France",
    "Spain",
    "Italy",
    "Australia",
    "China",
    "Japan",
    "Brazil",
    "Mexico",
    "India",
    "South Africa",
    "Russia",
    "Sweden",
    "Norway",
    "Netherlands",
    "Argentina",
    "New Zealand",
]


# gender = ("Male","Female","Trans")
# gender_list = []
# for _ in range(20):
#     g = random.choice(gender)
#     gender_list.append(g)
#
# uuid_list = []
# for _ in range(20):
#
#     uuid_list.append(uuid.uuid4())
#


# main_list =
# [uuid_list, gender_list, countries, date_of_birth_list,
# email_list, first_names, last_names]


def add_person(session,
        first_name, last_name, gender, email, date_of_birth,
        country_of_birth, car_id
) -> dict:
    id_ = uuid.uuid4()
    print("gender------->", gender.value)

    # with sqlmodel_db_session() as session:
    person = Person(
        first_name=first_name,
        last_name=last_name,
        gender=gender.value,
        email=email,
        date_of_birth=date_of_birth,
        country_of_birth=country_of_birth,
        car_id=car_id,
        id=id_,
    )
    session.add(person)
    return {"id": str(id_)}


def get_persons(session: Session):

    stmt = select(Person)
    res = session.exec(stmt)
    persons = res.all()
    print("persons----->", persons)
    if not persons:
        return []

    return [
        {
            "name": f'{r.first_name + "  " + r.last_name}',
            "id": str(r.id),
            "email": r.email,
        }
        for r in persons
    ]


