from rt_release_sim import greeting


def test_greeting_names_the_person() -> None:
    assert greeting("Ada") == "Hello, Ada!"


def test_greeting_without_a_name_greets_the_world() -> None:
    assert greeting("") == "Hello, world!"


def test_greeting_with_a_blank_name_greets_the_world() -> None:
    assert greeting("   ") == "Hello, world!"
