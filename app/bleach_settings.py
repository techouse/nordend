from bleach_whitelist import generally_xss_safe, standard_styles

allowed_tags = generally_xss_safe + ["audio", "iframe", "embed", "source", "video"]
allowed_tags.sort()

allowed_styles = standard_styles

allowed_attributes = {
    "*": ["id", "data-id", "class", "style", "title", "label"],
    "a": ["href", "alt", "title", "target"],
    "audio": ["controls"],
    "dialog": ["open"],
    "embed": ["src"],
    "iframe": ["src", "data-start", "data-thumb", "allowfullscreen", "allow", "width", "height", "frameborder"],
    "img": ["src", "width", "height", "alt", "srcset", "sizes"],
    "source": ["media", "srcset", "type", "src"],
    "td": ["colspan", "rowspan", "headers"],
    "th": ["colspan", "rowspan", "scope", "sorted", "headers", "abbr"],
    "video": ["controls", "width", "height"],
    "meter": ["optimum", "high", "max", "value"],
    "progress": ["value", "max"],
    "time": ["datetime"],
    "option": ["value"]
}
