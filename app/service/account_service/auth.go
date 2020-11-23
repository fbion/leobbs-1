package account_service

import (
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
)

func AuthGetLoginUinfo(c *gin.Context) (lu_username interface{}, lu_uid interface{}, isAdmin interface{}) {
	currentMethod := "AuthGetLoginUinfo@account_service";
	safeSess := sessions.Default(c)
	lu_username = safeSess.Get("lu_username")
	common.Sugar.Infof(currentMethod +" luUsername : %v", lu_username)
	if lu_username == nil {
		lu_username = ""
	}
	lu_uid = safeSess.Get("lu_uid")
	if lu_uid == nil {
		lu_uid = 0
	}

	isAdmin = safeSess.Get("isAdmin")
	if isAdmin != nil {
		isAdmin = true
	} else {
		isAdmin = false
	}


	return lu_username,lu_uid,isAdmin
}
