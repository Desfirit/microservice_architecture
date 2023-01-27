package utils

import (
	"time"
)

func IsDateStringValid(date string) bool {
	layout := "02-01-2006" // dd/mm/yyyy

	_, err := time.Parse(layout, date)

	return err == nil
}
