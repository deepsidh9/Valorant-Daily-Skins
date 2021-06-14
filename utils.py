def validate_input(entities):
    for entity in entities:
        if not isinstance(entity, str) or len(entity) == 0:
            return False
    return True

def get_client_ip(request):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']  # if behind a proxy

test_skins=[{'displayName':'Glitchpop Odin','displayIcon':"https://media.valorant-api.com/weaponskinchromas/9667983e-4c8c-e5b2-68d7-be84f9b3d46c/displayicon.png"},
{'displayName':'Prime 2 Phantom','displayIcon':"https://media.valorant-api.com/weaponskinchromas/9e59563c-4467-43df-3b58-2ca43c25abde/displayicon.png"}]