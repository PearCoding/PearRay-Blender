def write_spectral(exporter, spec_name, color):
    new_name = exporter.make_unique_name(exporter.spec_instances, spec_name)
    exporter.spec_instances.append(new_name)

    exporter.w.write("(spectrum")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % spec_name)
    exporter.w.write(":data (rgb %f %f %f)" % color[:])

    exporter.w.goOut()
    exporter.w.write(")")

    return new_name