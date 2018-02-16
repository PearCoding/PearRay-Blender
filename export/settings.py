def setup_settings(pr, settings, scene):
    s = scene.pearray
    settings.integratorMode = pr.IntegratorMode.__members__[s.integrator]
    settings.debugMode = pr.DebugMode.__members__[s.debug_mode]
    settings.maxRayDepth = s.max_ray_depth

    settings.tileMode = pr.TileMode.__members__[s.render_tile_mode]

    settings.aaSampler = pr.SamplerMode.__members__[s.sampler_aa_mode]
    settings.maxAASampleCount = s.sampler_max_aa_samples
    settings.lensSampler = pr.SamplerMode.__members__[s.sampler_lens_mode]
    settings.maxLensSampleCount = s.sampler_max_lens_samples
    settings.timeSampler = pr.SamplerMode.__members__[s.sampler_time_mode]
    settings.maxTimeSampleCount = s.sampler_max_time_samples
    settings.timeMappingMode = pr.TimeMappingMode.__members__[s.sampler_time_mapping_mode]
    settings.timeScale = s.sampler_time_scale
    settings.spectralSampler = pr.SamplerMode.__members__[s.sampler_spectral_mode]
    settings.maxSpectralSampleCount = s.sampler_max_spectral_samples

    settings.maxDiffuseBounces = s.max_diffuse_bounces
    settings.maxLightSamples = s.max_light_samples

    settings.ppm.maxPhotonsPerPass = s.photon_count
    settings.ppm.maxPassCount = s.photon_passes
    settings.ppm.maxGatherRadius = s.photon_gather_radius
    settings.ppm.maxGatherCount = s.photon_max_gather_count
    settings.ppm.gatheringMode = pr.PPMGatheringMode.__members__[s.photon_gathering_mode]
    settings.ppm.squeezeWeight = s.photon_squeeze/100
    settings.ppm.contractRatio = s.photon_ratio/100
