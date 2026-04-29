"""
Data Link Layer - Framing and ARQ (Step 5)
Implements Stop-and-Wait ARQ
"""
import zlib
import random

class DataLinkLayer:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries
        self.retransmissions = 0

    def framing(self, packet: bytes):
        """Convert packet to frame with CRC"""
        crc = zlib.crc32(packet).to_bytes(4, 'big')
        flag = b'\x7E'  # Frame delimiter
        frame = flag + packet + crc + flag
        return frame

    def deframe(self, frame: bytes):
        """Extract packet from frame, verify CRC"""
        if frame[0:1] != b'\x7E' or frame[-1:] != b'\x7E':
            return None, False
        payload = frame[1:-5]
        received_crc = frame[-5:-1]
        computed_crc = zlib.crc32(payload).to_bytes(4, 'big')
        return payload, (received_crc == computed_crc)

    def stop_and_wait_arq(self, frame, channel_send_func):
        """ARQ: Send frame, retransmit on failure"""
        for attempt in range(self.max_retries):
            success = channel_send_func(frame)
            if success:
                return True, attempt
            self.retransmissions += 1
        return False, self.max_retries