async def allowed_file(filename: str):
    """Checks if the filename has an allowed extension."""
    allowed_extensions = {"pdf", "txt"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
