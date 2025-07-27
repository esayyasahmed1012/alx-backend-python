import json
from pathlib import Path

output_path = Path("/mnt/data/post_man-Collections.json")
with open(output_path, "w") as f:
    json.dump(postman_collection, f, indent=2)

output_path.name