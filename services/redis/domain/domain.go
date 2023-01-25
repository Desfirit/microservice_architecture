package domain

type Student struct {
	StudentId string `json:"id"`
	Name      string `json:"name"`
	Surname   string `json:"surname"`
	GroupId   string `json:"group_fk"`
}
