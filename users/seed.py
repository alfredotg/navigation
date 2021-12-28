from app.env import load_dotenv

load_dotenv()

from app.database import SessionLocal 
from app import crud, pwd

def seed():
    with SessionLocal() as session:
        for email in ['alice@gmail.com', 'bob@gmail.com', 'carol@gmail.com']:
            if crud.get_user_by_email(session, email) is not None:
                continue
            crud.create_user(session, name=email, email=email, password_hash=pwd.password_hash("test"))

if "__main__" == __name__:
    seed()
