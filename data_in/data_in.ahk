pageNumber := 1

HexToDec(hex) {
    dec := 0
    VarSetStrCapacity(&dec, 66)
    , val := DllCall("msvcrt.dll\_wcstoui64", "Str", hex, "UInt", 0, "UInt", 16, "CDECL Int64")
    , DllCall("msvcrt.dll\_i64tow", "Int64", val, "Str", dec, "UInt", 10, "CDECL")
    return dec
}

text := FileRead("page_sequence.txt")
nibbleValue := 0

`:: {
    Global pageNumber
    Loop Parse SubStr(text, 1, 8) {
        WriteNibble(HexToDec(A_LoopField), &pageNumber)
    }
}


WriteNibble(value, &pageNumber) {
    sleepTime := 200
    If (value = 0) {
        Send "{PgDn}"
        ; Take the book off the lectern
        Send "{Enter}"
        PreciseSleep(100)

        ; Place the book back on the lectern
        Send "{RButton}"

        ; Edit the book
        Send "{RButton}"
        PreciseSleep(100)

        ; Navigate to the "Take Book" button
        Send "{Tab}"
        Send "{Tab}"
        pageNumber := 1

    } Else {
        offset := value - pageNumber

        If (offset = 0) {
            ; Flip the page back and forth to update the observer
            If (value = 15) {
                Send "{PgUp}"
                Send "{PgDn}"
            } Else {
                Send "{PgDn}"
                Send "{PgUp}"
            }
            
        } Else If (offset > 0) {
            Loop offset
                Send "{PgDn}"
        } Else {
            Loop -offset
                Send "{PgUp}"
        }
        pageNumber := value
        PreciseSleep(200)
    }
}

PreciseSleep(milliseconds) {
    DllCall("Winmm\timeBeginPeriod", "UInt", 3)  ; Affects all applications, not just this script's DllCall("Sleep"...), but does not affect SetTimer.
    DllCall("Sleep", "UInt", milliseconds)
    DllCall("Winmm\timeEndPeriod", "UInt", 3)  ; Should be called to restore system to normal.
}
