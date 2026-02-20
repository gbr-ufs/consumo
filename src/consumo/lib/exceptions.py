# SPDX-License-Identifier: GPL-3.0-or-later


class ConsumoError(Exception):
    pass


class MissingMetadataError(ConsumoError):
    pass
