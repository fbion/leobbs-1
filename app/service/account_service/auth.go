package account_service

import (
	"gitee.com/leobbs/leobbs/pkg/common"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
)

func AuthGetLoginUinfo(c *gin.Context) (lu_username interface{}, lu_uid interface{}, is_admin interface{}) {
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

	is_admin = safeSess.Get("is_admin")
	if is_admin != nil {
		is_admin = true
	} else {
		is_admin = false
	}


	return lu_username,lu_uid,is_admin
}
