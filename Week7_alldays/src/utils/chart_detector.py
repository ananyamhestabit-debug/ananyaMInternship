def detect_chart_type(filename, caption):
    text = (filename + " " + caption).lower()

    if "pie" in text:
        return "pie chart"
    elif "bar" in text:
        return "bar chart"
    elif "graph" in text or "plot" in text:
        return "graph"
    else:
        return "chart"