package router

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/go-chi/chi"
	"github.com/neo4j/neo4j-go-driver/neo4j"
)

func applyRoutes(r *chi.Mux, client neo4j.Driver) {
	r.Get("/api/students", getStudentInfoHandler(client))
}

func getStudentInfoHandler(client neo4j.Driver) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		students := r.URL.Query().Get("students")

		if len(students) == 0 {
			w.WriteHeader(400)
			w.Write([]byte("Missing required query parameter student_id"))
		}

		studentList := strings.Split(students, ",")

		session, err := client.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeRead})

		if err != nil {
			log.Fatal(err)
		}

		defer session.Close()

		var studentsJsonFromNeo [][]string

		for _, studentId := range studentList {
			studentJson, err := session.ReadTransaction(func(tx neo4j.Transaction) (interface{}, error) {
				log.Println("started transaction")

				var resultContainer []string

				r, err := tx.Run(`
			MATCH
				(s:Student {id: $studentId})-[:member_of]->(g:Group)-[:takes_part_in]->(p:Speciality)-[:belongs_to]->(d:Department)-[:belongs_to]->(i:Institute)
			RETURN apoc.convert.toJson({
				student_id: s.id,
				group_name: g.id,
				speciality: p.name,
				department: d.name,
				institute: i.name
			})
			`,
					map[string]interface{}{"studentId": studentId})

				log.Println("ran transaction")

				if err != nil {
					log.Fatal(err)
				}

				for r.Next() {
					resultContainer = append(resultContainer, r.Record().Values()[0].(string))
				}

				return resultContainer, nil
			})

			log.Println("got result")

			if err != nil {
				log.Fatal(err)
			}

			st, ok := studentJson.([]string)

			if !ok {
				log.Fatal("could not convert studentInfo to string array")
			}

			studentsJsonFromNeo = append(studentsJsonFromNeo, st)
		}

		type resultStruct struct {
			StudentId      string `json:"student_id"`
			GroupName      string `json:"group_name"`
			SpecialityName string `json:"speciality"`
			DepartmentName string `json:"department"`
			InstituteName  string `json:"institute"`
			Course         string `json:"course"`
		}

		unmarshalledArray := []resultStruct{}

		log.Print(studentsJsonFromNeo)

		for _, res := range studentsJsonFromNeo {
			log.Println("res", res)

			var rs resultStruct
			err = json.Unmarshal([]byte(fmt.Sprintf("%v", res[0])), &rs)

			if err != nil {
				log.Fatal(err)
			}

			unmarshalledArray = append(unmarshalledArray, rs)
		}

		log.Println("finished unmarshalling")

		stringifiedResult, err := json.Marshal(unmarshalledArray)

		if err != nil {
			w.WriteHeader(500)
			w.Write([]byte{})
			log.Fatal(err)
		}

		w.WriteHeader(200)
		w.Write(stringifiedResult)
	}
}
