def write_spectral(exporter, spec_name, color):
    new_name = exporter.register_unique_name('SPEC', spec_name)

    exporter.w.write("(spectrum")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % spec_name)
    exporter.w.write(":data (rgb %f %f %f)" % color[:])

    exporter.w.goOut()
    exporter.w.write(")")

    return new_name