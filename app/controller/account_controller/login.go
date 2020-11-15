package account_controller

import (
	"gitee.com/leobbs/leobbs/app/form"
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/skins"
	"gitee.com/leobbs/leobbs/pkg/common"
	"gitee.com/leobbs/leobbs/pkg/passwd_utils"
	"gitee.com/leobbs/leobbs/pkg/string_utils"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
)

func LoginAction(c *gin.Context) {
	safeSess := sessions.Default(c)
	safeSess.Delete("lu_username")
	safeSess.Delete("lu_is_admin")
	_ = safeSess.Save()
	pongoContext := pongo2.Context{
		"imagesurl": "/assets",
		"skin":      "leobbs",
		"hello":     "world",
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}
	c.HTML(200, "account/login.html",
		pongoContext)
}


func DoLoginAction(c *gin.Context) {
	currentMethod := "DoLoginAction"
	var loginForm form.LoginForm

	err := c.MustBindWith(&loginForm, binding.Form)
	if err != nil {
		common.LogError(err)
		common.ShowUMessage(c, &common.Umsg{Msg: "登录失败", Url: "javascript:history.go(-1);"})
		return
	}

	var mm orm_model.Member

	result := common.DB.Where(" username = ? ", loginForm.Username).Find(&mm)
	if result.Error != nil {
		common.Sugar.Info(currentMethod + " error: %v", result.Error)
	}


	checkResult, err :=passwd_utils.CheckPasswordHash(mm.Password, loginForm.Password, mm.Salt)
	if err != nil {
		common.Sugar.Error(currentMethod + " error: %v", err)
		common.ShowUMessage(c, &common.Umsg{
			"登录失败",
			"javascript:history.go(-1);",
		})
		return
	}
	if checkResult == false {
		common.ShowUMessage(c, &common.Umsg{
			"登录失败",
			"javascript:history.go(-1);",
		})
		return
	}

	common.Sugar.Infof(currentMethod + " user %v success login", mm)


	adminUserList := common.Config.Admin_user

	safeSess := sessions.Default(c)
	safeSess.Set("lu_username", mm.Username)
	// 如果用户名在管理员列表里面，就设置为is_admin的session
	if string_utils.StringExistsInList(mm.Username, adminUserList) {
		safeSess.Set("is_admin", true)
	}

	_ = safeSess.Save()
	common.ShowUMessage(c, &common.Umsg{
		"登录成功",
		"/",
	})
	return
}
