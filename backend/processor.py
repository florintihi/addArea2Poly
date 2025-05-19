import ezdxf
from ezdxf.math import Vec2

def process_dxf(input_path, output_path):
    try:
        doc = ezdxf.readfile(input_path)
        msp = doc.modelspace()

        for entity in list(msp):  # Iterate over a copy to allow adding entities
            if entity.dxftype() == 'LWPOLYLINE':
                points = list(entity.get_points(format='xy'))
                if len(points) < 3:
                    continue  # Skip non-closed or invalid polylines

                # Shoelace formula for area
                area = 0.0
                num_points = len(points)
                for i in range(num_points):
                    x1, y1 = points[i]
                    x2, y2 = points[(i + 1) % num_points]
                    area += (x1 * y2 - x2 * y1)
                area = abs(area) / 2.0

                # Centroid calculation
                centroid_x = sum(p[0] for p in points) / num_points
                centroid_y = sum(p[1] for p in points) / num_points
                centroid = Vec2(centroid_x, centroid_y)

                # Add text label
                text = msp.add_text(f"{area:.0f}", dxfattribs={'height': 1.0})
                text.set_placement(centroid)

        doc.saveas(output_path)

    except Exception as e:
        print(f"Processing error: {e}")
        raise
