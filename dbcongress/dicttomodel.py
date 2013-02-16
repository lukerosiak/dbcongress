
def dictToModel(model,json,pk=None):
    obj = {}    
    if pk and pk in json.keys():
        obj['pk'] = json[pk]
    for field in model._meta.local_fields:
        if field.column in json.keys():
            obj[field.column] = json[field.column]
    return obj
