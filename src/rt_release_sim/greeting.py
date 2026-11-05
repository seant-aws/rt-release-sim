def greeting(name: str) -> str:
    """A greeting for name; an empty or blank name greets the world."""
    return f"Hello, {name.strip() or 'world'}!"
