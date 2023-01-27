package domain

type Institute struct {
	Name       string       `json:"name"`
	Department []Department `json:"department"`
}
