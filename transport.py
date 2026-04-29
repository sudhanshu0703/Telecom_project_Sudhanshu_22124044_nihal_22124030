"""
Transport Layer - Segmentation and reliable delivery
"""

class TransportLayer:
    def __init__(self):
        self.seq_num = 0
        self.MSS = 64  # Max Segment Size in bytes

    def segment(self, data: bytes):
        """Break data into segments"""
        segments = []
        for i in range(0, len(data), self.MSS):
            chunk = data[i:i + self.MSS]
            header = f"SEQ:{self.seq_num}|".encode('utf-8')
            segments.append(header + chunk)
            self.seq_num += 1
        return segments

    def reassemble(self, segments):
        """Reassemble received segments"""
        data = b''
        for seg in segments:
            try:
                _, payload = seg.split(b'|', 1)
                data += payload
            except ValueError:
                continue
        return data