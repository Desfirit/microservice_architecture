package filler

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"redis/domain"

	"github.com/redis/go-redis/v9"
)

func FillInDB(rdb *redis.Client) {
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

	ctx := context.Background()

	for _, student := range studentList {
		marshalledStudent, err := json.Marshal(student)

		if err != nil {
			log.Fatal(err)
		}

		command := rdb.Set(ctx, student.StudentId, string(marshalledStudent), redis.KeepTTL)

		if command.Err() != nil {
			log.Fatal(err)
		}
	}
}
