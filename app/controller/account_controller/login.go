package account_controller

import (
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"github.com/leobbs/leobbs/app/form"
	"github.com/leobbs/leobbs/app/orm_model"
	"github.com/leobbs/leobbs/pkg/common"
	"github.com/leobbs/leobbs/pkg/passwd_utils"
	"github.com/leobbs/leobbs/pkg/string_utils"
)

func LoginAction(c *gin.Context) {
	safeSess := sessions.Default(c)
	safeSess.Delete("luUsername")
	safeSess.Delete("lu_isAdmin")
	_ = safeSess.Save()
	c.HTML(200, "account/login.html",
		common.Pongo2ContextWithVersion(pongo2.Context{
			"imagesurl": "/assets",
			"skin":      "leobbs",
			"hello":     "world",
		}))

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
		common.Sugar.Info(currentMethod+" error: %v", result.Error)
	}

	checkResult, err := passwd_utils.CheckPasswordHash(mm.Password, loginForm.Password, mm.Salt)
	if err != nil {
		common.Sugar.Error(currentMethod+" error: %v", err)
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

	common.Sugar.Infof(currentMethod+" user %v success login", mm)

	adminUserList := common.Config.Admin_user

	safeSess := sessions.Default(c)
	safeSess.Set("luUsername", mm.Username)
	safeSess.Set("luUid", mm.ID)
	// 如果用户名在管理员列表里面，就设置为isAdmin的session
	if string_utils.StringExistsInList(mm.Username, adminUserList) {
		safeSess.Set("isAdmin", true)
	}

	_ = safeSess.Save()
	common.ShowUMessage(c, &common.Umsg{
		"登录成功",
		"/",
	})
	return
}
