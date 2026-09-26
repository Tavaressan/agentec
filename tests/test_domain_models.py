"""Testes dos modelos de dominio tipados (Pydantic) - Issue #1.

Cada modelo e instanciado com dado valido e testado quanto a rejeicao de
campo obrigatorio ausente, conforme o criterio de aceite da issue.
"""

from datetime import date, datetime

import pytest
from pydantic import ValidationError

from hermes_academic.domain.models import (
    AcademicClass,
    Announcement,
    Assignment,
    CalendarEvent,
    Student,
)


def test_academic_class_valid_data():
    academic_class = AcademicClass(
        id="class-1",
        name="Banco de Dados",
        teacher="Prof. Ana Souza",
        semester=6,
    )

    assert academic_class.id == "class-1"
    assert academic_class.name == "Banco de Dados"
    assert academic_class.teacher == "Prof. Ana Souza"
    assert academic_class.semester == 6


def test_academic_class_missing_required_field_raises():
    with pytest.raises(ValidationError):
        AcademicClass(name="Banco de Dados", teacher="Prof. Ana Souza", semester=6)


def test_assignment_valid_data():
    assignment = Assignment(
        id="assign-1",
        class_id="class-1",
        subject="Banco de Dados",
        title="Projeto de Modelagem",
        description="Modelagem conceitual e logica do banco.",
        due_date=date(2026, 9, 28),
        status="pending",
    )

    assert assignment.id == "assign-1"
    assert assignment.class_id == "class-1"
    assert assignment.subject == "Banco de Dados"
    assert assignment.title == "Projeto de Modelagem"
    assert assignment.due_date == date(2026, 9, 28)
    assert assignment.status == "pending"


def test_assignment_missing_required_field_raises():
    with pytest.raises(ValidationError):
        Assignment(
            class_id="class-1",
            subject="Banco de Dados",
            title="Projeto de Modelagem",
            due_date=date(2026, 9, 28),
            status="pending",
        )


def test_announcement_valid_data():
    announcement = Announcement(
        id="ann-1",
        class_id="class-1",
        subject="Banco de Dados",
        author="Prof. Ana Souza",
        created_at=datetime(2026, 9, 20, 10, 0),
        content="A entrega do projeto foi prorrogada para 30/09.",
    )

    assert announcement.id == "ann-1"
    assert announcement.class_id == "class-1"
    assert announcement.author == "Prof. Ana Souza"
    assert announcement.content == "A entrega do projeto foi prorrogada para 30/09."


def test_announcement_missing_required_field_raises():
    with pytest.raises(ValidationError):
        Announcement(
            class_id="class-1",
            subject="Banco de Dados",
            author="Prof. Ana Souza",
            created_at=datetime(2026, 9, 20, 10, 0),
        )


def test_calendar_event_valid_data():
    event = CalendarEvent(
        id="event-1",
        subject="Banco de Dados",
        title="Prova P2",
        description="Prova sobre normalizacao.",
        start=datetime(2026, 10, 1, 19, 0),
        end=datetime(2026, 10, 1, 21, 0),
        location="Sala 12",
    )

    assert event.id == "event-1"
    assert event.title == "Prova P2"
    assert event.start == datetime(2026, 10, 1, 19, 0)
    assert event.end == datetime(2026, 10, 1, 21, 0)
    assert event.location == "Sala 12"


def test_calendar_event_missing_required_field_raises():
    with pytest.raises(ValidationError):
        CalendarEvent(
            subject="Banco de Dados",
            title="Prova P2",
            start=datetime(2026, 10, 1, 19, 0),
            end=datetime(2026, 10, 1, 21, 0),
        )


def test_student_valid_data():
    student = Student(
        id="student-1",
        name="Vitor Tavares Chaves",
        course="Desenvolvimento de Software Multiplataforma",
        semester=6,
    )

    assert student.id == "student-1"
    assert student.name == "Vitor Tavares Chaves"
    assert student.course == "Desenvolvimento de Software Multiplataforma"
    assert student.semester == 6


def test_student_missing_required_field_raises():
    with pytest.raises(ValidationError):
        Student(course="Desenvolvimento de Software Multiplataforma", semester=6)
