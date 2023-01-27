package filler

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"neo4j/domain"
	"net/http"
	"os"

	"github.com/neo4j/neo4j-go-driver/neo4j"
)

func addGroups(client neo4j.Driver) {
	response, err := http.Get(fmt.Sprintf("http://postgres-ma:%s/api/groups", os.Getenv("LOCAL_SERVICES_PORT")))

	if err != nil {
		log.Fatal(err)
	}

	responseBody, err := ioutil.ReadAll(response.Body)

	if err != nil {
		log.Fatal(err)
	}

	var groupList []domain.Group

	err = json.Unmarshal(responseBody, &groupList)

	if err != nil {
		log.Fatal(err)
	}

	session, err := client.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})

	if err != nil {
		log.Fatal(err)
	}

	defer session.Close()

	log.Println(groupList)

	for _, group := range groupList {

		_, err = session.WriteTransaction(func(tx neo4j.Transaction) (interface{}, error) {
			result, err := tx.Run(`
			CREATE (g:Group {id: $id, specialityId: $specialityId})
			WITH g
			MATCH
			(s:Student {groupId: $id})
			CREATE (s)-[:member_of]->(g)
			`, map[string]interface{}{"id": group.Id, "specialityId": group.SpecialityId})

			if err != nil {
				log.Fatal(err)
			}

			return result.Consume()
		})

		if err != nil {
			log.Fatal(err)
		}
	}
}
