from http.server import BaseHTTPRequestHandler
import json
import numpy as np
from scipy.linalg import solve_continuous_are

def calculate_k(q_val, r_val):
    # 转向执行器模型: 状态 x = [角度误差, 角速度]
    A = np.array([[0, 1], [0, 0]])
    B = np.array([[0], [1]])
    Q = np.diag([float(q_val), 0.1])
    R = np.array([[float(r_val)]])
    try:
        P = solve_continuous_are(A, B, Q, R)
        K = np.linalg.inv(R) @ B.T @ P
        return K.flatten().tolist()
    except:
        return [1.0, 0.5] # 默认备选值

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        K = calculate_k(data.get('q', 10), data.get('r', 1))
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = {'K': K}
        self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
