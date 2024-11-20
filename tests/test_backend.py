import pytest
from ..flaskApp import admin, single_elim_room, users, matches, reset, empty_check, assign_admin, find_user, find_room, find_room_admin, pair_up, report, advance_round, find_players_in_room, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def setup_database():
    """Fixture to set up a temporary test database."""
    # Create an in-memory SQLite database for isolated testing
    engine =  create_engine('sqlite:///example.db')
    Session = sessionmaker(bind=engine)
    test_session = Session()
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    Base.metadata.drop_all(engine)  # Reset the database
    Base.metadata.create_all(engine)  # Create all tables

    # Inject test data
    room1 = single_elim_room(room_number=1, empty=False, start=False, time="2024-11-16", round=0)
    room2 = single_elim_room(room_number=2, empty=False, start=False, time="2024-11-15", round=0)
    user1 = users(username="user1", in_room=1, ready=True, dropped=False)
    user2 = users(username="user2", in_room=1, ready=True, dropped=False)
    test_session.add_all([room1, room2, user1, user2])
    test_session.commit()

    yield test_session  # Provide the session to the tests

    # Clean up after tests
    test_session.close()

def test_find_players_in_room(setup_database):
    """Test finding all players in a room."""
    players = find_players_in_room(1)
    assert len(players) == 2
    assert players[0].username == "user1"
    assert players[1].username == "user2"


def test_empty_check(setup_database):
    """Test the empty_check function."""
    room = find_room(1)
    assert room.empty is False  # Room initially not empty
    reset(find_user("user1"))
    reset(find_user("user2"))
    empty_check(room)
    assert room.empty is True  # Room becomes empty after users leave


def test_assign_admin(setup_database):
    """Test assigning an admin to a room."""
    assign_admin("admin1", 1, "password123")
    admin_user = find_room_admin(1)
    assert admin_user.admin == "admin1"
    assert admin_user.password == "password123"


def test_find_user(setup_database):
    """Test finding a user."""
    user = find_user("user1")
    assert user is not None
    assert user.username == "user1"


def test_find_room(setup_database):
    """Test finding a room."""
    room = find_room(1)
    assert room is not None
    assert room.room_number == 1


def test_find_room_admin(setup_database):
    """Test finding the admin of a room."""
    assign_admin("admin2", 2)
    admin_user = find_room_admin(1)
    assert admin_user is not None
    assert admin_user.admin == "admin1"





def test_reset_user(setup_database):
    """Test the reset function."""
    user = find_user("user1")
    reset(user)
    assert user.ready is False
    assert user.dropped is False
    assert user.in_room == 0

