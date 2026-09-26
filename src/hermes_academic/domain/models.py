"""Modelos de dominio tipados (Pydantic).

Contrato compartilhado entre AcademicProvider, MCP server e agente. Sem
logica de negocio alem de validacao de campo.
"""

from datetime import date, datetime

from pydantic import BaseModel


class AcademicClass(BaseModel):
    """Uma materia/turma cursada pelo aluno."""

    id: str
    name: str
    teacher: str
    semester: int


class Assignment(BaseModel):
    """Uma tarefa/trabalho academico com prazo de entrega."""

    id: str
    class_id: str
    subject: str
    title: str
    description: str | None = None
    due_date: date
    status: str


class Announcement(BaseModel):
    """Um aviso publicado por um professor em uma materia."""

    id: str
    class_id: str
    subject: str
    author: str
    created_at: datetime
    content: str


class CalendarEvent(BaseModel):
    """Um evento do calendario academico (prova, aula, entrega, etc.)."""

    id: str
    subject: str
    title: str
    description: str | None = None
    start: datetime
    end: datetime
    location: str | None = None


class Student(BaseModel):
    """O aluno para quem o agente presta assistencia."""

    id: str
    name: str
    course: str
    semester: int
