package main

import (
	"fmt"

	"github.com/go-vgo/robotgo"
)

func main() {
	fmt.Println("Press 'Ctrl + C' to exit.")

	for {
		if robotgo.AddEvents("ctrl") {
			fmt.Println("Ctrl key pressed")
			// Perform actions based on the detected key, for example:
			// robotgo.KeyTap("a")
		}

		// Add more key events as needed, for example:
		// if robotgo.AddEvents("shift") {
		//     fmt.Println("Shift key pressed")
		//     // Perform actions based on the detected key
		// }

		// Sleep for a short duration to reduce CPU usage
		robotgo.MilliSleep(100)
	}
}
