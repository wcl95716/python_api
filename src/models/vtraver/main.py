import subprocess

subprocess.run([
    "vtracer",
    "--input", "panda.png",
    "--output", "panda.svg",
    "--mode", "color",
    "--posterize", "20",
    "--filter_speckle"
])
