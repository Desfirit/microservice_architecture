package main

import (
	"fmt"
	"gateway/router"
	"log"
	"net/http"
	"os"
)

func main() {
	r := router.NewRouter()

	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", os.Getenv("LOCAL_SERVICES_PORT")), r))
}
