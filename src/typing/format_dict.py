class FormatDict(dict):
    """A subclass of a dictionary which will not replace any key not present
    when format_map is used, preventing exceptions."""

    def __missing__(self, key: str) -> str:
        string = "{" + key + "}"
        return string