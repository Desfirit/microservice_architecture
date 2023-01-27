package repository

import (
	"log"
	"os"

	"github.com/neo4j/neo4j-go-driver/neo4j"
)

func NewClient() neo4j.Driver {
	client, err := neo4j.NewDriver("bolt://neo4j:7687", neo4j.BasicAuth(os.Getenv("NEO4J_USER"), os.Getenv("NEO4J_PASS"), ""), func(c *neo4j.Config) { c.Encrypted = false })

	if err != nil {
		log.Fatal("Could not create client neo4j client")
	}

	return client
}
