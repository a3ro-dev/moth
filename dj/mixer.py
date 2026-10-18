"""The console: turns per-deck buses into one record instead of oil and water.

bus = {(deck, "vox"|"beat"): (n,2) float32, ("fx","fx"): ...}. Steps, each the thing a mashup engineer does:
  1. vocal channel strip   high-pass 100 Hz (foreign low end and mud out of the acapella)
  2. vocal level match     a vocal over a foreign beat sits at the vocal/beat ratio it had on its own record
  3. carve                 the foreign beat dips 1-5 kHz under the vocal (dynamic EQ, sidechained), so it sits IN it
  4. shared room           both decks share one short reverb, so they sound recorded in the same space
  5. glue                  gentle bus compression over everything (~2 dB), so it breathes as one mix
Every knob lives in KNOBS so the learning loop can tune it from rewards.
"""
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import butter, fftconvolve, sosfilt, stft

SR = 44100
KNOBS = {"vox_hp": 100.0, "carve_db": 5.0, "room_send_vox": 0.12, "room_send_beat": 0.04, "room_rt": 0.7,
         "glue_ratio": 2.0, "glue_gr_db": 2.0, "match_max_db": 6.0, "spec_match_db": 6.0}


def rms_env(x, win=0.02):
    m = x.mean(axis=1) if x.ndim == 2 else x
    return np.sqrt(uniform_filter1d(m.astype(np.float64) ** 2, max(1, int(win * SR))) + 1e-12)


def band(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x, axis=0).astype(np.float32)


def follower(e, attack=0.005, release=0.12):
    """One-pole attack/release smoothing of an envelope (block-wise for speed)."""
    out = np.empty_like(e)
    a, r = np.exp(-1 / (attack * SR)), np.exp(-1 / (release * SR))
    y = 0.0
    step = 64
    for i in range(0, len(e), step):
        v = e[i:i + step].max()
        c = a if v > y else r
        y = c ** step * y + (1 - c ** step) * v
        out[i:i + step] = y
    return out


def room_ir(rt):
    n = int(rt * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(11)
    ir = rng.standard_normal((n, 2)) * np.exp(-6.9 * t / rt)[:, None]
    ir[: int(0.015 * SR)] = 0  # 15 ms pre-delay keeps the dry hit in front
    ir = sosfilt(butter(2, [250, 7000], "bandpass", fs=SR, output="sos"), ir, axis=0)
    return (ir / np.sqrt((ir ** 2).sum(axis=0))).astype(np.float32)


def native_ratio(deck):
    """dB of vocals over the rest of the stems on the deck's own record, where the vocal is active."""
    v = rms_env(np.asarray(deck.stem("vocals")), 0.4)
    b = rms_env(sum(np.asarray(deck.stem(s)) for s in ("drums", "bass", "other")), 0.4)
    on = v > 0.25 * v.max()
    return float(np.median(20 * np.log10(v[on] / b[on]))) if on.any() else 0.0


EDGES = np.geomspace(80, 12000, 25)  # 24 bands, ~0.3 oct each
CENTERS = np.sqrt(EDGES[:-1] * EDGES[1:])


def ltas(x, mask=None):
    """Long-term average spectrum in dB per EDGES band, over the frames where mask (sample-level bool) is True."""
    m = x.mean(axis=1) if x.ndim == 2 else x
    f, t, Z = stft(m, SR, nperseg=4096)
    p = np.abs(Z) ** 2
    if mask is not None:
        idx = np.clip((t * SR).astype(int), 0, len(mask) - 1)
        p = p[:, mask[idx]]
    if p.shape[1] == 0:
        return None
    p = p.mean(axis=1)
    return np.array([10 * np.log10(p[(f >= lo) & (f < hi)].mean() + 1e-12) for lo, hi in zip(EDGES[:-1], EDGES[1:])])


def shape_diff(native, foreign):
    """native - foreign tonal balance in dB per band, overall level removed (level is the match stage's job)."""
    d = native - foreign
    return d - np.median(d)


def timbre_pairs(decks, vox, beats):
    """{(vocal deck, foreign beat deck): (native LTAS, foreign LTAS)} measured where that vocal is active."""
    out = {}
    for d in vox:
        if not np.asarray(vox[d]).any():
            continue
        v = rms_env(np.asarray(decks[d].stem("vocals")), 0.4)
        native = ltas(sum(np.asarray(decks[d].stem(s)) for s in ("drums", "bass", "other")), v > 0.25 * v.max())
        ve = rms_env(vox[d], 0.4)
        on = ve > 0.25 * ve.max()
        for o in beats:
            if o == d or not np.asarray(beats[o]).any() or on.sum() < SR:
                continue
            foreign = ltas(beats[o], on)
            if native is not None and foreign is not None:
                out[(d, o)] = (native, foreign)
    return out


def timbre_gap(pairs):
    """Mean |tonal-balance difference| in dB between each vocal's native beat and the foreign beat under it."""
    g = [np.abs(shape_diff(n, f)).mean() for n, f in pairs.values()]
    return round(float(np.mean(g)), 2) if g else None


def eq_curve(x, gain_db):
    """Static zero-phase EQ: gain_db per CENTERS band (log-interpolated, held flat outside 80 Hz-12 kHz)."""
    X = np.fft.rfft(x, axis=0)
    g = np.interp(np.log(np.fft.rfftfreq(len(x), 1 / SR) + 1e-9), np.log(CENTERS), gain_db)
    return np.fft.irfft(X * (10 ** (g / 20))[:, None], n=len(x), axis=0).astype(np.float32)


def spectral_match(decks, vox, beats, k, report):
    """Reshape each foreign beat toward the tonal balance of the beat the vocal was recorded over (reference matching)."""
    pairs = timbre_pairs(decks, vox, beats)
    report["timbre_raw_db"] = timbre_gap(pairs)
    for o in beats:
        cs = [uniform_filter1d(shape_diff(n, f), 3, mode="nearest") for (d, oo), (n, f) in pairs.items() if oo == o]
        if cs:
            beats[o] = eq_curve(beats[o], np.clip(np.mean(cs, axis=0), -k["spec_match_db"], k["spec_match_db"]))
    report["timbre_mismatch_db"] = timbre_gap(timbre_pairs(decks, vox, beats))


def mixer(bus, decks, beat, k=KNOBS, report=None):
    report = {} if report is None else report
    L = len(next(iter(bus.values())))
    keys = [d for d in decks]
    hp = butter(2, k["vox_hp"], "highpass", fs=SR, output="sos")
    vox = {d: sosfilt(hp, bus[(d, "vox")], axis=0).astype(np.float32) for d in keys}
    beats = {d: bus[(d, "beat")] for d in keys}

    # 2. vocal level match over foreign beats
    for d in keys:
        foreign = sum(beats[o] for o in keys if o != d) if len(keys) > 1 else None
        if foreign is None or not vox[d].any():
            continue
        ve, fe = rms_env(vox[d], 0.4), rms_env(foreign, 0.4)
        both = (ve > 0.25 * ve.max()) & (fe > 0.1 * fe.max()) if fe.max() > 0 else np.zeros(L, bool)
        if both.sum() < SR:  # less than a second of overlap: nothing to match
            continue
        now = float(np.median(20 * np.log10(ve[both] / fe[both])))
        want = native_ratio(decks[d])
        g = float(np.clip(want - now, -k["match_max_db"], k["match_max_db"]))
        vox[d] *= 10 ** (g / 20)
        report[f"vox_gain_{d}"] = round(g, 1)

    # 2b. spectral match: foreign beat takes on the tonal balance of the vocal's native beat
    if len(keys) > 1 and k["spec_match_db"] > 0:
        spectral_match(decks, vox, beats, k, report)

    # 3. carve: each beat dips 1-5 kHz under the OTHER decks' vocals
    for d in keys:
        other_vox = sum(vox[o] for o in keys if o != d) if len(keys) > 1 else None
        if other_vox is None or not other_vox.any() or not beats[d].any():
            continue
        ve = follower(rms_env(other_vox, 0.01))
        act = np.clip(ve / (np.percentile(ve[ve > 1e-5], 90) + 1e-9), 0, 1) if (ve > 1e-5).any() else ve * 0
        dip = 1 - (1 - 10 ** (-k["carve_db"] / 20)) * act
        b = band(beats[d], 1000, 5000)
        beats[d] = (beats[d] - b * (1 - dip)[:, None]).astype(np.float32)

    dry = sum(vox.values()) + sum(beats.values()) + bus[("fx", "fx")]
    # 4. shared room
    send = sum(vox.values()) * k["room_send_vox"] + sum(beats.values()) * k["room_send_beat"]
    wet = fftconvolve(send, room_ir(k["room_rt"]), axes=0)[:L].astype(np.float32)
    mix = dry + wet
    # 5. glue: RMS bus compressor, threshold set so the loud parts get ~glue_gr_db of gain reduction
    e = 20 * np.log10(follower(rms_env(mix, 0.01), 0.01, 0.2) + 1e-9)
    live = e > e.max() - 40
    if live.any():
        thr = np.percentile(e[live], 50)
        over = np.maximum(0, e - thr)
        gr = over * (1 - 1 / k["glue_ratio"])
        gr = np.minimum(gr, k["glue_gr_db"] * 2)
        mix = mix * (10 ** (-gr / 20))[:, None].astype(np.float32)
        report["glue_gr_db"] = round(float(np.percentile(gr[live], 90)), 1)
    return mix.astype(np.float32)
