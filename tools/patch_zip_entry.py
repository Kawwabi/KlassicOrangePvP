#!/usr/bin/env python3
"""Replace one entry of a ZIP by patching its central directory in place."""
import struct, sys, zlib

zip_path, entry_name, new_file = sys.argv[1:4]
data = open(zip_path, "rb").read()
new = open(new_file, "rb").read()

eocd = data.rfind(b"PK\x05\x06")
if eocd < 0:
    sys.exit("no end-of-central-directory record found")
_, disk, cd_disk, n_disk, n_total, cd_size, cd_off, comment_len = struct.unpack(
    "<4s4H2IH", data[eocd:eocd + 22])

cd_start = eocd - cd_size
base = cd_start - cd_off
if base < 0 or data[cd_start:cd_start + 4] != b"PK\x01\x02":
    sys.exit("central directory is not where expected; refusing to patch")

CEN = struct.Struct("<4s6H3I5H2I")
LOC = struct.Struct("<4s5H3I2H")
name_b = entry_name.encode()
crc = zlib.crc32(new) & 0xFFFFFFFF
new_local_off = cd_start - base

pos, out_cd, found, new_local = cd_start, bytearray(), False, b""
while pos < eocd:
    if data[pos:pos + 4] != b"PK\x01\x02":
        sys.exit(f"bad central directory entry at {pos}")
    f = list(CEN.unpack_from(data, pos))
    nlen, xlen, clen = f[10], f[11], f[12]
    end = pos + CEN.size + nlen + xlen + clen
    name = data[pos + CEN.size:pos + CEN.size + nlen]
    if name == name_b and not found:
        found = True
        f[2], f[3], f[4] = 20, 0, 0              # version needed, flags, method=stored
        f[7], f[8], f[9] = crc, len(new), len(new)
        f[11], f[12], f[13] = 0, 0, 0            # no extra, no comment, disk 0
        f[16] = new_local_off
        out_cd += CEN.pack(*f) + name
        new_local = LOC.pack(b"PK\x03\x04", 20, 0, 0, f[5], f[6], crc,
                             len(new), len(new), len(name_b), 0) + name_b + new
    else:
        out_cd += data[pos:end]
    pos = end
if pos != eocd:
    sys.exit("central directory did not end where expected")
if not found:
    sys.exit(f"entry not found: {entry_name}")

new_cd_off = new_local_off + len(new_local)
new_eocd = struct.pack("<4s4H2IH", b"PK\x05\x06", disk, cd_disk, n_disk, n_total,
                       len(out_cd), new_cd_off, comment_len) + data[eocd + 22:]

open(zip_path, "wb").write(data[:cd_start] + new_local + bytes(out_cd) + new_eocd)
print(f"patched {entry_name}: {len(data)} -> {cd_start + len(new_local) + len(out_cd) + len(new_eocd)} bytes")
