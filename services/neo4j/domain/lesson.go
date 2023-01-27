package domain

type Lesson struct {
	Id            int    `json:"id"`
	LessonType    string `json:"type"`
	CourseId      string `json:"course_fk"`
	DescriptionId string `json:"description_fk"`
}

type LessonDescription struct {
	Id        string `json:"id"`
	Materials string `json:"material"`
	Equipment string `json:"equipment"`
}
