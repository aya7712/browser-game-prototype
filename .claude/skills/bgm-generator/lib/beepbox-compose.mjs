// Tiny helper library for authoring BeepBox songs as JSON, consumed by the
// beepbox render-wav CLI (~/workspace/beepbox/cli/render-wav.mjs).
//
// Import from a per-track script in the project's scripts/ directory:
//
//   import { m, note, channel, buildSong, printSong, barTicks }
//     from "../.claude/skills/bgm-generator/lib/beepbox-compose.mjs";
//
// Pitch model: pitches are ABSOLUTE; the synth adds the key's basePitch.
// ALWAYS use key "C" (basePitch 12) so that m(midi) = midi - 12 holds, and
// change the tonal centre by moving MIDI numbers instead of the key.

export const DEFAULT_TICKS_PER_BEAT = 4;

// MIDI note number -> BeepBox absolute pitch value (assumes key "C").
//   C4 = 60 -> 48,  A4 = 69 -> 57,  C2 = 36 -> 24
export const m = (midi) => midi - 12;

// Ticks in one bar for the given meter. A note's tick positions run 0..barTicks.
export const barTicks = (beatsPerBar, ticksPerBeat) => beatsPerBar * ticksPerBeat;

// One note. `midis` is a single MIDI number or an array (a chord). The note
// runs from tick `a` to tick `b`; `volume` is 0..100 (mapped to 0..3 loudness).
// Within a single channel, notes must NOT overlap in time — use a chord (array)
// for simultaneous pitches.
export function note(midis, a, b, volume = 100) {
	const arr = Array.isArray(midis) ? midis : [midis];
	return {
		pitches: arr.map(m),
		points: [
			{ tick: a, pitchBend: 0, volume },
			{ tick: b, pitchBend: 0, volume },
		],
	};
}

// A pitch channel. `bars` is an array of bars; each bar is an array of notes.
// `octaveScrollBar` only affects how the song looks in the BeepBox editor
// (playback uses the absolute MIDI pitches), so pick a value near the register.
export function channel(octaveScrollBar, instrument, bars) {
	return {
		type: "pitch",
		octaveScrollBar,
		instruments: [instrument],
		patterns: bars.map((notes) => ({ notes })),
		sequence: bars.map((_, i) => i + 1), // 1-based pattern per bar (0 = empty)
	};
}

// Assemble the full song object. For seamless game-loop BGM keep introBars 0 so
// the whole file is the loop (the engine repeats the file end-to-start).
export function buildSong({
	key = "C",
	scale = "normal :)",
	beatsPerBar = 4,
	ticksPerBeat = DEFAULT_TICKS_PER_BEAT,
	tempo = 90,
	introBars = 0,
	loopBars,
	channels,
}) {
	return {
		format: "BeepBox",
		version: 9,
		scale,
		key,
		introBars,
		loopBars: loopBars ?? channels[0].sequence.length,
		beatsPerBar,
		ticksPerBeat,
		beatsPerMinute: tempo,
		layeredInstruments: false,
		patternInstruments: false,
		channels,
	};
}

export function printSong(song) {
	process.stdout.write(JSON.stringify(song));
}
