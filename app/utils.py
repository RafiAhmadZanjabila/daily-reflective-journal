def get_emotion_color(emotion_type):
    COLORS = {
        'HEU': '#ec4325',
        'HEP': '#f9d50d',
        'LEU': '#016fdc',
        'LEP': '#06a074',
    }
    return COLORS.get(emotion_type, 'black')