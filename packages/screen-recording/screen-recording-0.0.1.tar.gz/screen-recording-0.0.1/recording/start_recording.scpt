tell application "QuickTime Player"
	activate
	set newScreenRecording to new screen recording
	my putInMenuBar()
	tell newScreenRecording
		start
	end tell

end tell

on putInMenuBar()
	delay 1
	tell application "System Events"
		tell process "QuickTime Player"
			set frontmost to true
			key code 49
		end tell
	end tell
end putInMenuBar