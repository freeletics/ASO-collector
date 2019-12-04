from setuptools import setup, find_packages

setup(
    name="ASO_KPI",
    packages=find_packages(),
    entry_points={
        "distutils.commands": [
            "clear_old_logs = commands.clear_old_logs:ClearOldLogs",
            "remove_raw_data = commands.remove_raw_data:RemoveRawData",
        ]
    },
)

