package main

import (
	"fmt"
	"log"
	"neo4j/filler"
	"neo4j/repository"
	"neo4j/router"
	"net/http"
	"os"

	"github.com/neo4j/neo4j-go-driver/neo4j"
)

func main() {
	client := repository.NewClient()
	defer client.Close()

	session, err := client.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})

	if err != nil {
		log.Fatal(err)
	}

	defer session.Close()

	if err != nil {
		log.Fatal(err)
	}

	filler.FillInNeo(client)

	log.Println("filled in database")

	r := router.NewRouter(client)

	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", os.Getenv("LOCAL_SERVICES_PORT")), r))
}
