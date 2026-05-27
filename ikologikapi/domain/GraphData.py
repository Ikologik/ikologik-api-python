class GraphData:
    def __init__(self, date, value):
        self.date = date
        self.value = value

    def __repr__(self):
        return f"GraphData(date={self.date}, value={self.value})"