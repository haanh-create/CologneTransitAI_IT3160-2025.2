import osmnx as ox
import networkx as nx
import json
import os

def fetch_cologne_transit():
    print("Fetching Cologne transit data...")
    place_name = "Cologne, Germany"
    
    # Define transit tags
    custom_filter = '["railway"~"subway|tram|light_rail|rail"]'
    
    try:
        # Get graph from OSM
        G = ox.graph_from_place(place_name, custom_filter=custom_filter, retain_all=True)
        
        print(f"Retrieved {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
        
        # 1. Giữ lại thành phần liên thông lớn nhất (optional, nhưng tốt cho pathfinding)
        # Đối với transit, có thể có nhiều thành phần rời rạc (ví dụ: các tuyến không nối nhau)
        # Nhưng thường chúng nối nhau qua các trạm trung chuyển.
        
        # 2. Chuyển đổi sang định dạng có thể lưu JSON
        # Chúng ta cần: Danh sách trạm (nodes) và Danh sách kết nối (edges)
        
        nodes_data = []
        for node, data in G.nodes(data=True):
            nodes_data.append({
                "id": node,
                "lat": data.get('y'),
                "lon": data.get('x'),
                "name": data.get('name', f"Station {node}")
            })
            
        edges_data = []
        for u, v, data in G.edges(data=True):
            # Lấy tên tuyến (ví dụ: Line 1, S11, ...)
            # Trong OSM, railway lines thường có tag 'route' hoặc 'ref'
            line_name = data.get('ref', data.get('name', 'Unknown Line'))
            
            # Tính khoảng cách (độ dài cạnh)
            length = data.get('length', 0)
            
            edges_data.append({
                "source": u,
                "target": v,
                "line": line_name,
                "length": length,
                "oneway": data.get('oneway', False)
            })
            
        network = {
            "nodes": nodes_data,
            "edges": edges_data
        }
        
        # Lưu vào thư mục data
        output_path = os.path.join("data", "cologne_network.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(network, f, ensure_ascii=False, indent=4)
            
        print(f"Success! Data saved at: {output_path}")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    # Đảm bảo thư mục data tồn tại
    if not os.path.exists("data"):
        os.makedirs("data")
    fetch_cologne_transit()
