"""
Physical Layer - BPSK modulation over AWGN channel (Steps 6 & 7)
"""
import numpy as np

class PhysicalLayer:
    def __init__(self, snr_db=10):
        self.snr_db = snr_db
        self.snr_linear = 10 ** (snr_db / 10)

    def bytes_to_bits(self, data: bytes):
        return np.unpackbits(np.frombuffer(data, dtype=np.uint8))

    def bits_to_bytes(self, bits):
        # Pad if necessary
        if len(bits) % 8 != 0:
            bits = np.concatenate([bits, np.zeros(8 - len(bits) % 8, dtype=np.uint8)])
        return np.packbits(bits).tobytes()

    def bpsk_modulate(self, bits):
        """0 -> -1, 1 -> +1"""
        return 2 * bits - 1

    def awgn_channel(self, signal):
        """Add AWGN noise (Step 7)"""
        signal_power = np.mean(signal ** 2)
        noise_power = signal_power / self.snr_linear
        noise = np.sqrt(noise_power) * np.random.randn(len(signal))
        return signal + noise

    def bpsk_demodulate(self, received):
        """Threshold detection"""
        return (received > 0).astype(np.uint8)

    def transmit(self, frame: bytes):
        """Full PHY transmission: bits -> modulate -> AWGN -> demodulate -> bits"""
        bits = self.bytes_to_bits(frame)
        modulated = self.bpsk_modulate(bits)
        received = self.awgn_channel(modulated)
        demodulated = self.bpsk_demodulate(received)
        bit_errors = np.sum(bits != demodulated)
        ber = bit_errors / len(bits)
        received_bytes = self.bits_to_bytes(demodulated)
        return received_bytes, ber