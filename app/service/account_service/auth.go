package account_service

import (
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/leobbs/leobbs/pkg/common"
)

func AuthGetLoginUinfo(c *gin.Context) (luUsername interface{}, luUid interface{}, isAdmin interface{}) {
	currentMethod := "AuthGetLoginUinfo@account_service"
	safeSess := sessions.Default(c)
	luUsername = safeSess.Get("luUsername")
	common.Sugar.Infof(currentMethod+" luUsername : %v", luUsername)
	if luUsername == nil {
		luUsername = ""
	}
	luUid = safeSess.Get("luUid")
	if luUid == nil {
		luUid = 0
	}

	isAdmin = safeSess.Get("isAdmin")
	if isAdmin != nil {
		isAdmin = true
	} else {
		isAdmin = false
	}

	return luUsername, luUid, isAdmin
}
