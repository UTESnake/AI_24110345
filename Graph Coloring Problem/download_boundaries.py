from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import unicodedata

import contextily as ctx
import geopandas as gpd
import requests


OVERPASS_URL = "https://overpass-api.de/api/interpreter"
USER_AGENT = "hcm-map-coloring-student-project/1.0"
DATA_DIR = Path(__file__).with_name("data")
GADM_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_VNM_2.json.zip"


def normalized(text: str | None) -> str:
    value = unicodedata.normalize("NFKD", text or "")
    return "".join(char for char in value if not unicodedata.combining(char)).lower()


def overpass(query: str) -> dict:
    response = requests.post(
        OVERPASS_URL,
        data=query.encode("utf-8"),
        headers={"User-Agent": USER_AGENT},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def list_candidate_relations() -> list[dict]:
    query = """
    [out:json][timeout:90];
    (
      relation(10.30,106.30,11.25,107.15)
        ["boundary"="administrative"]["admin_level"="6"];
      relation(10.30,106.30,11.25,107.15)
        ["historic"="administrative"];
    );
    out tags center;
    """
    return overpass(query).get("elements", [])


def download_gadm() -> Path:
    response = requests.get(
        GADM_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=180,
    )
    response.raise_for_status()
    with ZipFile(BytesIO(response.content)) as archive:
        member = next(name for name in archive.namelist() if name.endswith(".json"))
        raw = json.loads(archive.read(member))

    features = []
    for feature in raw["features"]:
        province = normalized(feature["properties"].get("NAME_1"))
        if "hochiminh" in province.replace(" ", ""):
            features.append(feature)
    if not features:
        nearby_names = sorted(
            {
                feature["properties"].get("NAME_1", "")
                for feature in raw["features"]
                if "minh" in normalized(feature["properties"].get("NAME_1"))
                or "ho " in normalized(feature["properties"].get("NAME_1"))
            }
        )
        raise RuntimeError(f"Cannot find HCMC in GADM names: {nearby_names}")
    output = DATA_DIR / "hcm_districts.geojson"
    output.write_text(
        json.dumps(
            {"type": "FeatureCollection", "features": features},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return output


def download_basemap(boundary_file: Path) -> Path:
    regions = gpd.read_file(boundary_file)
    west, south, east, north = regions.total_bounds
    pad_x = (east - west) * 0.12
    pad_y = (north - south) * 0.06
    output = DATA_DIR / "hcm_basemap.tif"
    ctx.bounds2raster(
        west - pad_x,
        south - pad_y,
        east + pad_x,
        north + pad_y,
        str(output),
        zoom=10,
        source=ctx.providers.OpenStreetMap.Mapnik,
        ll=True,
    )
    return output


if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    output = download_gadm()
    basemap = download_basemap(output)
    data = json.loads(output.read_text(encoding="utf-8"))
    print("Saved:", output)
    print("Saved:", basemap)
    for feature in data["features"]:
        print(feature["properties"].get("NAME_2"))
