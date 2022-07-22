from setuptools import find_packages, setup

setup(
    name="random_utilites",
    version="1.0.2",
    author="Hetchfund.Capital (Libby Lebyane)",
    author_email="<lebyane.lm@gmail.com>",
    description="Helper library for random operations",
    # package_dir={"": "random_utilities"},
    packages=find_packages(),
    install_requires=["console", "flask"],
    keywords=["random", "utilities", "tools", "helpers"]
)
