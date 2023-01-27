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

func addLessons(client neo4j.Driver) {
	response, err := http.Get(fmt.Sprintf("http://postgres-ma:%s/api/lessons", os.Getenv("LOCAL_SERVICES_PORT")))

	if err != nil {
		log.Fatal(err)
	}

	responseBody, err := ioutil.ReadAll(response.Body)

	if err != nil {
		log.Fatal(err)
	}

	var lessonList []domain.Lesson

	err = json.Unmarshal(responseBody, &lessonList)

	if err != nil {
		log.Fatal(err)
	}

	session, err := client.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})

	if err != nil {
		log.Fatal(err)
	}

	defer session.Close()

	for _, lesson := range lessonList {

		_, err = session.WriteTransaction(func(tx neo4j.Transaction) (interface{}, error) {
			result, err := tx.Run("CREATE (a:Lesson {id: $id})", map[string]interface{}{"id": lesson.Id})

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
