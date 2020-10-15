def write_spectral_color(color, factor=1, asLight=False):
    if asLight:
        return "(illum %f %f %f)" % (factor * color[0], factor * color[1], factor * color[2])
    else:
        return "(refl %f %f %f)" % (factor * color[0], factor * color[1], factor * color[2])
