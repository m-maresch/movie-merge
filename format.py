def format_time(seconds):
    """
    Converts seconds into a human-readable MM:SS format.
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"
