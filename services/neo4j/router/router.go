package router

import (
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/neo4j/neo4j-go-driver/neo4j"
)

func NewRouter(client neo4j.Driver) *chi.Mux {
	r := chi.NewRouter()

	r.Use(middleware.Logger)

	applyRoutes(r, client)

	return r
}
