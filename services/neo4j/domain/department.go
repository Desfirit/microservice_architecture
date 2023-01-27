package domain

type Department struct {
	Name       string       `json:"name"`
	Course     []Course     `json:"courses"`
	Speciality []Speciality `json:"specs"`
}
