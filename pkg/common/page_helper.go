package common

import (
	"github.com/gin-gonic/gin"
	"strconv"
)

func PageHelper(c *gin.Context) (int, int, int) {
	page, err := strconv.Atoi(c.DefaultQuery("page", "1"))

	if err != nil {
		Sugar.Error(err)
	}
	page -= 1
	if page < 0 {
		page = 0
	}

	prevPage := page
	if prevPage < 1 {
		prevPage = 1
	}
	nextPage := page + 2
	return page,  prevPage, nextPage
}

