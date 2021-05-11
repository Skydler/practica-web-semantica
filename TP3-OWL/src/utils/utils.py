import unicodedata


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def normalize_special_symbols(s):
    # This could be done with regex
    replacements = (
        (" ", ""),
        (":", "_"),
        (".", ""),
        ("&", "And"),
        ("/", "_"),
        ("%", ""),
        ("’", ""),
        ("-", "_"),
        ("!", ""),
        ("'", ""),
        (",", ""),
        ("(", ""),
        (")", ""),
    )

    for a, b in replacements:
        s = s.replace(a, b)

    return s


def to_turtle_fmt(text):
    fmted_text = text.lower()
    fmted_text = remove_accents(fmted_text)
    fmted_text = fmted_text.title()
    fmted_text = normalize_special_symbols(fmted_text)
    return fmted_text
