from setuptools import setup, find_packages


def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


# 基础依赖从 requirements.txt 读取
requirements = read_requirements('requirements.txt')


setup(
    name="KlineDrawer",
    version="0.0.4",
    packages=find_packages(),
    install_requires=requirements,
    author="DoubleLiu",
    description="A drawer for stock kline data",
    python_requires=">=3.7",
)
