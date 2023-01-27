package utils

import (
	"io/ioutil"
	"log"
	"net/http"
)

// supports only get requests
func ReadResponseBody(requestUrl string) []byte {
	response, err := http.Get(requestUrl)

	if err != nil {
		log.Fatal(err)
	}

	responseBody, err := ioutil.ReadAll(response.Body)

	if err != nil {
		log.Fatal(err)
	}

	return responseBody
}
