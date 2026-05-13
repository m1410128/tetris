from setuptools import setup, find_packages

setup(
    name="tetris-game",
    version="1.0.0",
    description="A Tetris game implementation with ranking system",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/tetris",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "tetris=tetris.main:main",
        ],
    },
)
