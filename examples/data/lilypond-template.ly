%{
	foo
%}

\header{
	title = "TITLE"
}

va = {
%%%CONTENT-GOES-HERE%%%
}

% a list of instrument names can be found in
% in the lilypond source code in
% lilypond/scm/midi.scm

music = \new StaffGroup <<
	\new Staff {
		\set Staff.midiInstrument = "cello"
		\set Staff.instrumentName = "cello"
		\transpose c c' { \va }
	}

	\new Staff {
		\set Staff.midiInstrument = "acoustic grand"
		\set Staff.instrumentName = "piano"
		\transpose c c' { \va }
	}

%{
	\new Staff {
		\set Staff.midiInstrument = "acoustic guitar (nylon)"
		\set Staff.instrumentName = "guitar"
		\transpose c c' { \va }
	}
%}

	\new Staff {
		\set Staff.midiInstrument = "flute"
		\set Staff.instrumentName = "flute"
		\transpose c c' { \va }
	}
>>

\book {
	\score {
		\music
		\layout {}
	}

	\score {
		\unfoldRepeats \music
		\midi {
			\context {
				\Score
				tempoWholesPerMinute = #(ly:make-moment 120 4)
			}
		}
	}
}

\version "2.16.0"  % necessary for upgrading to future LilyPond versions.
