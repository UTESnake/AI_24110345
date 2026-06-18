from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import geopandas as gpd


DATA_FILE = Path(__file__).with_name("data") / "hcm_districts.geojson"

# Thứ tự này giúp animation đi từ ngoại thành vào trung tâm và cho kết quả ổn định.
COLORING_ORDER = [
    "Cu Chi",
    "Hoc Mon",
    "Q12",
    "Go Vap",
    "Binh Tan",
    "Binh Chanh",
    "Phu Nhuan",
    "Tan Binh",
    "Tan Phu",
    "Thu Duc",
    "Binh Thanh",
    "Q1",
    "Q3",
    "Q10",
    "Q11",
    "Q5",
    "Q6",
    "Q8",
    "Q4",
    "Q7",
    "Nha Be",
    "Can Gio",
]

NAME_MAP = {
    "BìnhChánh": "Binh Chanh",
    "BìnhTân": "Binh Tan",
    "BìnhThạnh": "Binh Thanh",
    "CầnGiờ": "Can Gio",
    "CủChi": "Cu Chi",
    "GòVấp": "Go Vap",
    "HócMôn": "Hoc Mon",
    "NhàBè": "Nha Be",
    "PhúNhuận": "Phu Nhuan",
    "Quận1": "Q1",
    "Quận10": "Q10",
    "Quận11": "Q11",
    "Quận12": "Q12",
    "Quận2": "Thu Duc",
    "Quận3": "Q3",
    "Quận4": "Q4",
    "Quận5": "Q5",
    "Quận6": "Q6",
    "Quận7": "Q7",
    "Quận8": "Q8",
    "Quận9": "Thu Duc",
    "TânBình": "Tan Binh",
    "TânPhú": "Tan Phu",
    "ThủĐức": "Thu Duc",
}


def load_regions() -> gpd.GeoDataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Không tìm thấy {DATA_FILE}. Hãy chạy download_boundaries.py trước."
        )

    regions = gpd.read_file(DATA_FILE)[["NAME_2", "geometry"]]
    regions["name"] = regions["NAME_2"].map(NAME_MAP)
    regions = regions.dropna(subset=["name"])

    # Gộp ba đơn vị cũ thành Thành phố Thủ Đức như bản đồ mẫu.
    regions = regions[["name", "geometry"]].dissolve(by="name", as_index=False)
    regions = regions.to_crs(epsg=3857)

    order = {name: index for index, name in enumerate(COLORING_ORDER)}
    regions["_order"] = regions["name"].map(order)
    return regions.sort_values("_order").drop(columns="_order").reset_index(drop=True)


def load_graph(regions: gpd.GeoDataFrame | None = None) -> dict[str, list[str]]:
    regions = load_regions() if regions is None else regions
    by_name = regions.set_index("name").geometry
    graph: OrderedDict[str, list[str]] = OrderedDict(
        (name, []) for name in COLORING_ORDER
    )

    for index, name in enumerate(COLORING_ORDER):
        for other in COLORING_ORDER[index + 1 :]:
            # Chỉ tính là láng giềng khi cùng chung một đoạn biên. Hai vùng chỉ
            # chạm nhau tại một điểm vẫn có thể dùng cùng màu.
            shared_border = (
                by_name[name].boundary.intersection(by_name[other].boundary).length
            )
            if shared_border > 100:
                graph[name].append(other)
                graph[other].append(name)

    return dict(graph)


def load_polygons():
    """Tương thích với code cũ: nay trả về GeoDataFrame ranh thật."""
    return load_regions()
