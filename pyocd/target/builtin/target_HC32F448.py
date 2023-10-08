# pyOCD debugger
# Copyright (c) 2022 Huada Semiconductor Corporation
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ...coresight.coresight_target import CoreSightTarget
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd.loader import SVDFile


class DBGMCU:
    STPCTL = 0xE0042020
    STPCTL_VALUE = 0x7FFFFF

    STPCTL1 = 0xE0042028
    STPCTL1_VALUE = 0xFFF

    TRACECTL = 0xE0042024
    TRACECTL_VALUE = 0x0

FLASH_ALGO = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xE00ABE00, 
    0x4770ba40, 0x4770ba40, 0x4770ba40, 0x4770bac0, 0x4770bac0, 0x4770bac0, 0x0030ea4f, 0x00004770,
    0x0030ea4f, 0x00004770, 0x0030ea4f, 0x00004770, 0x49052000, 0x49057008, 0x20016008, 0x39264902,
    0x002af881, 0x00004770, 0x40054026, 0x40010418, 0x6800480d, 0x0001f000, 0x480cb118, 0x6008490c,
    0x480ce002, 0x6008490a, 0x490b2003, 0x480b6008, 0x6208490b, 0x490a2000, 0x7008312a, 0x49082005,
    0x0026f881, 0x00004770, 0x40010684, 0x33306381, 0x40054100, 0x33304f81, 0x40010418, 0x00116310,
    0x40054000, 0xf000b510, 0xbd10f83f, 0x4604b510, 0xf0004620, 0xbd10f8a3, 0x49142000, 0xf44f6008,
    0x49133040, 0x20006008, 0x60081f09, 0x391c4910, 0x20016008, 0x7008490f, 0x490e480f, 0xf8c13926,
    0x20000100, 0x20016208, 0x1d09490a, 0x480b7008, 0x6008490b, 0x604812c0, 0x6108480a, 0x4025f44f,
    0x39264904, 0x03fef8a1, 0x00004770, 0x40010590, 0x4001041c, 0x40054026, 0x11101300, 0xfffffa0e,
    0x40048000, 0xa5a50000, 0xf000b570, 0xf240f989, 0x492e1005, 0x25006008, 0x2000148c, 0xe0076020,
    0x482b1c6d, 0xd3034285, 0xf97af000, 0xbd702001, 0x1d004826, 0xf4006800, 0xf5b07080, 0xd1ef7f80,
    0x4822e007, 0x68003008, 0x0010f040, 0x3108491f, 0x481e6008, 0x68001d00, 0x0010f000, 0xd1f02800,
    0x491a2004, 0x4c1b6008, 0x60202000, 0xf958f000, 0x4816e007, 0x68003008, 0x0010f040, 0x31084913,
    0x48126008, 0x68001d00, 0x0010f000, 0xd1f02800, 0x490e2004, 0x4c106008, 0x60202000, 0xf940f000,
    0x480ae007, 0x68003008, 0x0010f040, 0x31084907, 0x48066008, 0x68001d00, 0x0010f000, 0xd1f02800,
    0x60084902, 0xf92cf000, 0xe7b02000, 0x4001041c, 0x00061a80, 0x03002000, 0x03004000, 0x4604b570,
    0xf0002500, 0x2004f91d, 0x60084915, 0x60202000, 0x1c6de007, 0x42854813, 0xf000d303, 0x2001f911,
    0x480fbd70, 0x68001d00, 0x7080f400, 0x7f80f5b0, 0xe007d1ef, 0x3008480a, 0xf0406800, 0x49080010,
    0x60083108, 0x1d004806, 0xf0006800, 0x28000010, 0x4903d1f0, 0xf0006008, 0x2000f8f3, 0x0000e7e0,
    0x4001041c, 0x00061a80, 0xf000b510, 0xf240f8e9, 0x49101023, 0xf2436008, 0x60082010, 0x30fff04f,
    0x6008490d, 0x490b480d, 0x60081d09, 0x600843c0, 0x4908480b, 0x60083118, 0x1d0912c0, 0xf24a6008,
    0x49085001, 0xf7ff8008, 0xf7fffec3, 0xf000fed1, 0xbd10f8c7, 0x40010400, 0x40010590, 0x01234567,
    0x00080005, 0x400543fe, 0x43f8e92d, 0x460c4605, 0xf6494616, 0x90004040, 0xf24046b0, 0x492b1003,
    0x462f6008, 0x4040f649, 0xbf009000, 0xf8a8f000, 0x0000f8d8, 0x20006038, 0xe00c9000, 0x1c409800,
    0xf6499000, 0x98004140, 0xd3044288, 0xf898f000, 0xe8bd2001, 0x481d83f8, 0x68001d00, 0x0010f000,
    0xd1eb2810, 0x4819e007, 0x68003008, 0x0010f040, 0x31084916, 0x48156008, 0x68001d00, 0x0010f000,
    0xd0f02810, 0x0804f108, 0x1f241d3f, 0xd2cd2c04, 0x490e2000, 0x90006008, 0x9800e00b, 0x90001c40,
    0x4140f649, 0x42889800, 0xf000d303, 0x2001f869, 0x4806e7cf, 0x68001d00, 0x7080f400, 0x7f80f5b0,
    0xf000d1eb, 0x2000f85d, 0x0000e7c3, 0x4001041c, 0x4604b570, 0x4616460d, 0xff66f7ff, 0xbd702000,
    0x4604b570, 0x4616460d, 0x46294632, 0xf7ff4620, 0xbd70ff8b, 0x49034802, 0x48036008, 0x47706008,
    0xffff0123, 0x40049408, 0xffff3210, 0x4604b510, 0xfe72f7ff, 0xbd102000, 0x4604b5f0, 0x2300460d,
    0x27002600, 0x21004626, 0xf856e007, 0x6810cb04, 0xd0004584, 0x1d12e004, 0xebb11c49, 0xd3f40f95,
    0x4637bf00, 0xe0062300, 0xcb01f817, 0x45845cd0, 0xe004d000, 0xf0051c5b, 0x42980003, 0xbf00d8f4,
    0x0081eb04, 0xbdf04418, 0x49034802, 0x48036088, 0x47706088, 0xffff0123, 0x40049000, 0xffff3210,
    0x4807b500, 0xf4006800, 0xb9083080, 0xf854f000, 0x68004803, 0x0001f000, 0xf000b908, 0xbd00f809,
    0x40010680, 0x1e01bf00, 0x0001f1a0, 0x4770d1fb, 0x481fb510, 0xb2826800, 0x6800481e, 0x0481f3c0,
    0x6800481c, 0x2303f3c0, 0x1192b90c, 0x2c01e008, 0x1292d101, 0x2c02e004, 0x1312d101, 0x1392e000,
    0x2b0fb10b, 0xf7ffd102, 0xe020ff85, 0x0001f003, 0xb9e2b118, 0xff7ef7ff, 0xf003e019, 0x28020002,
    0x2a01d104, 0xf7ffd113, 0xe010ff75, 0x0004f003, 0xd1042804, 0xd10a2a02, 0xff6cf7ff, 0xf003e007,
    0x28080008, 0x2a03d103, 0xf7ffd101, 0xbd10ff63, 0x40049404, 0x40010680, 0x4823b510, 0xb2826840,
    0x68004822, 0x4481f3c0, 0x68004820, 0x6303f3c0, 0x1192b90c, 0x2c01e008, 0x1292d101, 0x2c02e004,
    0x1312d101, 0x1392e000, 0x2001b90b, 0x2000e000, 0xd1012b0f, 0xe0002101, 0x43082100, 0xf7ffb110,
    0xe020ff73, 0x0001f003, 0xb9e2b118, 0xff6cf7ff, 0xf003e019, 0x28020002, 0x2a01d104, 0xf7ffd113,
    0xe010ff63, 0x0004f003, 0xd1042804, 0xd10a2a02, 0xff5af7ff, 0xf003e007, 0x28080008, 0x2a03d103,
    0xf7ffd101, 0xbd10ff51, 0x40049000, 0x40010680, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000395,
    'pc_unInit': 0x200003d1,
    'pc_program_page': 0x200003a5,
    'pc_erase_sector': 0x200000b1,
    'pc_eraseAll': 0x200000a9,

    'static_base' : 0x20000000 + 0x00000004 + 0x00000590,
    'begin_stack' : 0x20000800,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x200,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001200],   # Enable double buffering
    'min_program_length' : 0x200,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x40000,
    'sector_sizes': (
        (0x0, 0x2000),
    )
}


FLASH_ALGO_OTP = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xE00ABE00, 
    0x4770ba40, 0x4770ba40, 0x4770ba40, 0x4770bac0, 0x4770bac0, 0x4770bac0, 0x0030ea4f, 0x00004770,
    0x0030ea4f, 0x00004770, 0x0030ea4f, 0x00004770, 0x49052000, 0x49057008, 0x20016008, 0x39264902,
    0x002af881, 0x00004770, 0x40054026, 0x40010418, 0x6800480d, 0x0001f000, 0x480cb118, 0x6008490c,
    0x480ce002, 0x6008490a, 0x490b2003, 0x480b6008, 0x6208490b, 0x490a2000, 0x7008312a, 0x49082005,
    0x0026f881, 0x00004770, 0x40010684, 0x33306381, 0x40054100, 0x33304f81, 0x40010418, 0x00116310,
    0x40054000, 0xf000b510, 0xbd10f83f, 0x4604b510, 0xf0004620, 0xbd10f83f, 0x49142000, 0xf44f6008,
    0x49133040, 0x20006008, 0x60081f09, 0x391c4910, 0x20016008, 0x7008490f, 0x490e480f, 0xf8c13926,
    0x20000100, 0x20016208, 0x1d09490a, 0x480b7008, 0x6008490b, 0x604812c0, 0x6108480a, 0x4025f44f,
    0x39264904, 0x03fef8a1, 0x00004770, 0x40010590, 0x4001041c, 0x40054026, 0x11101300, 0xfffffa0e,
    0x40048000, 0xa5a50000, 0xf000b510, 0x2000f925, 0x0000bd10, 0x4604b570, 0xf0002500, 0x2004f91d,
    0x60084915, 0x60202000, 0x1c6de007, 0x42854813, 0xf000d303, 0x2001f911, 0x480fbd70, 0x68001d00,
    0x7080f400, 0x7f80f5b0, 0xe007d1ef, 0x3008480a, 0xf0406800, 0x49080010, 0x60083108, 0x1d004806,
    0xf0006800, 0x28000010, 0x4903d1f0, 0xf0006008, 0x2000f8f3, 0x0000e7e0, 0x4001041c, 0x00061a80,
    0xf000b510, 0xf240f8e9, 0x49101023, 0xf2436008, 0x60082010, 0x30fff04f, 0x6008490d, 0x490b480d,
    0x60081d09, 0x600843c0, 0x4908480b, 0x60083118, 0x1d0912c0, 0xf24a6008, 0x49085001, 0xf7ff8008,
    0xf7ffff27, 0xf000ff35, 0xbd10f8c7, 0x40010400, 0x40010590, 0x01234567, 0x00080005, 0x400543fe,
    0x43f8e92d, 0x460c4605, 0xf6494616, 0x90004040, 0xf24046b0, 0x492b1003, 0x462f6008, 0x4040f649,
    0xbf009000, 0xf8a8f000, 0x0000f8d8, 0x20006038, 0xe00c9000, 0x1c409800, 0xf6499000, 0x98004140,
    0xd3044288, 0xf898f000, 0xe8bd2001, 0x481d83f8, 0x68001d00, 0x0010f000, 0xd1eb2810, 0x4819e007,
    0x68003008, 0x0010f040, 0x31084916, 0x48156008, 0x68001d00, 0x0010f000, 0xd0f02810, 0x0804f108,
    0x1f241d3f, 0xd2cd2c04, 0x490e2000, 0x90006008, 0x9800e00b, 0x90001c40, 0x4140f649, 0x42889800,
    0xf000d303, 0x2001f869, 0x4806e7cf, 0x68001d00, 0x7080f400, 0x7f80f5b0, 0xf000d1eb, 0x2000f85d,
    0x0000e7c3, 0x4001041c, 0x4604b570, 0x4616460d, 0xff66f7ff, 0xbd702000, 0x4604b570, 0x4616460d,
    0x46294632, 0xf7ff4620, 0xbd70ff8b, 0x49034802, 0x48036008, 0x47706008, 0xffff0123, 0x40049408,
    0xffff3210, 0x4604b510, 0xfed6f7ff, 0xbd102000, 0x4604b5f0, 0x2300460d, 0x27002600, 0x21004626,
    0xf856e007, 0x6810cb04, 0xd0004584, 0x1d12e004, 0xebb11c49, 0xd3f40f95, 0x4637bf00, 0xe0062300,
    0xcb01f817, 0x45845cd0, 0xe004d000, 0xf0051c5b, 0x42980003, 0xbf00d8f4, 0x0081eb04, 0xbdf04418,
    0x49034802, 0x48036088, 0x47706088, 0xffff0123, 0x40049000, 0xffff3210, 0x4807b500, 0xf4006800,
    0xb9083080, 0xf854f000, 0x68004803, 0x0001f000, 0xf000b908, 0xbd00f809, 0x40010680, 0x1e01bf00,
    0x0001f1a0, 0x4770d1fb, 0x481fb510, 0xb2826800, 0x6800481e, 0x0481f3c0, 0x6800481c, 0x2303f3c0,
    0x1192b90c, 0x2c01e008, 0x1292d101, 0x2c02e004, 0x1312d101, 0x1392e000, 0x2b0fb10b, 0xf7ffd102,
    0xe020ff85, 0x0001f003, 0xb9e2b118, 0xff7ef7ff, 0xf003e019, 0x28020002, 0x2a01d104, 0xf7ffd113,
    0xe010ff75, 0x0004f003, 0xd1042804, 0xd10a2a02, 0xff6cf7ff, 0xf003e007, 0x28080008, 0x2a03d103,
    0xf7ffd101, 0xbd10ff63, 0x40049404, 0x40010680, 0x4823b510, 0xb2826840, 0x68004822, 0x4481f3c0,
    0x68004820, 0x6303f3c0, 0x1192b90c, 0x2c01e008, 0x1292d101, 0x2c02e004, 0x1312d101, 0x1392e000,
    0x2001b90b, 0x2000e000, 0xd1012b0f, 0xe0002101, 0x43082100, 0xf7ffb110, 0xe020ff73, 0x0001f003,
    0xb9e2b118, 0xff6cf7ff, 0xf003e019, 0x28020002, 0x2a01d104, 0xf7ffd113, 0xe010ff63, 0x0004f003,
    0xd1042804, 0xd10a2a02, 0xff5af7ff, 0xf003e007, 0x28080008, 0x2a03d103, 0xf7ffd101, 0xbd10ff51,
    0x40049000, 0x40010680, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x200002cd,
    'pc_unInit': 0x20000309,
    'pc_program_page': 0x200002dd,
    'pc_erase_sector': 0x200000b1,
    'pc_eraseAll': 0x200000a9,

    'static_base' : 0x20000000 + 0x00000004 + 0x000004c8,
    'begin_stack' : 0x20000700,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x400,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001400],   # Enable double buffering
    'min_program_length' : 0x400,

    # Flash information
    'flash_start': 0x3000c00,
    'flash_size': 0x400,
    'sector_sizes': (
        (0x0, 0x400),
    )
}


class HC32F448xA(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x20000, page_size=0x200, sector_size=0x2000,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        FlashRegion( start=0x03000C00, length=0x400, page_size=0x400, sector_size=0x400,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_OTP),
        RamRegion(   start=0x1FFF8000, length=0x10000),
        RamRegion(   start=0x200F0000, length=0x1000)
        )

    def __init__(self, session):
        super(HC32F448xA, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32F448.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.STPCTL, DBGMCU.STPCTL_VALUE)
        self.write32(DBGMCU.STPCTL1, DBGMCU.STPCTL1_VALUE)
        self.write32(DBGMCU.TRACECTL, DBGMCU.TRACECTL_VALUE)


class HC32F448xC(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x40000, page_size=0x200, sector_size=0x2000,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        FlashRegion( start=0x03000C00, length=0x400, page_size=0x400, sector_size=0x400,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_OTP),
        RamRegion(   start=0x1FFF8000, length=0x10000),
        RamRegion(   start=0x200F0000, length=0x1000)
        )

    def __init__(self, session):
        super(HC32F448xC, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32F448.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.STPCTL, DBGMCU.STPCTL_VALUE)
        self.write32(DBGMCU.STPCTL1, DBGMCU.STPCTL1_VALUE)
        self.write32(DBGMCU.TRACECTL, DBGMCU.TRACECTL_VALUE)

