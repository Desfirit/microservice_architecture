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

func addLessonDescriptions(client neo4j.Driver) {
	response, err := http.Get(fmt.Sprintf("http://elastic-ma:%s/api/lessons", os.Getenv("LOCAL_SERVICES_PORT")))

	if err != nil {
		log.Fatal(err)
	}

	responseBody, err := ioutil.ReadAll(response.Body)

	if err != nil {
		log.Fatal(err)
	}

	var lessonDescriptionList []domain.LessonDescription

	err = json.Unmarshal(responseBody, &lessonDescriptionList)

	if err != nil {
		log.Fatal(err)
	}

	session, err := client.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})

	if err != nil {
		log.Fatal(err)
	}

	defer session.Close()

	for _, lessonDescription := range lessonDescriptionList {

		_, err = session.WriteTransaction(func(tx neo4j.Transaction) (interface{}, error) {
			result, err := tx.Run(`
			CREATE (ld:LessonDescription {name: $name})
			WITH ld
			MATCH
			(l:Lesson {id: $name})
			CREATE (ld)-[:part_of]->(l)
			`, map[string]interface{}{
				"name":      lessonDescription.Id,
				"materials": lessonDescription.Materials,
				"equipment": lessonDescription.Equipment})

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
