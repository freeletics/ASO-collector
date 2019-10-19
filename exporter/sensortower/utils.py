from exporter import config
from exporter.utils import export_writer


class Executor:
    android_countries = config.COUNTRIES
    ios_countries = config.COUNTRIES

    def __init__(self, exporter):
        self.exporter = exporter

    def execute(self, export_from, export_to):
        params_list = self.get_params_list(export_from, export_to)
        exported_data = self.get_export_data(params_list, self.exporter)
        proccessed_data = self.get_proccessed_data(exported_data)
        self.write_export(proccessed_data)

    def get_params(self):
        raise NotImplementedError

    def get_export_data(self):
        raise NotImplementedError

    def get_proccessed_data(self):
        raise NotImplementedError

    def get_params_list(self, export_from, export_to):
        params_list = []
        for country in config.COUNTRIES:
            for app_id, platform in config.SENSORTOWER_APPS.items():
                params = self.get_params(export_from, export_to, app_id, platform, country)
                params_list.append(params)
        return params_list

    def write_export(self, data):
        writer = export_writer.ExportWriter()
        self.write_export_for_platform(writer, data, "ios", self.ios_countries)
        self.write_export_for_platform(writer, data, "android", self.android_countries)

    def write_export_for_platform(self, writer, data, platform_name, countries):
        filename_ios = self.get_filename(platform_name, self.kpi)
        filtered_data = self.filter_data_for_platform(data, platform_name)
        writer.export_data(
            filtered_data, filename_ios, self.get_export_field_list(countries)
        )

    def filter_data_for_platform(self, data, platform_name):
        return {
            (date, platform): value
            for (date, platform), value in data.items()
            if platform == platform_name
        }

    def get_filename(self, platform_name, kpi):
        return f"{config.EXPORTED_DATA_DIR}/sensortower_{kpi}_{platform_name}_daily.csv"
