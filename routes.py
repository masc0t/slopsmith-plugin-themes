"""Themes plugin — persist active theme ID in config_dir."""

import json
from pathlib import Path
from fastapi import FastAPI, Request


DEFAULT_ACTIVE = "classic-dark"


def setup(app: FastAPI, context: dict):
    config_dir = Path(context["config_dir"])
    config_file = config_dir / "themes.json"

    def _read() -> dict:
        if not config_file.exists():
            return {"active": DEFAULT_ACTIVE}
        try:
            data = json.loads(config_file.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return {"active": DEFAULT_ACTIVE}
            return data
        except Exception:
            return {"active": DEFAULT_ACTIVE}

    def _write(config: dict) -> None:
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file.write_text(json.dumps(config), encoding="utf-8")

    @app.get("/api/plugins/themes/config")
    def get_config():
        return _read()

    @app.post("/api/plugins/themes/config")
    async def set_config(req: Request):
        new_data = await req.json()
        config = _read()
        config.update(new_data)
        if "active" not in config:
            config["active"] = DEFAULT_ACTIVE
        _write(config)
        return {"ok": True, "config": config}
