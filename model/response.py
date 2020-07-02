class Response:
    text = "",
    danger = "",
    danger_value = "",
    danger_obj = []

    def __init__(self, text, danger, danger_value, danger_obj):
        self.text = text
        self.danger = danger
        self.danger_value = danger_value
        self.danger_obj = danger_obj
