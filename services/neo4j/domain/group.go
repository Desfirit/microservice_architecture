package domain

type Group struct {
	Id           string `json:"id"`
	SpecialityId string `json:"speciality_fk"`
}
