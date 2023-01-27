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

func addMongoDbData(client neo4j.Driver) {
	response, err := http.Get(fmt.Sprintf("http://mongo-ma:%s/api/all", os.Getenv("LOCAL_SERVICES_PORT")))

	if err != nil {
		log.Fatal(err)
	}

	responseBody, err := ioutil.ReadAll(response.Body)

	if err != nil {
		log.Fatal(err)
	}

	var instituteList []domain.Institute

	err = json.Unmarshal(responseBody, &instituteList)

	if err != nil {
		log.Fatal(err)
	}

	courseGroupMap := getCourseGroupList()

	log.Printf("courseGroupMap: %+v", courseGroupMap)

	session, err := client.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})

	if err != nil {
		log.Fatal(err)
	}

	defer session.Close()

	for _, institute := range instituteList {
		_, err = session.WriteTransaction(func(tx neo4j.Transaction) (interface{}, error) {
			result, err := tx.Run(`
			CREATE (i:Institute {name: $name})
			`,
				map[string]interface{}{"name": institute.Name})

			if err != nil {
				log.Fatal(err)
			}

			for _, department := range institute.Department {
				_, err := tx.Run(`
					CREATE (d:Department {name: $name})
					WITH d
					MATCH
					(i:Institute {name: $instituteName})
					CREATE (d)-[:belongs_to]->(i)
					`,
					map[string]interface{}{"name": department.Name, "instituteName": institute.Name})

				if err != nil {
					log.Fatal(err)
				}

				for _, speciality := range department.Speciality {
					_, err := tx.Run(`
							CREATE (s:Speciality {name: $name})
							WITH s
							MATCH
							(d:Department {name: $departmentName}),
							(g: Group {specialityId: $name})
							CREATE (g)-[:takes_part_in]->(s), (s)-[:belongs_to]->(d)
							`,
						map[string]interface{}{"name": speciality.Name, "departmentName": department.Name})

					if err != nil {
						log.Fatal(err)
					}

				}

				for _, course := range department.Course {
					_, err := tx.Run(`
							CREATE (c:Course {name: $name})
							`,
						map[string]interface{}{"name": course.Name})

					if err != nil {
						log.Fatal(err)
					}

					for _, group := range courseGroupMap[course.Name] {
						_, err := tx.Run(`
								MATCH
								(c:Course {name: $name}),
								(s:Student)-[:member_of]->(:Group {id: $groupId})
								CREATE (s)-[:studying]->(c)
								`,
							map[string]interface{}{"name": course.Name, "groupId": group})

						if err != nil {
							log.Fatal(err)
						}

						if err != nil {
							log.Fatal(err)
						}
					}
				}
			}

			return result, nil
		})

	}

	if err != nil {
		log.Fatal(err)
	}
}

func getCourseGroupList() map[string][]string {
	groupCourse, err := http.Get(fmt.Sprintf("http://postgres-ma:%s/api/courses", os.Getenv("LOCAL_SERVICES_PORT")))

	if err != nil {
		log.Fatal(err)
	}

	groupCourseBody, err := ioutil.ReadAll(groupCourse.Body)

	if err != nil {
		log.Fatal(err)
	}

	var GroupCourseList []struct {
		Groups []string `json:"groups"`
		Course string   `json:"name"`
	}

	err = json.Unmarshal(groupCourseBody, &GroupCourseList)

	if err != nil {
		log.Fatal(err)
	}

	result := map[string][]string{}

	for _, item := range GroupCourseList {
		result[item.Course] = item.Groups
	}

	return result
}
