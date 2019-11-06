from exporter import config
from exporter.utils import func
from exporter.utils import export_writer


class Executor:
    android_field_list_params = config.COUNTRIES
    ios_field_list_params = config.COUNTRIES
    export_writer_class = export_writer.ExportWriter

    def __init__(self, exporter):
        self.exporter = exporter
        self.writer = self.export_writer_class()

    @property
    def apps(self):
        raise NotImplementedError

    @property
    def kpi(self):
        raise NotImplementedError

    @property
    def source_name(self):
        raise NotImplementedError

    def execute(self, export_from, export_to):
        export_from = self.optimize_export_from(export_from)
        params_list = self.get_params_list(export_from, export_to)
        exported_data = self.get_export_data(params_list, self.exporter)
        proccessed_data = self.get_proccessed_data(exported_data)
        self.write_export(proccessed_data)
        self.writer.upload_files()

    def get_params(self, *args, **kwargs):
        raise NotImplementedError

    def get_export_data(self, params_list, exporter):
        raise NotImplementedError

    def get_proccessed_data(self, exported_data):
        raise NotImplementedError

    def get_export_field_list(self, filed_list_params):
        raise NotImplementedError

    def get_params_list(self, export_from, export_to):
        params_list = []
        for country in config.COUNTRIES:
            for app_id, platform in self.apps.items():
                params = self.get_params(
                    export_from, export_to, app_id, platform, country
                )
                params_list.append(params)
        return params_list

    def write_export(self, data):
        self.write_export_for_platform(
            self.writer, data, "ios", self.ios_field_list_params
        )
        self.write_export_for_platform(
            self.writer, data, "android", self.android_field_list_params
        )

    def write_export_for_platform(self, writer, data, platform_name, filed_list_params):
        filename_ios = self.get_filename(platform_name, self.kpi)
        filtered_data = self.filter_data_for_platform(data, platform_name)
        writer.export_data(
            filtered_data, filename_ios, self.get_export_field_list(filed_list_params)
        )

    def filter_data_for_platform(self, data, platform_name):
        return {
            (date, platform): value
            for (date, platform), value in data.items()
            if platform == platform_name
        }

    def get_filename(self, platform_name, kpi):
        return f"{config.EXPORTED_DATA_DIR}/{self.source_name}_{kpi}_{platform_name}_days.csv"

    def optimize_export_from(self, export_from):
        if config.OPTIMIZE_EXPORT_FROM:
            return self.get_last_date(export_from)
        else:
            return export_from

    def get_last_date(self, export_from):
        return max(
            [
                func.get_last_date(export_from, self.get_filename(platform, self.kpi))
                for platform in self.apps.values()
            ]
        )
