package router

import (
	"encoding/json"
	"fmt"
	"gateway/utils"
	"log"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"text/template"

	"github.com/go-chi/chi/v5"
)

func applyRoutes(r *chi.Mux) {
	r.Get("/api/lab1", labHandler)
}

func labHandler(w http.ResponseWriter, r *http.Request) {
	validFrom := r.URL.Query().Get("valid_from")
	validUntil := r.URL.Query().Get("valid_until")
	search := r.URL.Query().Get("search")

	if len(validFrom) == 0 {
		w.WriteHeader(400)
		w.Write([]byte("Missing required field valid_from"))

		return
	}

	if len(validUntil) == 0 {
		w.WriteHeader(400)
		w.Write([]byte("Missing required field valid_until"))

		return
	}

	if len(search) == 0 {
		w.WriteHeader(400)
		w.Write([]byte("Missing required field search"))

		return
	}

	if !utils.IsDateStringValid(validFrom) {
		w.WriteHeader(400)
		w.Write([]byte("valid_from is not a valid date"))

		return
	}

	if !utils.IsDateStringValid(validUntil) {
		w.WriteHeader(400)
		w.Write([]byte("valid_until is not a valid date"))

		return
	}

	// elastic get lesson name list
	params := url.Values{}

	params.Add("search", search)

	log.Println("checkpoint 1 (search)", search)

	lessonNameResult := utils.ReadResponseBody(
		fmt.Sprintf("http://elastic-ma:%s/api/lessons?%s",
			os.Getenv("LOCAL_SERVICES_PORT"),
			params.Encode(),
		),
	)

	type Lesson struct {
		Equipment   string `json:"equipment"`
		Materials   string `json:"materials"`
		Name        string `json:"name"`
		Id          int    `json:"id"`
		CourseId    string `json:"course_fk"`
		Description string `json:"description"`
		Type        string `json:"type"`
	}

	lessonList := []Lesson{}

	err := json.Unmarshal(lessonNameResult, &lessonList)

	if err != nil {
		log.Fatal(err)
	}

	lessonNameList := url.Values{}

	for _, lesson := range lessonList {
		lessonNameList.Add("lesson_ids", lesson.Name)
	}

	// postgres get lesson ids from lesson name list
	lessonIdResult := utils.ReadResponseBody(
		fmt.Sprintf("http://postgres-ma:%s/api/lessons?%s",
			os.Getenv("LOCAL_SERVICES_PORT"),
			lessonNameList.Encode(),
		),
	)

	var lessonPostgresDataList []Lesson

	err = json.Unmarshal(lessonIdResult, &lessonPostgresDataList)

	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))

		return
	}

	lessonIds := []string{}

	for _, lesson := range lessonPostgresDataList {
		lessonIds = append(lessonIds, strconv.Itoa(lesson.Id))
	}

	log.Println("checkpoint 2 (lessonIds)", lessonIds)
	// postgres get student ids and percentage from until lessons
	studentVisitInfo := utils.ReadResponseBody(
		fmt.Sprintf("http://postgres-ma:%s/api/students?lessons=%s&from=%s&until=%s",
			os.Getenv("LOCAL_SERVICES_PORT"),
			strings.Join(lessonIds, ","),
			validFrom,
			validUntil,
		),
	)

	var studentInfoList []struct {
		Id           string  `json:"id"`
		VisitPercent float64 `json:"visit_percent"`
	}

	err = json.Unmarshal(studentVisitInfo, &studentInfoList)

	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))

		return
	}

	var studentIdList []string

	for _, item := range studentInfoList {
		studentIdList = append(studentIdList, item.Id)
	}

	log.Println("checkpoint 3 (studentIdList)", studentIdList)

	// go to redis to get student names
	studentNameInfoList := utils.ReadResponseBody(
		fmt.Sprintf(
			"http://redis-ma:%s/api/students?students=%s",
			os.Getenv("LOCAL_SERVICES_PORT"),
			strings.Join(studentIdList, ","),
		),
	)

	var studentNameList []struct {
		StudentId string `json:"id"`
		Name      string `json:"name"`
		Surname   string `json:"surname"`
		GroupId   string `json:"group_fk"`
	}

	err = json.Unmarshal(studentNameInfoList, &studentNameList)

	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte("Could not parse json into studentName list"))

		return
	}

	log.Println("checkpoint 4 (studentNameList)", studentNameList)

	// go to postgres to get course id list
	groupCourseIdList := utils.ReadResponseBody(
		fmt.Sprintf(
			"http://postgres-ma:%s/api/courses",
			os.Getenv("LOCAL_SERVICES_PORT"),
		),
	)

	var groupCourseList []struct {
		GroupId  string `json:"group_fk"`
		CourseId int    `json:"course_fk"`
	}

	err = json.Unmarshal(groupCourseIdList, &groupCourseList)

	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte("Could not parse json into groupCourse list"))

		return
	}

	type StudentInfo struct {
		StudentName    string  `json:"student_name"`
		StudentSurname string  `json:"student_surname"`
		StudentId      string  `json:"student_id"`
		GroupName      string  `json:"group_name"`
		SpecialityName string  `json:"speciality"`
		DepartmentName string  `json:"department"`
		InstituteName  string  `json:"institute"`
		Course         string  `json:"course"`
		VisitPercent   float64 `json:"visit_percent"`
	}

	// go to neo to get group, speciality and institute
	studentInstituteInfo := utils.ReadResponseBody(fmt.Sprintf(
		"http://neo4j-ma:%s/api/students?students=%s",
		os.Getenv("LOCAL_SERVICES_PORT"),
		strings.Join(studentIdList, ","),
	))

	var resultList []StudentInfo

	err = json.Unmarshal(studentInstituteInfo, &resultList)

	if err != nil {
		log.Fatal(string(studentInstituteInfo))
	}

	for i, student := range resultList {
		for _, item := range studentNameList {
			if item.StudentId == student.StudentId {
				resultList[i].StudentName = item.Name
				resultList[i].StudentSurname = item.Surname

				break
			}
		}

		for _, visitInfo := range studentInfoList {
			if visitInfo.Id == student.StudentId {
				resultList[i].VisitPercent = visitInfo.VisitPercent
			}
		}
	}

	tmpl := template.Must(template.ParseFiles("template.html"))

	data := struct {
		Students []StudentInfo
	}{
		Students: resultList,
	}

	tmpl.Execute(w, data)

	w.WriteHeader(200)
}
