%{
foo
%}

\header{
  title = "TITLE"
}

va = {
  
%%%CONTENT-GOES-HERE%%%

}

music = \new StaffGroup <<
      \new Staff {
\set Staff.midiInstrument = "piano"
\set Staff.instrumentName = #"Vc 1"
\transpose c c { \va }
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
