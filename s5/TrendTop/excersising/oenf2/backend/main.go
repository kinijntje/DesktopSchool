package main

import (
	"fmt"
	"net/http"

	"D:/Documenten/ASchoel/s5/TrendTop/oenf2/backend/pkg/websocket"
)

func setupRoutes() {
	pool := websocket.NewPool()
}

func main() {
	fmt.Println("Full stack chat project")
	setupRoutes()
	http.ListenAndServe(":9000", nil)
}
