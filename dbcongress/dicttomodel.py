"""Use model introspection to match a Python dictionary to a model's field. It:
1) Throws away any of the dict's fields that aren't present in the model
2) If the model's field has a verbose_name, it uses that instead of the field name
3) It can traverse nested dictionaries using the double-underscore syntax in the model's verbose__name. So if your dict is
{sponsor: {name: Joe Smith, state: 'VA'}}
your model fields can be
sponsor_name = models.TextField(verbose_name="sponsor__name")
sponsor_state = models.TextField(verbose_name="sponsor__state")

If you have a list of dictionary objects generated from JSON or the like, create models like this:
for j in jsonlist:
    vote = Vote.objects.create(**dictToModel(Vote,j))

By Luke Rosiak
"""

import copy



def dictToModel(model,json):

    def traverse(verbose,j):
        chunks = verbose.split('__')
        if chunks[0] in j.keys():
            j = j[chunks[0]]
            if type(j)==list:
                j = j[0]
            if len(chunks)==1:
                return j
            else:
                return traverse('__'.join(chunks[1:]),j)
        return None

    obj = {}    
    for field in model._meta.local_fields:
        if field.verbose_name.replace(' ','_')!=field.column:
            if field.verbose_name in json.keys():
                obj[field.column] = json[field.verbose_name]
            elif '__' in field.verbose_name:
                match = traverse(field.verbose_name,copy.deepcopy(json))
                if match:
                    obj[field.column] = match                    

        elif field.column in json.keys():
            obj[field.column] = json[field.column]

    for key in obj.keys(): #can't pass None values to Postgres or it tries to force Null into not-null fields
        if obj[key]==None:
            del obj[key]

    return obj
    

