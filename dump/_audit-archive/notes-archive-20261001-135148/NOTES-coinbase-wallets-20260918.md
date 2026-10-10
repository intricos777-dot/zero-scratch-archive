# HAULT NOTE — Coinbase wallet-address quest (2026-09-18, paused)

## The quest
Use the CDP API key (`~/Desktop/games/cdp_api_key.json`, already in `.env` as
COINBASE_API_KEY / COINBASE_API_SECRET) to pull every public wallet address of the
Coinbase account, so the bot's `CoinbaseSink` can sweep profits back INTO the account.

## What is DONE (verified)
- Full wallet inventory pulled via `GET /api/v3/brokerage/accounts` (paginated):
  **70 wallets**, saved to `coinbase-wallets.json` (repository-ignored, .gitignore patched).
- Notable holdings: SHIB Vault ~1,052,620 SHIB available; POL 0.0076, ATOM 0.0041,
  XTZ 0.0023, AVAX/DOT dust; all other wallets empty. No staking/locked assets.
- The CDP key scope is confirmed working for: brokerage accounts, orders, convert
  (submitConvertQuote / commitConvertTrade), trading.

## The GATE (why addresses are not pulled yet)
- `GET /api/v3/brokerage/wallets`            -> HTTP 401 Unauthorized
- `POST /api/v3/brokerage/wallets/{id}/deposit_address` -> HTTP 401 Unauthorized
- `https://api.cdp.coinbase.com/v1/accounts|wallets`    -> HTTP 404

=> The CDP org key lacks the retail **Wallets** scope on the v3 brokerage API.

## Additional landmine (pre-existing, still open)
- `coinbase-api` v1.1.12's `CBAdvancedTradeClient` ships NEITHER `getDepositAddress`
  NOR `withdraw` (endpoints list has no /withdrawals). The sink
  (`src/sinks/coinbase.ts` `sendToWallet()`) calls both -> sweep path is phantom until
  the SDK is upgraded and/or the sink is rewired.
- `COINBASE_WALLET_ID` (.env) is DEAD config — no code reads it; never needed.
- `FAUCETS_SWAP_TARGET` default = "LTC", but no LTC address knob exists; as-is, sweeps
  would break. Convert-to-ETH/BTC route works (convert endpoints exist).
- `COINBASE_WALLET_ID` empty + no `ETH_WALLET_ADDRESS` / `BTC_WALLET_ADDRESS` -> sink
  today would throw.

## Strategy shift — SHIB stacking (2026-09-18)
- FAUCETS_SWAP_TARGET: LTC → **SHIB** (user: stack SHIB in Coinbase vault)
- Sink rewired: when asset === swapTarget, skip withdraw entirely — just log "stacking"
- Convert failures handled gracefully: try convert, on failure fall back to stacking original asset
- CDP convert endpoint only supports USDC-USD/EURC-EUR pairs → most assets can't convert to SHIB via API
- No ETH/BTC wallets exist on this Coinbase account (70 wallets, all altcoins)
- Door 2 (ETH_WALLET_ADDRESS/BTC_WALLET_ADDRESS): impossible — no ETH/BTC wallets
- Door 3 (API auto-deposit): blocked — CDP key lacks Wallets scope (403)
- Current strategy: convert to SHIB where possible, stack whatever arrives in Coinbase vault
- To unlock full sweep: grant Wallets scope on CDP key + create ETH/BTC wallets

## Addendum 2026-09-18 (evening) — fleet rewire (open-code session, in aid of Hermes)
- SDK elevated `coinbase-api ^1.1.12 -> ^1.2.6` (by Hermes) — but that version ships NO
  `getDepositAddress`/`withdraw` helpers on CBAdvancedTradeClient (those belong to the
  PRIME client). Confirmed against dist/cjs typings.
- FLEET REWIRED `src/sinks/coinbase.ts` onto the raw BaseRestClient verbs:
    * deposit: `POST /api/v3/brokerage/accounts/{uuid}/deposit_addresses` (empty body) —
      minted per-asset from the accounts list resolved at runtime
    * withdraw: `POST /api/v3/brokerage/withdrawals/crypto`
    * ETH/BTC_WALLET_ADDRESS still take priority when set; network map extended (SHIB,
      POL, ATOM, XTZ, AVAX, DOT).
- `getAccounts()` envelope normalized (array | {body|data|accounts}) — both the sink and
  `checkBalance`.
- `COINBASE_WALLET_ID` == DEAD CONFIG (read into config.walletId, zero consumers). .env
  value stays EMPTY. TODO item reclassified accordingly.
- REMAINING RISK (runtime, not code): the CDP key may lack the Wallets/"Withdraw" scope —
  minting deposit addresses and withdrawals will surface 401 at sweep time. Hermes'
  parallel v2 `deposit-destinations` probes (test-cdp-v2.js etc.) may open that door;
  Scope grant in the CDP console or user-pasted Receive addresses are the fallback.
- Push decision: USER AUTHORIZED private push 2026-09-18 evening.