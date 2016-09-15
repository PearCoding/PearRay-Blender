def export_texture(exporter, texture):
    if not texture:
        return
    
    if texture.name in exporter.instances['TEXTURE']:
        return

    name = exporter.register_unique_name('TEXTURE', texture.name)



    return name
    