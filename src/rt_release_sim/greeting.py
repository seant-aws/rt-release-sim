def greeting(name: str) -> str:
    """A greeting for name; an empty name greets the world."""
    return f"Hello, {name or 'world'}!"
