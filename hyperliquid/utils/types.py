from __future__ import annotations

import sys

if sys.version_info >= (3, 8):
    from typing import Literal, TypedDict
    from typing_extensions import NotRequired
else:
    from typing_extensions import TypedDict, Literal, NotRequired

from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union, cast

Any = Any
Option = Optional
cast = cast
Callable = Callable
NamedTuple = NamedTuple
NotRequired = NotRequired

AssetInfo = TypedDict("AssetInfo", {"name": str, "szDecimals": int})
Meta = TypedDict("Meta", {"universe": List[AssetInfo]})
Side = Union[Literal["A"], Literal["B"]]
SIDES: List[Side] = ["A", "B"]

SpotAssetInfo = TypedDict("SpotAssetInfo", {"name": str, "tokens": List[int], "index": int, "isCanonical": bool})
SpotTokenInfo = TypedDict(
    "SpotTokenInfo",
    {"name": str, "szDecimals": int, "weiDecimals": int, "index": int, "tokenId": str, "isCanonical": bool},
)
SpotMeta = TypedDict("SpotMeta", {"universe": List[SpotAssetInfo], "tokens": List[SpotTokenInfo]})
SpotAssetCtx = TypedDict(
    "SpotAssetCtx",
    {"dayNtlVlm": str, "markPx": str, "midPx": Optional[str], "prevDayPx": str, "circulatingSupply": str, "coin": str},
)
SpotMetaAndAssetCtxs = Tuple[SpotMeta, List[SpotAssetCtx]]

AllMidsSubscription = TypedDict("AllMidsSubscription", {"type": Literal["allMids"]})
L2BookSubscription = TypedDict("L2BookSubscription", {"type": Literal["l2Book"], "coin": str})
TradesSubscription = TypedDict("TradesSubscription", {"type": Literal["trades"], "coin": str})
UserEventsSubscription = TypedDict("UserEventsSubscription", {"type": Literal["userEvents"], "user": str})
UserNonFundingLedgerUpdatesSubscription = TypedDict(
    "UserNonFundingLedgerUpdatesSubscription", {"type": Literal["userNonFundingLedgerUpdates"], "user": str}
)
Subscription = Union[
    AllMidsSubscription,
    L2BookSubscription,
    TradesSubscription,
    UserEventsSubscription,
    UserNonFundingLedgerUpdatesSubscription,
]

AllMidsData = TypedDict("AllMidsData", {"mids": Dict[str, str]})
AllMidsMsg = TypedDict("AllMidsMsg", {"channel": Literal["allMids"], "data": AllMidsData})
L2Level = TypedDict("L2Level", {"px": str, "sz": str, "n": int})
L2BookData = TypedDict("L2BookData", {"coin": str, "levels": Tuple[List[L2Level]], "time": int})
L2BookMsg = TypedDict("L2BookMsg", {"channel": Literal["l2Book"], "data": L2BookData})
PongMsg = TypedDict("PongMsg", {"channel": Literal["pong"]})
Trade = TypedDict("Trade", {"coin": str, "side": Side, "px": str, "sz": int, "hash": str, "time": int})
TradesMsg = TypedDict("TradesMsg", {"channel": Literal["trades"], "data": List[Trade]})
Fill = TypedDict(
    "Fill",
    {
        "coin": str,
        "px": str,
        "sz": str,
        "side": Side,
        "time": int,
        "startPosition": str,
        "dir": str,
        "closedPnl": str,
        "hash": str,
        "oid": int,
        "crossed": bool,
    },
)
# TODO: handle other types of user events
UserEventsData = TypedDict("UserEventsData", {"fills": List[Fill]}, total=False)
UserEventsMsg = TypedDict("UserEventsMsg", {"channel": Literal["user"], "data": UserEventsData})

"""
userNonFundingLedgerUpdates WebSocket messages

Docs: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions
"""


class DepositDelta(TypedDict):
    type: Literal["deposit"]
    usdc: str


class WithdrawDelta(TypedDict):
    type: Literal["withdraw"]
    fee: str
    nonce: int
    usdc: str


class SpotTransferDelta(TypedDict):
    type: Literal["spotTransfer"]
    token: str
    amount: str
    usdcValue: str
    user: str
    destination: str
    fee: str


class SpotGenesisDelta(TypedDict):
    type: Literal["spotGenesis"]
    token: str
    amount: str


class InternalTransferDelta(TypedDict):
    type: Literal["internalTransfer"]
    destination: str
    fee: str
    usdc: str
    user: str


class AccountClassTransferDelta(TypedDict):
    type: Literal["accountClassTransfer"]
    toPerp: bool
    usdc: str


class VaultDelta(TypedDict):
    type: Union[Literal["vaultCreate"], Literal["vaultDeposit"], Literal["vaultDistribution"]]
    usdc: str
    vault: str


class VaultWithdrawDelta(TypedDict):
    type: Literal["vaultWithdraw"]
    basis: str
    closingCost: str
    commission: str
    netWithdrawnUsd: str
    requestedUsd: str
    user: str
    vault: str


class LiquidatedPosition(TypedDict):
    coin: str
    szi: str


class LiquidationDelta(TypedDict):
    type: Literal["liquidation"]
    accountValue: str
    leverageType: Union[Literal["Cross"], Literal["Isolated"]]
    liquidatedNtlPos: str
    liquidatedPositions: List[LiquidatedPosition]


class NonFundingLedgerUpdate(TypedDict):
    time: int
    hash: str
    delta: Union[
        DepositDelta,
        WithdrawDelta,
        SpotTransferDelta,
        SpotGenesisDelta,
        InternalTransferDelta,
        AccountClassTransferDelta,
        VaultDelta,
        VaultWithdrawDelta,
        LiquidationDelta,
    ]


class UserNonFundingLedgerUpdatesData(TypedDict):
    user: str
    nonFundingLedgerUpdates: List[NonFundingLedgerUpdate]


class UserNonFundingLedgerUpdatesMsg(TypedDict):
    channel: Literal["userNonFundingLedgerUpdates"]
    data: UserNonFundingLedgerUpdatesData


WsMsg = Union[AllMidsMsg, L2BookMsg, TradesMsg, UserEventsMsg, UserNonFundingLedgerUpdatesMsg, PongMsg]


class Cloid:
    def __init__(self, raw_cloid: str):
        self._raw_cloid: str = raw_cloid
        self._validate()

    def _validate(self):
        assert self._raw_cloid[:2] == "0x", "cloid is not a hex string"
        assert len(self._raw_cloid[2:]) == 32, "cloid is not 16 bytes"

    @staticmethod
    def from_int(cloid: int) -> Cloid:
        return Cloid(f"{cloid:#034x}")

    @staticmethod
    def from_str(cloid: str) -> Cloid:
        return Cloid(cloid)

    def to_raw(self):
        return self._raw_cloid
