## Embed `dict`'s structure

The embed `dict`'s structure is as followed:
```json
{
    "title":            Any,
    "description":      Any,
    "url":              Optional[str],
    "color":            Optional[colors.Colorish],
    "colour":           Optional[colors.Colorish],
    "timestamp":        Optional[datetime.datetime],
    "author":           dict
    {
        "name":         Optional[str],
        "url":          Optional[str],
        "icon":         Optional[files.Resourceish],
    },
        
    "footer":           dict
    {
        "text":         Optional[str],
        "icon":         Optional[files.Resourceish],
    },
    "thumbnail":        Optional[files.Resourceish],
    "image":            Optional[files.Resourceish],
    "fields":           Iterable
    [
        {
            "name":     str,
            "value":    str,
            "inline":   Optional[bool],
        },
    ],
}
```