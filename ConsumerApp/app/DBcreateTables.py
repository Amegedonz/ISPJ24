#SQLalchemy requirements to build models
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Float, DateTime, LargeBinary, func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
 

#DB connection
from database import engine, Base, dbSession

#Login lib requirements
from flask_login import UserMixin

#secret generation
import pyotp

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(String(9), primary_key=True, unique=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    phoneNumber = Column(Integer(), unique=True)
    role = Column(String(50), nullable=False, default="Patient")

    twofa = relationship("Twofa", back_populates="user", uselist=False, cascade="all, delete-orphan")
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
    doctors = relationship("PatientAssignment", back_populates="patient")

    def __repr__(self):
        return f"<User(id = {self.id}, username = {self.username})>"

    def add_doctor(self, license_number, specialisation, facility):
        doctor = Doctor(
            id=self.id,
            license_number=license_number,
            specialisation=specialisation,
            facility=facility
        )
        self.doctor_profile = doctor
        self.role = "Doctor"
        return doctor
    
class Twofa(Base):
    __tablename__ = 'twofa'

    id = Column(String(9), ForeignKey('users.id'), primary_key=True, unique=True)
    user_secret = Column(String(32), unique=True, nullable=False, default=lambda: pyotp.random_base32())
    twofa_enabled = Column(Boolean(), default=False)

    user = relationship("User", back_populates='twofa')

class Doctor(Base):
    __tablename__ = 'doctors'

    license_number = Column(String(7), primary_key=True, unique=True)
    id = Column(String(9), ForeignKey('users.id'), nullable=False)
    specialisation = Column(String(50), nullable=False)
    facility = Column(String(50))

    user = relationship("User", back_populates="doctor_profile")
    patients = relationship("PatientAssignment", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor(license_number={self.license_number}, specialisation={self.specialisation})>"

class PatientAssignment(Base):
    __tablename__ = 'doctor_patient_assignment'

    doctor_id = Column(String(7), ForeignKey('doctors.license_number'), primary_key=True)
    patient_id = Column(String(9), ForeignKey('users.id'), primary_key=True)
    doctor = relationship("Doctor", back_populates="patients")
    patient = relationship("User", back_populates="doctors")

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)  
    name = Column(String(255), nullable=False)
    license_no = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)
    facility = Column(String(255), nullable=False)
    patient_nric = Column(String(50), nullable=False)
    type = Column(String(100), nullable=False)

def create_tables():
    try:
        Base.metadata.create_all(engine)
        dbSession.commit()
        print("Tables created successfully!")
    except SQLAlchemyError as e:
        print(f"Database connection failed: {e}")
        dbSession.rollback()
    finally:
        dbSession.close()

def delete_tables():
    Base.metadata.drop_all(engine)
    dbSession.commit()
    dbSession.close()

def clear_table_data():
    dbSession.query(User).delete()
    print("Contents deleted!")
    dbSession.commit()
    dbSession.close()


Base.metadata.create_all(engine)

def main():
    ...
    
main()
