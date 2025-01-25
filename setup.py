from setuptools import setup, find_packages

setup(
    name="SubNXT",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.26.0",
        "openai-whisper==20231106",
        "moviepy==1.0.3",
    ],
)
