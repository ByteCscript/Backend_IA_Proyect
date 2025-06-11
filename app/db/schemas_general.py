from sqlalchemy import Table, Column, Integer, String, Date, Float, ForeignKey, Text, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Tabla intermedia para asignación de roles a usuarios
enable_user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

# Tabla de logs de tareas realizadas por usuario
user_task_logs_table = Table(
    "user_task_logs",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
    Column("date", Date, nullable=False),
    Column("quantity", Numeric(12,2), nullable=False, default=1),
)
# Tabla intermedia rol → tarea
role_tasks_table = Table(
    "role_tasks",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # Relación inversa a usuarios
    users = relationship("User", secondary=enable_user_roles, back_populates="roles")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)

    # relaciones existentes…
    productivity = relationship("Productivity", back_populates="user")
    sales        = relationship("Sale",        back_populates="user")
    roles        = relationship("Role",        secondary=enable_user_roles, back_populates="users")

    # ← aquí agregamos reports
    reports = relationship("Report", back_populates="user")
class Productivity(Base):
    __tablename__ = "productivity"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)

    user = relationship("User", back_populates="productivity")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)

    user = relationship("User", back_populates="sales")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    type = Column(String(50), nullable=False)

    # relación inversa a User
    user = relationship("User", back_populates="reports")