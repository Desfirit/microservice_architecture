package filler

import "github.com/neo4j/neo4j-go-driver/neo4j"

func FillInNeo(client neo4j.Driver) {
	addLessons(client)
	addLessonDescriptions(client)

	addStudents(client)
	addGroups(client)

	addMongoDbData(client)
}
