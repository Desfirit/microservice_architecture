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

func addStudents(client neo4j.Driver) {
	response, err := http.Get(fmt.Sprintf("http://postgres-ma:%s/api/students", os.Getenv("LOCAL_SERVICES_PORT")))

	if err != nil {
		log.Fatal(err)
	}

	responseBody, err := ioutil.ReadAll(response.Body)

	if err != nil {
		log.Fatal(err)
	}

	var studentList []domain.Student

	err = json.Unmarshal(responseBody, &studentList)

	if err != nil {
		log.Fatal(err)
	}

	session, err := client.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})

	if err != nil {
		log.Fatal(err)
	}

	defer session.Close()

	for _, student := range studentList {

		_, err = session.WriteTransaction(func(tx neo4j.Transaction) (interface{}, error) {
			result, err := tx.Run("CREATE (a:Student {id: $id, groupId: $groupId})",
				map[string]interface{}{"id": student.Id, "groupId": student.GroupId})

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
