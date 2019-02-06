def status_colour(status='On Track'):
    """Function to return a colour based on status"""
    if status == 'On Track':
        c = "#00CC96"
    elif status == 'At Risk':
        c = "#FDB507"
    elif status == 'Off Track':
        c = "#FD3A07"
    return c