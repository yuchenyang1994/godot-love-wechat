from nicegui import ui, app
import webview
from app.stroge import Storge
from app.exporter import Exporter
from dataclasses import dataclass, field
from PIL import Image

@dataclass
class ProjectsStorge:
    storge: Storge = field(default_factory=Storge)

    def get_project_by_id(self, id: str):
        projects = self.storge.get("projects.json")
        if not projects:
            return None
        for project in projects:
            if project["id"] == id:
                return project

@dataclass
class ExportSettings:
    appid: str = field(default="")
    device_orientation: str = field(default="portrait")
    export_template: str = field(default="")
    export_path: str = field(default="")

    def read_project_export_settings(self, project_path: str):
        pass

    def save(self, project_path: str):
        pass

    def to_dict(self):
        return {
            "appid": self.appid,
            "device_orientation": self.device_orientation,
            "export_template": self.export_template,
            "export_path": self.export_path
        }
    
        

stroge = ProjectsStorge()
export_settings = ExportSettings()
exporter = Exporter()


def project_info(project):
    async def on_click_export():
        if not export_settings.export_path:
            ui.notify("未填写导出目录", type="negative")
            return
        if not export_settings.export_template:
            ui.notify("未选择导出模板", type="negative")
            return
        if not export_settings.appid:
            ui.notify("未填写APPID", type="negative")
            return
    with ui.row(align_items="center").classes("w-full"):
        with ui.column(align_items="center").classes("w-1/5"):
            ui.image(Image.open(project["icon"])).classes("w-32 h-32")
        with ui.column(align_items="baseline").classes("w-2/5 mt-2"):
            ui.label(project["name"]).classes("text-h6")
            ui.label(f"Version: {project["version"]}").classes("text-subtitle2")
            ui.label(project["description"]).classes("text-caption")

        ui.space()
        with ui.column(align_items="start").classes("w-1/5 p-4"):
            ui.button("导出", icon="import_export")
            ui.button("预览", icon="play_arrow")
            ui.button("返回", icon="arrow_back").props("outline")

def export_config():
    async def chosse_export_path():
        file = await app.native.main_window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG, allow_multiple=False, file_types=()) # type: ignore
        if file:
            export_settings.export_path = file[0]
    templates = exporter.get_tempalte_json()
    templates_options = {i["filename"]: i["name"] for i in templates}
    with ui.row(align_items="start").classes("w-full border-b p-4"):
        ui.label("导出设置")
    with ui.column(align_items="start").classes("w-full p-4"):
        with ui.row(align_items="center").classes("border-b w-full p-2"):
            ui.label("APPID")
            ui.space()
            ui.input().props("outlined outlined dense").classes("w-64").bind_value(export_settings, "appid")
        with ui.row(align_items="center").classes("border-b w-full p-2"):
            ui.label("屏幕方向")
            ui.space()
            ui.select({"portrait": "横向", "landscape": "竖向"}).props("outlined outlined dense").classes("w-64").bind_value(export_settings, "device_orientation")
        with ui.row(align_items="center").classes("border-b w-full p-2"):
            ui.label("导出模板")
            ui.space()
            ui.select(templates_options).props("outlined outlined dense").classes("w-64").bind_value(export_settings, "export_template")
        with ui.row(align_items="center").classes("border-b w-full p-2"):
            ui.label("导出目录")
            ui.space()
            with ui.input().props("outlined outlined dense").classes("w-64").bind_value(export_settings, "export_path"):
                ui.button(icon="folder_open", on_click=chosse_export_path).props("flat dense")

        
        


def project(id: str):
    project = stroge.get_project_by_id(id)
    with ui.column(align_items="start").classes("w-full p-2"):
        with ui.card(align_items="start").tight().classes("w-full"):
            project_info(project)
        with ui.card(align_items="start").tight().classes("w-full"):
            export_config()
